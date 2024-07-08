from src import api
from src.posts.views import PostsDetailedView, PostsCollectionView
from src.user.views import AuthRegister, AuthLogin


api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(PostsCollectionView, '/posts', strict_slashes=False)
api.add_resource(PostsDetailedView, '/posts/<string:post_id>', strict_slashes=False)
