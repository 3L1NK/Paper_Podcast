from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils import extract_text_from_pdf
from rag_pipelines import summarize_with_rag
from gtts import gTTS
import os

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of main.py
TEMP_DIR = os.path.join(BASE_DIR, "temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure directories exist
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory
app.mount("/audio", StaticFiles(directory=OUTPUT_DIR), name="audio")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Paper to Podcast API. Use /upload to upload files."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save file to TEMP_DIR
        file_location = os.path.join(TEMP_DIR, file.filename)
        print("file loc = " + file_location)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Extract and summarize text
        text = extract_text_from_pdf(file_location)
        #print("text = " +text)
        summary = summarize_with_rag(text)
        print("Generated Summary:", summary)

        # Generate audio file
        audio_filename = f"{os.path.splitext(file.filename)[0]}_podcast.mp3"
        audio_filepath = os.path.join(OUTPUT_DIR, audio_filename)
        tts = gTTS(summary, lang="en")
        tts.save(audio_filepath)

        # Clean up
        os.remove(file_location)

        # Return URL
        return {"audio_url": f"http://127.0.0.1:8000/audio/{audio_filename}"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/audio/{audio_file}")
def get_audio(audio_file: str):
    audio_path = os.path.join(OUTPUT_DIR, audio_file)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg", filename=audio_file)
    return {"error": "Audio file not found"}
