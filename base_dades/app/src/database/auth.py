from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlalchemy
import src.utils as utils
from .schemas import UserLogin
from datetime import datetime, timedelta
import os

router = APIRouter(tags=["auth"])

# Simple in-memory session storage (in production, use secure session management)
sessions = {}

def get_template_path(filename: str) -> str:
    """Get the full path to a template file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, "templates", filename)

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Serve the login page. Redirect to dashboard if already logged in."""
    session_id = request.cookies.get("session_id")
    
    if session_id and session_id in sessions:
        session = sessions[session_id]
        if datetime.now() <= session["expires_at"]:
            return RedirectResponse(url="/dashboard", status_code=302)
    
    with open(get_template_path("login.html"), "r") as f:
        return f.read()

@router.post("/auth/login")
async def login(request: Request):
    """Handle login form submission."""
    try:
        form_data = await request.form()
        username = form_data.get("username")
        password = form_data.get("password")
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password required")
        
        # Query database for user
        with utils.db_engine.connect() as db_con:
            result = db_con.execute(
                sqlalchemy.text("SELECT id, username, password FROM users WHERE username = :username"),
                {"username": username}
            )
            user = result.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        user_id, db_username, hashed_password = user
        
        # Verify password
        if not utils.verify_password(password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Create session
        session_id = utils.generate_session_id()
        sessions[session_id] = {
            "user_id": user_id,
            "username": db_username,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }
        
        # Redirect to dashboard with session cookie
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie("session_id", session_id, httponly=True, max_age=86400)
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the dashboard page for authenticated users."""
    session_id = request.cookies.get("session_id")
    
    if not session_id or session_id not in sessions:
        return RedirectResponse(url="/login", status_code=302)
    
    session = sessions[session_id]
    if datetime.now() > session["expires_at"]:
        del sessions[session_id]
        return RedirectResponse(url="/login", status_code=302)
    
    # Read and render dashboard template
    with open(get_template_path("dashboard.html"), "r") as f:
        content = f.read()
    
    # Simple template substitution
    content = content.replace("{{ username }}", session["username"])
    return content

@router.post("/auth/logout")
async def logout(request: Request):
    """Handle logout."""
    session_id = request.cookies.get("session_id")
    
    if session_id and session_id in sessions:
        del sessions[session_id]
    
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_id")
    return response

@router.get("/auth/register", response_class=HTMLResponse)
def register_page():
    """Serve the register page."""
    with open(get_template_path("register.html"), "r") as f:
        return f.read()

@router.post("/auth/register")
async def register(request: Request):
    """Handle user registration."""
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    password_confirm = form_data.get("password_confirm")
    
    if not username or not password or not password_confirm:
        raise HTTPException(status_code=400, detail="All fields are required")
    
    if password != password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Check if user already exists
    with utils.db_engine.connect() as db_con:
        result = db_con.execute(
            sqlalchemy.text("SELECT id FROM users WHERE username = :username"),
            {"username": username}
        )
        existing_user = result.fetchone()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password and insert user
    hashed_password = utils.hash_password(password)
    
    with utils.db_engine.connect() as db_con:
        db_con.execute(
            sqlalchemy.text("INSERT INTO users (username, password) VALUES (:username, :password)"),
            {"username": username, "password": hashed_password}
        )
        db_con.commit()
    
    # Redirect to login
    return RedirectResponse(url="/login", status_code=302)
