from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_text_from_pdf
from rag_pipelines import summarize_with_rag
from gtts import gTTS
import os

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Paper to Podcast API. Use /upload to upload files."}

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Extract text from PDF
        text = extract_text_from_pdf(file_location)

        # Summarize with RAG
        summary = summarize_with_rag(text)

        # Generate podcast audio
        audio_filename = f"output/{os.path.splitext(file.filename)[0]}_podcast.mp3"
        tts = gTTS(summary, lang="en")
        tts.save(audio_filename)

        # Clean up the temporary PDF file
        os.remove(file_location)

        return {"audio_url": f"http://localhost:8000/audio/{os.path.basename(audio_filename)}"}

    except Exception as e:
        return {"error": str(e)}

# Serve generated audio files
@app.get("/audio/{audio_file}")
def get_audio(audio_file: str):
    audio_path = f"output/{audio_file}"
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg", filename=audio_file)
    else:
        return {"error": "Audio file not found"}

# Create temp and output directories if they don't exist
os.makedirs("temp", exist_ok=True)
os.makedirs("output", exist_ok=True)
