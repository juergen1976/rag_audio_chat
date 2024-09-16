# Procedure
import chromadb
import psycopg2
import whisper
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class AudioInderxer:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="llama3")
        self.chroma_client = chromadb.Client()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)

    def connect_to_postgres(self):
        try:
            conn = psycopg2.connect(
                dbname="ab_audio",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432")
            return conn
        except Exception as e:
            print("Error connecting to the database: ", e)
            return None

    def get_teams(self):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM teams")
        teams = cur.fetchall()
        return teams

    def get_topics_for__team_id(self, team_id: int):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM topics WHERE team_id = %s", (team_id,))
        topics = cur.fetchall()
        return topics

    def get_recordings_for_topic_id(self, topic_id: int):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM recordings WHERE topic_id = %s", (topic_id,))
        recordings = cur.fetchall()
        return recordings

    def get_text_from_whisper(self, audio_file_path: str) -> str:
        model = whisper.load_model("medium")

    def does_collection_exists_in_chroma(collection_name: str) -> bool:
        # Check if the collection exists in the Chroma vector database
        pass

    def connect_to_postgres(self):
        try:
            conn = psycopg2.connect(
                dbname="ab_audio",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432")
            return conn
        except Exception as e:
            print("Error connecting to the database: ", e)
            return None

    def get_teams(self):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM teams")
        teams = cur.fetchall()
        return teams

    def get_topics_for__team_id(self, team_id: int):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM topics WHERE team_id = %s", (team_id,))
        topics = cur.fetchall()
        return topics

    def get_recordings_for_topic_id(self, topic_id: int):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("SELECT * FROM recordings WHERE topic_id = %s", (topic_id,))
        recordings = cur.fetchall()
        return recordings

    def get_text_from_whisper(self, audio_file_path: str) -> str:
        model = whisper.load_model("medium")
        result = model.transcribe(audio_file_path)
        return result["text"]

    def store_recording_in_chroma(self, collection_name: str, recording_text: str, recording_id: int):
        # https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not neccesary
        )

        document = Document(
            page_content=recording_text,
            #metadata={"source": "voice"},
            id=recording_id,
        )
        chunks = self.text_splitter.split_documents([document])
        vector_store.add_documents(chunks)

if __name__ == "__main__":
    audio_indexer = AudioInderxer()
    # 1. Get from the Postgres database all teams and topics
    teams = audio_indexer.get_teams()
    for team in teams:
        team_id = team[0]
        team_name = team[1]
        topics = audio_indexer.get_topics_for__team_id(team_id)
        for topic in topics:
            recordings = audio_indexer.get_recordings_for_topic_id(topic[0])
            for recording in recordings:
                print(f"Processing recording: {recording[1]} for topic {topic[1]}")
                # Transcribe the audio file with the whisper model
                audio_file_path = recording[2]
                text = audio_indexer.get_text_from_whisper(audio_file_path)
                print("Transcribed text: ", text)
                # Store the transcribed text in the Chroma vector database
                audio_indexer.store_recording_in_chroma(collection_name=f"{team_name}_{topic[1]}", recording_text=text, recording_id=recording[0])



    # 4. Check if the collection "team_topic" exists as collection in Chroma vector database
    # 5. If it does not exist, create the collection "team_topic" in Chroma vector database
    # 6. Store the transcribed text in the collection "team_topic" in Chroma vector database