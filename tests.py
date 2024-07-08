import pytest
from flask_mongoengine import MongoEngine

from mongoengine import disconnect

from src.config import TestConfig, Config

from src import app
from src.logger.models import LoggerModel
from src.posts.models import Posts
from src.user.models import User


@pytest.fixture
def app_test():
    app.config.from_object(TestConfig)
    app_context = app.app_context()
    app_context.push()

    disconnect(alias='default')

    db = MongoEngine(app)

    Posts.drop_collection()
    User.drop_collection()
    LoggerModel.drop_collection()

    yield app

    Posts.drop_collection()
    User.drop_collection()
    LoggerModel.drop_collection()
    app_context.pop()
    app.config.from_object(Config)


@pytest.fixture
def client(app_test):
    return app_test.test_client()


def get_log(**kwargs) -> LoggerModel:
    return LoggerModel.objects(**kwargs).first()


def create_user(client):

    return client.post('/register', json={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'password123'
    })


def login_dummy_user(client):
    return client.get('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })


def create_post(client, access_token):
    return client.post('/posts', json={
        'title': 'Test Post',
        'text': 'This is a test post.'
    }, headers={'Authorization': f'Bearer {access_token}'})


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register_user(client):
    response = create_user(client)
    assert response.status_code == 201
    assert b'User has been registered successfully' in response.data

    log = get_log(
        info_type='INFO',
        message='User test@example.com, Test User was created successfully'
    )
    assert log


def test_register_duplicated_user(client):
    original_user_response = create_user(client)

    duplicated_user_response = create_user(client)

    assert duplicated_user_response.status_code == 400
    assert b'Email is already taken!' in duplicated_user_response.data

    log = get_log(
        info_type='ERROR',
        message='Error "Email is already taken!" occurred in /register with method: POST'
    )
    assert log


def test_login_user(client):
    create_user(client)

    response = login_dummy_user(client)

    assert response.status_code == 200
    assert b'access_token' in response.data

    log = get_log(
        info_type='INFO',
        message='User test@example.com, Test User has logged in'
    )
    assert log


def test_failed_login(client):
    response = login_dummy_user(client)

    assert response.status_code == 401
    assert b'wrong credentials!' in response.data


def test_create_post(client):
    create_user(client)

    response = login_dummy_user(client)
    access_token = response.json['access_token']

    response = create_post(client, access_token)

    assert response.status_code == 200
    assert b'Post was successfuly created!' in response.data

    post_id = response.json.get('post').get('id')

    log = get_log(
        info_type='INFO',
        message=f"test@example.com, Test User created a new record at base_model table with id {post_id} in /posts"
    )
    assert log


def test_validation_error_in_create_post(client):
    create_user(client)

    response = login_dummy_user(client)
    access_token = response.json['access_token']

    response = client.post('/posts', json={
        'title': 'Test Post'
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 400
    assert b"ValidationError (BaseModel.Posts:None) (Field is required: ['text'])" in response.data

    log = get_log(
        info_type='ERROR',
        message='''test@example.com, Test User got an error '''
                '''"ValidationError (BaseModel.Posts:None) (Field is required: ['text'])" in /posts with method: POST'''
    )
    assert log


def test_get_posts(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert b'posts' in response.data


def test_update_post(client):
    create_user(client)

    response = login_dummy_user(client)
    access_token = response.json['access_token']

    post_response = create_post(client, access_token)
    post_id = post_response.json['post']['id']

    response = client.patch(f'/posts/{post_id}', json={
        'title': 'Updated Test Post',
        'text': 'This is an updated test post.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert b'Post was successfuly updated!' in response.data

    log = get_log(
        info_type='INFO',
        message="test@example.com, Test User changed ['title', 'text'] from "
                "{'title': 'Test Post', 'text': 'This is a test post.'} to "
                "{'text': 'This is an updated test post.', 'title': 'Updated Test Post'} at "
                f"base_model in /posts/{post_id}"
    )
    assert log is not None


def test_validation_error_in_update_post(client):
    create_user(client)

    response = login_dummy_user(client)
    access_token = response.json['access_token']

    post_response = create_post(client, access_token)
    post_id = post_response.json['post']['id']

    response = client.patch(f'/posts/{post_id}', json={
        'title': 'Updated Test Post',
        'text': 'This is an updated test post.',
        'unreal_field': 'text'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 400
    assert b"'unreal_field' is not a valid field" in response.data

    log = get_log(
        info_type='ERROR',
        message='''test@example.com, Test User got an error "'unreal_field' is not a valid field" '''
                f'''in /posts/{post_id} with method: PATCH'''
    )
    assert log is not None


def test_delete_post(client):
    create_user(client)

    response = login_dummy_user(client)
    access_token = response.json['access_token']

    post_response = create_post(client, access_token)
    post_id = post_response.json['post']['id']

    response = client.delete(f'/posts/{post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert b'Post was successfuly deleted!' in response.data

    log = get_log(
        info_type='INFO',
        message=f'test@example.com, Test User deleted record at base_model table with '
                f'id {post_id} in /posts/{post_id}'
    )
    assert log is not None


def test_delete_unreal_post(client):
    create_user(client)

    response = login_dummy_user(client)
    access_token = response.json['access_token']

    fake_post_id = '668a700a1a4e4bcaa7490904'

    response = client.delete(f'/posts/{fake_post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 400
    assert b'Post with id 668a700a1a4e4bcaa7490904 does not exist!' in response.data

    log = get_log(
        info_type='ERROR',
        message='test@example.com, Test User got an error '
                f'"Post with id {fake_post_id} does not exist!" in /posts/{fake_post_id} with method: DELETE'
    )
    assert log is not None


