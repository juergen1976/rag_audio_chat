# Audio GPT

![Alt text](./web/audio-recorder-app/src/assets/ai_bot.jpg)

# Idea
* Recording voice with Vue.js app and save the audio file to the server.
* Transcribe the audio file with Whisper
* Provide a chatbot using the transcribed text with RAG

# Tech Stack
- Postgres to store Metadata
- Vue.js app to record the audio and manage the teams and topics
- Express backend to save the audio files and manage the teams and topics
- Whisper for transcribing the recorded audio
- Ollama for deploying LLama
- Streamlit for the UI
- Langchain and Chroma for RAG

# Setup
## Docker Postgres
```bash
docker pull postgres
docker run --name postgres -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 -v ./data:/var/lib/postgresql/data postgres
```
## Web
- Install Node.js

# Usage

## Frontend Dev
```bash
cd web/audio-recorder-app
npm install
npm run serve
```

## Frontend Prod
```bash
cd web/audio-recorder-app
npm install
npm run build
npm install -g serve
serve -l portnr -s dist
```

## Backend
```bash
cd backend
npm install
node server.js
```