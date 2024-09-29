# Procedure
import chromadb
import psycopg2
import whisper
from babel.numbers import get_currency_name
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from chromadb.utils import embedding_functions
from langchain.embeddings import SentenceTransformerEmbeddings

from AB_AudioChat.database import AudioChatDatabase

class AudioIndexer:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="llama3")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
        self.audio_database = AudioChatDatabase()

    def get_text_from_whisper(self, audio_file_path: str) -> str:
        model = whisper.load_model("medium")
        result = model.transcribe(audio_file_path)
        return result["text"]

    def store_recording_in_chroma(self, collection_name: str, recording_text: str, recording_id: int):
        # https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/


        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"),
            #embedding_function=self.embeddings,
            persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not neccesary
        )

        document = Document(
            page_content=recording_text,
            #metadata={"source": "voice"},
            id=recording_id,
        )
        chunks = self.text_splitter.split_documents([document])
        vector_store.add_documents(chunks)

    def get_collection_name(self, team_name, topic) -> str:
        return f"{team_name[0:2]}_{topic}"


if __name__ == "__main__":
    audio_indexer = AudioIndexer()
    # 1. Get from the Postgres database all teams and topics
    teams = audio_indexer.audio_database.get_teams()
    for team in teams:
        team_id = team[0]
        team_name = team[1]
        topics = audio_indexer.audio_database.get_topics_for__team_id(team_id)
        for topic in topics:
            recordings = audio_indexer.audio_database.get_recordings_for_topic_id(topic[0])
            for recording in recordings:
                # if the recording is already transcribed, skip it
                if recording[5]:
                    continue
                print(f"Processing recording: {recording[1]} for topic {topic[1]}")
                # Transcribe the audio file with the whisper model
                audio_file_path = recording[2]
                text = audio_indexer.get_text_from_whisper(audio_file_path)
                print("Transcribed text: ", text)
                # Store the transcribed text in the Chroma vector database
                audio_indexer.store_recording_in_chroma(collection_name=f"{audio_indexer.get_collection_name(team_name, topic[1])}", recording_text=text, recording_id=recording[0])
                # mark the recording as transcribed and save it in the database
                audio_indexer.audio_database.mark_recording_as_transcribed(recording[0])
                audio_indexer.audio_database.set_transcribed_text(recording[0], text)