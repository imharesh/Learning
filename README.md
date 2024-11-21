# FastAPI Backend with SQLAlchemy and Alembic

This is the development branch of the backend application built with FastAPI, SQLAlchemy, and Alembic.

## Features

- FastAPI REST API
- SQLAlchemy ORM with PostgreSQL
- Alembic database migrations
- JWT Authentication
- Soft Delete functionality
- User and Article management
- Environment configuration
- Development tools integration

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/imharesh/Learning.git
cd Learning
git checkout dev
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# OR
.\venv\Scripts\activate  # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```env
DATABASE_URL=postgresql://postgres:root@localhost:5432/article_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Initialize the database:
```bash
# Create the database in PostgreSQL
createdb article_db

# Run migrations
python -m alembic upgrade head
```

6. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Development

- The project uses Alembic for database migrations
- Black for code formatting
- Flake8 for code linting
- isort for import sorting

### Creating New Migrations

After making changes to SQLAlchemy models:
```bash
python -m alembic revision --autogenerate -m "Description of changes"
python -m alembic upgrade head
```

## Branch Strategy

- `main`: Production-ready code
- `dev`: Development branch, feature branches should be created from here
- Feature branches: Create from `dev` branch

## Testing

Run tests with:
```bash
pytest
```

## Contributing

1. Create a new feature branch from dev:
```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

2. Make your changes and commit:
```bash
git add .
git commit -m "Description of your changes"
```

3. Push to remote and create a pull request to dev branch:
```bash
git push origin feature/your-feature-name
```
