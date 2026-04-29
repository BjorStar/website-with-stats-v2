from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# In-memory user storage
users = {}  # {"username": "password"}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body>
        <h2>Login</h2>
        <form action="/login" method="post">
            <input name="username" placeholder="Username"><br>
            <input name="password" type="password" placeholder="Password"><br>
            <button type="submit">Login</button>
        </form>

        <h2>Create Account</h2>
        <form action="/create" method="post">
            <input name="new_username" placeholder="New Username"><br>
            <input name="new_password" type="password" placeholder="New Password"><br>
            <button type="submit">Create Account</button>
        </form>
    </body>
    </html>
    """

@app.post("/create", response_class=HTMLResponse)
def create_account(new_username: str = Form(...), new_password: str = Form(...)):
    if new_username in users:
        return """
        <html><body>
        <h3>Username already exists.</h3>
        <a href="/">Back</a>
        </body></html>
        """
    users[new_username] = new_password
    return """
    <html><body>
    <h3>Account created successfully!</h3>
    <a href="/">Login</a>
    </body></html>
    """

@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    if username in users and users[username] == password:
        return f"""
        <html><body>
        <h1>Welcome, {username}!</h1>
        <p>You are logged in.</p>
        </body></html>
        """
    return RedirectResponse("/", status_code=302)
