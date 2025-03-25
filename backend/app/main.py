from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import shutil
import os
from .analyzers import analyze_javascript, analyze_python

app = FastAPI(
    title="Carbon Crunch",
    description="Code quality analyzer for JavaScript/React and Python/FastAPI files",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Carbon Crunch API! Use /analyze-code endpoint to analyze your code."}

@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)):
    try:
        # Check if file extension is supported
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in ['.js', '.jsx', '.py']:
            return JSONResponse(
                status_code=400,
                content={"error": "Unsupported file type. Please upload .js, .jsx, or .py files."}
            )
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        # Analyze the file based on its extension
        if file_extension in ['.js', '.jsx']:
            result = analyze_javascript(temp_file_path)
        elif file_extension == '.py':
            result = analyze_python(temp_file_path)
        
        # Clean up the temp file
        os.unlink(temp_file_path)
        
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )
    finally:
        file.file.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 