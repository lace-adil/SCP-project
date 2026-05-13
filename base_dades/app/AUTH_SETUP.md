# SCP Database - Authentication Setup

This authentication system has been added to your FastAPI application. Here's what was implemented:

## Features Added

### 1. **User Authentication**
   - Login page with form validation
   - User registration page
   - Password hashing using bcrypt
   - Session management with secure cookies
   - Logout functionality

### 2. **Database Schema**
   - Users table with id, username, and hashed password
   - Password storage using bcrypt hashing

### 3. **New Endpoints**
   - `GET /login` - Serves the login form
   - `POST /auth/login` - Handles login submissions
   - `GET /dashboard` - Protected route for authenticated users
   - `POST /auth/logout` - Handles logout
   - `GET /auth/register` - Serves the registration form
   - `POST /auth/register` - Handles user registration

### 4. **HTML Templates**
   - `templates/login.html` - Beautiful login form
   - `templates/register.html` - User registration form
   - `templates/dashboard.html` - Protected dashboard with database access

## How to Use

### 1. **Install Dependencies**
```bash
cd /home/yurest/Desktop/projecte_SCP/base_dades/app
poetry install
```

### 2. **Update the Database Schema**
The users table should already exist from your migration. If not, run:
```bash
poetry run alembic upgrade head
```

### 3. **Start the Application**
```bash
poetry run uvicorn src.main:app --reload
```

### 4. **Access the Application**
- Navigate to `http://localhost:8000/login`
- Click "Register here" to create a new account
- Use any username and password (minimum 6 characters)
- After registration, login with your credentials
- You'll be redirected to the dashboard

### 5. **Dashboard Features**
Once logged in, you can:
- View all SCP subjects from the database
- Add new SCP subjects
- Update the database schema
- Access all your existing SCP endpoints (API)

## Security Notes

⚠️ **Important**: The current session management uses in-memory storage. For production:
1. Use Redis or a database for session storage
2. Implement CSRF protection
3. Use HTTPS only
4. Add rate limiting to login attempts
5. Implement email verification for registration
6. Add password reset functionality

## File Structure
```
base_dades/app/
├── src/
│   ├── main.py (updated)
│   ├── database/
│   │   ├── __init__.py (existing SCP routes)
│   │   ├── auth.py (NEW - authentication logic)
│   │   └── schemas.py (updated with User models)
│   └── utils/
│       └── __init__.py (updated with password hashing)
├── templates/
│   ├── login.html (NEW)
│   ├── register.html (NEW)
│   └── dashboard.html (NEW)
├── pyproject.toml (updated with new dependencies)
└── alembic/ (migrations)
```

## Dependencies Added
- `passlib` - Password hashing
- `python-multipart` - Form data handling
- `jinja2` - Template rendering

Enjoy your new authentication system!
