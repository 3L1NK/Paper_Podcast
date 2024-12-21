# Paper to Podcast - README

## Overview
The **Paper to Podcast** project allows users to upload a research paper (in PDF format) and transform it into an audio podcast using AI. This pipeline uses advanced techniques like Retrieval-Augmented Generation (RAG) and Text-to-Speech (TTS) to extract, summarize, and convert text into an audio file.

---

## Features
- Drag-and-drop UI for PDF upload
- Automatic text extraction from PDFs
- Summarization of text using OpenAI’s GPT models
- Audio generation using Google Text-to-Speech (gTTS), Amazon Polly, and ElevenLabs
- Simple, aesthetic, and user-friendly frontend
- Backend API built with FastAPI

---

## Requirements

### Backend
- Python 3.10+
- Required Python Libraries (see `requirements.txt`):
  - FastAPI
  - LangChain
  - gTTS
  - PyPDF2
  - Uvicorn
  - dotenv
  - boto3
  - requests

### Frontend
- HTML, CSS (with TailwindCSS)
- JavaScript (for interacting with the API)

### Additional
- An OpenAI API key (needed for text summarization)
- AWS Access Key (for Amazon Polly)
- ElevenLabs API key
- Node.js (for running the frontend locally using `http-server`)

---

## Project Structure
```
Paper_Podcast/
├── backend/
│   ├── main.py                # FastAPI application
│   ├── rag_pipelines.py       # RAG summarization pipeline
│   ├── tts_services.py        # Text-to-Speech services
│   ├── utils.py               # PDF text extraction utility
│   ├── uvicorn_config.py      # Uvicorn server configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment vars (API keys)
│   ├── output/                # Folder for gen audio files
│   └── temp/                  # Temporary folder for uploaded files
├── frontend/
│   ├── src/
│     ├── dist/
│     ├── index.html             # Frontend HTML file
│     ├── input.css              # TailwindCSS configuration
│     ├── app.js                 # Frontend JavaScript logic
│     ├── package.json
│     └── tailwind.config.js      
└── README.md                  # Project README
```

---

## Installation

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Paper_Podcast/backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your `.env` file:
   - Create a `.env` file in the `backend` directory.
   - Add your API keys:
     ```
     OPENAI_API_KEY=your-openai-api-key
     ELEVENLABS_API_KEY=your-elevenlabs-api-key
     AWS_ACCESS_KEY_ID=your-aws-access-key
     AWS_SECRET_ACCESS_KEY=your-aws-secret-key
     ```

5. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   - The server will be available at `http://127.0.0.1:8000`.

### Frontend Setup
1. Navigate to the `src` directory:
   ```bash
   cd Paper_Podcast/src
   ```

2. Install `http-server` (if not already installed):
   ```bash
   npm install -g http-server
   ```

3. Start the frontend server:
   ```bash
   http-server .
   ```
   - The frontend will be available at `http://127.0.0.1:8080`.

---

## Usage
1. Open the frontend in your browser (`http://127.0.0.1:8080`).
2. Drag and drop a PDF file into the upload area.
3. Select your preferred TTS service (Google, Amazon Polly, or ElevenLabs).
4. Wait for the backend to process the file.
5. Once completed, an audio player will appear with the generated podcast.
6. Download the audio file using the provided link.

---

## Environment Variables
The backend requires an `.env` file with the following keys:
- **OPENAI_API_KEY**: Your OpenAI API key for text summarization.
- **ELEVENLABS_API_KEY**: Your ElevenLabs API key for TTS.
- **AWS_ACCESS_KEY_ID**: AWS access key for Amazon Polly.
- **AWS_SECRET_ACCESS_KEY**: AWS secret key for Amazon Polly.

Example `.env` file:
```
OPENAI_API_KEY=your-openai-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

---

## Troubleshooting
### Common Issues
1. **Error: Audio URL not returned by backend**:
   - Ensure the backend is running on `http://127.0.0.1:8000`.
   - Check the console logs for errors in the backend.

2. **OpenAI API quota exceeded**:
   - Check your OpenAI API usage on [OpenAI’s dashboard](https://platform.openai.com/account/usage).
   - Upgrade your plan or reduce the size of the input PDF.

3. **CORS Errors**:
   - Ensure the backend’s CORS settings allow requests from the frontend’s origin.

4. **Environment Variables Missing**:
   - Make sure your `.env` file exists and contains the correct API keys.

---

## Text-to-Speech Services
For improved results, consider:
- **Google TTS:** Free and simple to use.
- **Amazon Polly:** Offers more natural voices.
- **ElevenLabs:** High-quality emotional AI voices.

---

## Acknowledgments
- **OpenAI**: For GPT APIs.
- **Google Text-to-Speech (gTTS)**: For audio generation.
- **Amazon Polly:** For natural speech synthesis.
- **ElevenLabs:** For advanced AI voices.
- **LangChain**: For building the RAG pipeline.
- **FastAPI**: For backend API development.

---

## Future Enhancements
- Add support for multiple languages in text-to-speech.
- Allow users to customize the podcast’s tone and voice.
- Deploy the application online for public use.
- Implement user authentication and API key management.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

