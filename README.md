# 🎙️ AI Meeting Intelligence

AI Meeting Intelligence is an NLP-powered application that transcribes meeting audio, generates AI summaries, extracts action items, and stores meeting history using SQLite.

## Features

* 🎧 Upload meeting audio files (MP3, WAV, M4A)
* 📝 Automatic transcription using OpenAI Whisper
* 🤖 AI-powered meeting summaries using Google Gemini
* 📋 Action item extraction
* 📄 PDF report generation
* 🗄️ SQLite database storage
* 📁 Meeting history viewer
* 🔍 Search past meetings

## Tech Stack

### Frontend

* Streamlit

### AI & NLP

* OpenAI Whisper
* Google Gemini

### Database

* SQLite

### PDF Generation

* ReportLab

### Language

* Python

---

## Project Structure

```text
meeting-intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── transcriber.py
│   ├── summarizer.py
│   └── pdf_generator.py
│
├── database/
├── uploads/
├── outputs/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/meeting-intelligence.git
cd meeting-intelligence
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Gemini API

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Workflow

1. Upload meeting audio
2. Generate transcript using Whisper
3. Generate AI summary using Gemini
4. Extract action items
5. Export PDF report
6. Save meeting to SQLite database
7. View meeting history

---

## Future Improvements

* Speaker diarization
* Sentiment analysis
* Multi-language support
* Meeting search engine
* RAG-based meeting assistant
* Cloud deployment

---

## Author

Abhijit Vichare
