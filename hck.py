from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile
import black
import os

app = FastAPI(title="CodeRefine API")

# 🟢 ADDED: Enable CORS so your HTML file can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any local file to connect
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

@app.get("/")
def home():
    return {"message": "Welcome to CodeRefine Backend 🚀"}

@app.post("/format")
def format_code(data: CodeInput):
    try:
        formatted_code = black.format_str(data.code, mode=black.FileMode())
        return {"status": "success", "formatted_code": formatted_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/analyze")
def analyze_code(data: CodeInput):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(data.code.encode())
            temp_path = temp.name
        result = subprocess.run(["pylint", temp_path], capture_output=True, text=True)
        os.remove(temp_path)
        return {"status": "success", "analysis": result.stdout}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/refine")
def refine_code(data: CodeInput):
    try:
        formatted_code = black.format_str(data.code, mode=black.FileMode())
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(formatted_code.encode())
            temp_path = temp.name
        result = subprocess.run(["pylint", temp_path], capture_output=True, text=True)
        os.remove(temp_path)
        return {
            "status": "success",
            "formatted_code": formatted_code,
            "analysis": result.stdout
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}