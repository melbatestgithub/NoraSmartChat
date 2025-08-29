# main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from agents import workflow

app = FastAPI()

# Serve static files (HTML/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index page
@app.get("/", response_class=HTMLResponse)
def get_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)

# API endpoint for chat
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")
    memory = data.get("memory", [])

    inputs = {"question": question, "memory": memory}
    result = workflow.invoke(inputs)

    return JSONResponse(content=result)

