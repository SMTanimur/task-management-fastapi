Instructions for Task Management Backend Application

Overview

We are developing a backend application for task management similar to Lark. The application will be built using FastAPI and Uvicorn, and deployed using Docker and Docker Compose for both local and production environments. Authentication will be handled using JWT tokens, including access tokens and cookie-based authentication.

Tech Stack

FastAPI: For building the backend API.

Uvicorn: ASGI server for running FastAPI applications.

JWT Authentication: Using access tokens stored in cookies.

PostgreSQL: As the database.

Alembic: For database migrations.

SQLModel: For ORM and data validation.

Pydantic: For data validation.

SQLAlchemy: For database interactions.

asyncpg: Async driver for PostgreSQL.

psycopg2: PostgreSQL adapter for Python.

Loguru: For logging.

python-dotenv: For environment variable management.

Gunicorn: For running the application in production.

bcrypt: For password hashing.

Project Structure

project-root/
│── app/
│   ├── models/       # Database models
│   ├── routes/       # API routes
│   ├── services/     # Business logic
│   ├── config.py     # Configuration settings
│── alembic/          # Database migrations
│── docker-compose.yml # Docker Compose setup
│── pyproject.toml    # Poetry dependencies
│── README.md         # Project documentation
│── instruction.md    # Development and deployment instructions

Installing Poetry on Linux Mint

Install dependencies:

sudo apt update && sudo apt install python3-pip python3-venv -y

Install Poetry:

curl -sSL https://install.python-poetry.org | python3 -

Configure PATH:

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

Verify installation:

poetry --version

Setting Up the Project

1. Clone the Repository

git clone <repository_url>
cd project-root

2. Install Dependencies with Poetry

poetry install

3. Activate the Virtual Environment

poetry shell

4. Environment Variables

Create a .env file in the root directory and add the necessary configuration:

SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_ALGORITHM=HS256
DATABASE_URL=postgresql://user:password@db/task_db

5. Run the Application

uvicorn app.main:app --reload

Running with Docker

1. Build and Start the Containers

docker-compose up --build

2. Stopping Containers

docker-compose down

Authentication Flow

User Registration: Users sign up using email and password.

Login: Users receive a JWT access token stored in an HTTP-only cookie.

Protected Routes: Users must send their JWT token in requests.

Token Refresh: Refresh tokens can be used to obtain new access tokens.

Task Management Features

Create, update, delete, and assign tasks.

Set task priority, due dates, and status.

Assign tasks to users and teams.

User Management Features

Register and authenticate users.

Manage user profiles and roles.

Deployment to Production

Configure .env with production settings.

Use docker-compose.prod.yml for production setup.

Deploy to a cloud server with Docker support.

Next Steps

Implement role-based access control (RBAC).

Add logging and monitoring.

Improve API documentation with Swagger (built into FastAPI).

