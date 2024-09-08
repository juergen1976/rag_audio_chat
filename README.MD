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
## Backend
```bash
cd backend
npm install
node server.js
```

# Links
- https://www.baeldung.com/ops/postgresql-docker-setup