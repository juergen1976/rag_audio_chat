# Audio GPT

![Alt text](./web/audio-recorder-app/src/assets/ai_bot.jpg)

# Idea
* Recording voice with Vud.js app and save the audio file to the server.

# Tech Stack
- Postgres
- Vue.js app to record the audio and manage the teams and topics
- Express backend to save the audio files and manage the teams and topics
- Whisper for transcribing the recorded audio

# Setup
## Docker Postgres
```bash
docker pull postgres
docker run --name postgres -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 -v ./data:/var/lib/postgresql/data postgres
```

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
serve -s dist
```


## Backend
```bash
cd backend
npm install
node server.js
```