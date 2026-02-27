from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import tempfile
import black
import os

app = FastAPI(title="CodeRefine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

@app.post("/refine")
def refine_code(data: CodeInput):
    try:
        # Format the code first
        formatted_code = black.format_str(data.code, mode=black.FileMode())
        
        # 🟢 FIX: Automatically add a docstring if the user forgot one
        process_code = formatted_code
        if not (process_code.strip().startswith('"""') or process_code.strip().startswith("'''")):
            process_code = '"""Auto-generated docstring for CodeRefine."""\n' + process_code

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(process_code.encode())
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
