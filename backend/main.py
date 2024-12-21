from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_text_from_pdf
from rag_pipelines import summarize_with_rag
from tts_services import google_tts, amazon_polly_tts, elevenlabs_tts
import os

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of main.py
TEMP_DIR = os.path.join(BASE_DIR, "temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure directories exist
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# FastAPI App Initialization
app = FastAPI()

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only, restrict in production)
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    tts_service: str = Query("google")  # Default TTS service is Google
):
    try:
        # Save the uploaded file
        file_location = os.path.join(TEMP_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(file_location)
        summary = summarize_with_rag(text)

        # Generate the audio file
        audio_filename = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}_podcast.mp3")
        
        if tts_service == "google":
            google_tts(summary, audio_filename)
        elif tts_service == "amazon":
            amazon_polly_tts(summary, audio_filename)
        elif tts_service == "elevenlabs":
            elevenlabs_tts(summary, audio_filename)
        else:
            raise ValueError("Unsupported TTS service selected")

        # Clean up the temporary uploaded file
        os.remove(file_location)
        
        return {
            "audio_url": f"http://127.0.0.1:8000/audio/{os.path.basename(audio_filename)}"
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/audio/{audio_file}")
def get_audio(audio_file: str):
    """
    Retrieve the generated audio file from the server.
    """
    audio_path = os.path.join(OUTPUT_DIR, audio_file)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg", filename=audio_file)
    return {"error": "Audio file not found"}
