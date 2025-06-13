import os
from pathlib import Path
import markdown2
from src.ai_cv_advisor.crew import CareerSupportCrew
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")


UPLOAD_DIR = Path("/uploads")
OUTPUT_DIR = Path("/output")
MARKDOWN_FILE = OUTPUT_DIR / "result.md"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Upload CV</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <h2>Upload Your CV (PDF)</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="cv_file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """


@app.post("/upload")
async def upload_cv(cv_file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = UPLOAD_DIR / cv_file.filename
        cv_file.save(file_path)
        
        # Analyze the file to markdown
        cv_crew = CareerSupportCrew(inputs={'pdf_path': str(file_path)})
        cv_crew.crew().kickoff(inputs={'pdf_path': str(file_path)})

        return RedirectResponse(url="/result", status_code=302)

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.get("/result", response_class=HTMLResponse)
async def view_result():
    try:
        if not (OUTPUT_DIR / "result.md").exists():
            return HTMLResponse("<h3>No result found. Please upload a CV first.</h3>", status_code=404)

        markdown_text = (OUTPUT_DIR / "result.md").read_text(encoding="utf-8")
        html_content = markdown2.markdown(markdown_text)

        return HTMLResponse(content=f"""
        <html>
            <head>
                <title>CV Analysis Result</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <body>
                <h1>CV Analysis Result</h1>
                <div class="content">
                    {html_content}
                </div>
            </body>
        </html>
        """)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

