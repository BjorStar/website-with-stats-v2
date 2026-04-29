from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# In-memory user storage
users = {}  # {"username": "password"}
account_created = set()  # users who already created an account

def page_layout(content: str, username: str | None = None):
    # Top-right login or username display
    if username:
        auth_box = f"""
        <div style='position:absolute; top:20px; right:20px;'>
            Logged in as <b>{username}</b>
        </div>
        """
    else:
        auth_box = """
        <div style='position:absolute; top:20px; right:20px;'>
            <form action="/login" method="post" style="display:flex; gap:5px;">
                <input name="username" placeholder="Username" style="padding:5px;">
                <input name="password" type="password" placeholder="Password" style="padding:5px;">
                <button type="submit" style="padding:5px;">Login</button>
            </form>
        </div>
        """

    # Hide create account if user already created one
    if username in account_created:
        create_section = ""
    else:
        create_section = """
        <div style="text-align:center; margin-top:40px;">
            <h3>Create Account</h3>
            <form action="/create" method="post">
                <input name="new_username" placeholder="New Username" style="padding:5px;"><br><br>
                <input name="new_password" type="password" placeholder="New Password" style="padding:5px;"><br><br>
                <button type="submit" style="padding:5px;">Create Account</button>
            </form>
        </div>
        """

    return f"""
    <html>
    <body style="font-family:Arial; margin:0; padding:0;">
        {auth_box}

        <div style="text-align:center; padding-top:100px;">
            <h1 style="font-size:48px; margin-bottom:10px;">Welcome to Sutakutu</h1>
            {content}
        </div>

        {create_section}
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
def home(user: str | None = None):
    return page_layout("<p>Your personalized homepage.</p>", username=user)

@app.post("/create", response_class=HTMLResponse)
def create_account(new_username: str = Form(...), new_password: str = Form(...)):
    if new_username in users:
        return page_layout("<h3>Username already exists.</h3>")
    users[new_username] = new_password
    account_created.add(new_username)
    return RedirectResponse(f"/?user={new_username}", status_code=302)

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username in users and users[username] == password:
        return RedirectResponse(f"/?user={username}", status_code=302)
    return RedirectResponse("/", status_code=302)
