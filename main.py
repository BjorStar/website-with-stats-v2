from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Single File App</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Hello from main.py</h1>
        <p>This entire page is generated directly by Python.</p>

        <button onclick="alert('JS works!')">Click me</button>

        <script>
            console.log("Inline JS is working");
        </script>
    </body>
    </html>
    """
