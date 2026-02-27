from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import black
import os

app = FastAPI(title="CodeRefine API")

# Request Model
class CodeInput(BaseModel):
    code: str


# 🟢 Home Route
@app.get("/")
def home():
    return {"message": "Welcome to CodeRefine Backend 🚀"}


# 🟢 Code Formatter Route
@app.post("/format")
def format_code(data: CodeInput):
    try:
        formatted_code = black.format_str(data.code, mode=black.FileMode())
        return {
            "status": "success",
            "formatted_code": formatted_code
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# 🟢 Code Analysis Route
@app.post("/analyze")
def analyze_code(data: CodeInput):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(data.code.encode())
            temp_path = temp.name

        # Run pylint
        result = subprocess.run(
            ["pylint", temp_path],
            capture_output=True,
            text=True
        )

        os.remove(temp_path)

        return {
            "status": "success",
            "analysis": result.stdout
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# 🟢 Combined Refine Route
@app.post("/refine")
def refine_code(data: CodeInput):
    try:
        # Format
        formatted_code = black.format_str(data.code, mode=black.FileMode())

        # Analyze
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(formatted_code.encode())
            temp_path = temp.name

        result = subprocess.run(
            ["pylint", temp_path],
            capture_output=True,
            text=True
        )

        os.remove(temp_path)

        return {
            "status": "success",
            "formatted_code": formatted_code,
            "analysis": result.stdout
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }