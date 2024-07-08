<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>

<h1>Test Logger for Flask app</h1>

<h2>Prerequisites</h2>
<p>Before running the project, make sure you have the following installed:</p>
<ul>
    <li>Python (version 3.12)</li>
    <li>Poetry</li>
    <li>Docker</li>
    <li>Docker Compose (if using Docker)</li>
</ul>

<h2>Setup and Installation</h2>

<h3>Setting Up Flask Project</h3>

<ol>
    <li>Clone the repository:
        <pre><code>git clone &lt;repository-url&gt;
cd logger_test_assessment</code></pre>
    </li>
    <li>Install dependencies:
        <pre><code>poetry install</code></pre>
    </li>
    <li>Set up environment variables:
        <p>Create a <code>.env</code> file in the root of your project and add the following environment variables:</p>
        <pre><code>DB_NAME=flask_db
DB_HOST=localhost
DB_PORT=27017
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example
PORT=80
SECRET_KEY=you-will-never-know</code></pre>
    </li>
    <li>Run the Flask application:
        <pre><code>python wsgi.py</code></pre>
        <p>This will start the Flask server locally. Access the application at <a href="http://localhost:80">http://localhost:80</a> by default.</p>
    </li>
</ol>

<h3>Running the local MongoDB server with Docker Compose</h3>
<ol>
    <li>Build and run Docker containers:
        <pre><code>docker-compose up --build</code></pre>
        <p>This command builds the Docker images and starts the containers defined in <code>docker-compose.yml</code>.</p>
    </li>
    <li>Accessing the application:
        <p>Once Docker Compose has started the containers, you can access the local database.</p>
    </li>
</ol>

<h2>API Endpoints</h2>
<ul>
    <li><code>POST /register</code> - Register a new user</li>
    <li><code>POST /login</code> - Login an existing user</li>
    <li><code>GET /posts</code> - Get a collection of posts</li>
    <li><code>POST /posts</code> - Create a new post</li>
    <li><code>GET /posts/&lt;post_id&gt;</code> - Get details of a specific post</li>
    <li><code>PUT /posts/&lt;post_id&gt;</code> - Update a specific post</li>
    <li><code>DELETE /posts/&lt;post_id&gt;</code> - Delete a specific post</li>
    <li><code>GET /</code> - Get logs</li>
</ul>

<h2>Project Structure</h2>

<pre><code>Path/to/project:
│   .env - Environment variables file
│   .gitignore - Files that should be ignored by GIT
│   docker-compose.yaml - Docker-compose file with MongoDB config
│   poetry.lock - Poetry lock file
│   pyproject.toml - Poetry Virtual environment file
│   tests.py - Pytests
│   wsgi.py - Run server script
│
├───logging
│       py.log - Base logging file
│
├───src
│   │   base_classes.py - Base classes for an inheritance
│   │   config.py - Config of the project
│   │   routes.py - Endpoints declaration
│   │   __init__.py - App's initialization
│   │
│   ├───logger
│   │   │   logger.py - Logger initialization and Logging messages templates
│   │   │   models.py - Logger model
│   │   │   views.py - Get Logs info logic
│   │   │   __init__.py
│   │
│   ├───posts
│   │   │   models.py - Posts model
│   │   │   views.py - Posts CRUD logic
│   │
│   ├───static
│   ├───templates
│   │       index.html - HTML file for visualization of logs
│   │
│   ├───user
│   │   │   models.py - User models
│   │   │   utils.py - Authentication utils
│   │   │   views.py - Auth and Register logic
│   │   │   __init__.py
</code></pre>

<h2>Additional Notes</h2>
<p>How to install poetry - <a href="https://python-poetry.org/docs/">https://python-poetry.org/docs/</a></p>

</body>
</html>
