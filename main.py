from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import secrets
import time

app = FastAPI()

# Static files (optional, for CSS/images if you add them later)
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory user store (demo)
users = {
    "gym": "password123",
    "admin": "admin"
}

# In-memory session store
sessions = {}


def create_session(username: str, remember: bool = False) -> str:
    session_id = secrets.token_hex(32)
    # 1 hour vs 30 days
    expiry = time.time() + (60 * 60 * 24 * 30 if remember else 60 * 60)
    sessions[session_id] = {"username": username, "expires": expiry}
    return session_id


def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    session = sessions.get(session_id)
    if not session:
        return None
    if session["expires"] < time.time():
        # Session expired
        del sessions[session_id]
        return None
    return session["username"]


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/home", status_code=302)

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Login</h1>
        <form method="post" action="/login">
            <div>
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div>
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <div>
                <label>
                    <input type="checkbox" name="remember">
                    Remember me
                </label>
            </div>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    remember: bool = Form(False),
):
    if username in users and users[username] == password:
        session_id = create_session(username, remember)
        response = RedirectResponse(url="/home", status_code=302)
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=60 * 60 * 24 * 30 if remember else None,
        )
        return response

    # Simple invalid login page
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html>
        <head><title>Login failed</title></head>
        <body>
            <h1>Login failed</h1>
            <p>Invalid username or password.</p>
            <a href="/">Back to login</a>
        </body>
        </html>
        """,
        status_code=401,
    )


@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home</title>
        <meta charset="utf-8">
    </head>
    <body>
        <header>
            <div style="float:right;">
                Logged in as: <strong>{user}</strong>
                | <a href="/logout">Logout</a>
            </div>
            <h1>Welcome, {user}!</h1>
        </header>
        <main>
            <p>This is your protected home page.</p>
            <p>Add your stats, images, or other content here.</p>
        </main>
    </body>
    </html>
    """


@app.get("/logout")
def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_id")
    return response


# For local testing:
# uvicorn main:app --host 0.0.0.0 --port 8000
