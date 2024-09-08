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
  topic_id INTEGER REFERENCES topics(id)
);