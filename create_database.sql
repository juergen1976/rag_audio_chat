CREATE DATABASE ab_audio;

CREATE TABLE teams (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE topics (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  team_id INTEGER REFERENCES teams(id)
);

CREATE TABLE recordings (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  file_path VARCHAR(255),
  team_id INTEGER REFERENCES teams(id),
  topic_id INTEGER REFERENCES topics(id),
  is_transcribed BOOLEAN DEFAULT FALSE,
  transcribed_text TEXT
);

ALTER TABLE recordings
ADD transcribed_text TEXT;