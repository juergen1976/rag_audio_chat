# Procedure

# 1. Get from the Postgres database all teams and topics
# 2. For each team and topic, get all the audio files
# 3. Use whisper to transcribe the audio files and store the text beside the upload audio file with the same name
# 4. Check if the collection "team_topic" exists as collection in Chroma vector database
# 5. If it does not exist, create the collection "team_topic" in Chroma vector database
# 6. Store the transcribed text in the collection "team_topic" in Chroma vector database
