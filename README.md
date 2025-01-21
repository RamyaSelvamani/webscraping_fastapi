# webscraping_fastapi

Web Scraping with FastAPI
This project is a FastAPI-based web scraping application that includes features for authentication and version management. The project is structured to allow scalability and maintainability, leveraging best practices in Python web development.

Project Features
FastAPI for building RESTful APIs.
Authentication Module for secure user login and token-based access.
Version Management Module for tracking and managing application versions.
Middleware for logging HTTP requests and response times.
Database integration using SQLAlchemy and Alembic for migrations.


Folder Structure
.
├── alembic/           # Alembic files for database migrations
├── routers/           # API route definitions
│   ├── auth.py        # Authentication routes
│   └── versions.py    # Version management routes
├── __pycache__/      
├── database.py        # Database connection and setup
├── main.py            # Application entry point
├── models.py          # Database models
├── schemas.py         # Pydantic schemas for data validation
├── utils.py           # Utility functions
├── requirements.txt   # Project dependencies
└── alembic.ini        # Alembic configuration file

How to Run the Project

Step 1: Clone the Repository
  git clone <repository-url>
  cd <repository-folder>

Step 2: Create and Activate a Virtual Environment

  python -m venv venv
  venv\Scripts\activate      


Step 3: Install Dependencies

  pip install -r requirements.txt

Step 4: Set Up the Database
Update the database connection details in database.py and alembic.ini.
Run migrations to initialize the database:

  alembic upgrade head
  
Step 5: Start the FastAPI Server

  uvicorn main:app --reload
The application will be available at http://127.0.0.1:8000.

API Endpoints:
Authentication
POST /auth/login - User login
POST /auth/register - User registration

Version Management
GET /versions - Fetch all versions
POST /versions - Add a new version
PUT /versions/{id} - Update a version
DELETE /versions/{id} - Delete a version
Root Endpoint
GET / - Welcome message: { "message": "Welcome to OTG" }
