from AB_AudioChat.database import AudioChatDatabase


# 1. Read the teams and topics from the postgres database
audio_database = AudioChatDatabase()
teams = audio_database.get_teams()
print(teams)


# 2. Show the Team and topics in the UI as section boxes
# 3. Use RAG with the "team_topic" as the collection name

