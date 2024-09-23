import psycopg2

class AudioChatDatabase():

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

    def mark_recording_as_transcribed(self, recording_id: int):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("UPDATE recordings SET is_transcribed = true WHERE id = %s", (recording_id,))
        conn.commit()
        return True

    def set_transcribed_text(self, recording_id: int, text: str):
        conn = self.connect_to_postgres()
        if conn is None:
            return None
        cur = conn.cursor()
        cur.execute("UPDATE recordings SET transcribed_text = %s WHERE id = %s", (text, recording_id))
        conn.commit()