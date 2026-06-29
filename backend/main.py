import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException  # type: ignore
from fastapi.responses import HTMLResponse, JSONResponse  # type: ignore
from fastapi.staticfiles import StaticFiles  # type: ignore
import uvicorn  # type: ignore

from services.pdf_parser import extract_text_from_pdf  # type: ignore
from services.ai_generator import generate_questions  # type: ignore

app = FastAPI(title="DocQuest")

# Mount the frontend directory for static files
# We ensure the path works regardless of where you start the server from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

try:
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
except RuntimeError:
    print(f"Warning: {FRONTEND_DIR} does not exist yet. Static files won't be served.")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Frontend not found</h1><p>Please create frontend/index.html</p>"

@app.post("/api/analyze")
async def analyze_pdf(
    file: UploadFile = File(...),
    num_questions: int = Form(5),
    difficulty: str = Form("Medium")
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    try:
        # Read the uploaded file into bytes
        content = await file.read()
        
        # Extract text from the PDF content
        text = extract_text_from_pdf(content)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It may be an image-based PDF or empty.")
            
        # Call the AI service to generate questions
        result = await generate_questions(text, num_questions, difficulty)
        
        return JSONResponse(content={"status": "success", "data": result})
        
    except ValueError as e:
        # Catch specific value errors (e.g., API key missing)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An error occurred while analyzing the document.")

if __name__ == "__main__":
    # Changed to 127.0.0.1 so the link printed in the terminal works when clicked
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
