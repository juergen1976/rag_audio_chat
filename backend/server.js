const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');
const cors = require('cors');
const { Pool } = require('pg');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());
app.use(cors());

// PostgreSQL Pool Setup
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'ab_audio',
  password: 'postgres',
  port: 5432,
});

// Set up storage for audio files using multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadPath)) {
      fs.mkdirSync(uploadPath);
    }
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});
const upload = multer({ storage });

// API Endpoints

// Create a new team
app.post('/teams', async (req, res) => {
  const { name } = req.body;
  try {
    const result = await pool.query('INSERT INTO teams (name) VALUES ($1) RETURNING *', [name]);
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Create a new topic for a team
app.post('/topics', async (req, res) => {
  const { name, teamId } = req.body;
  try {
    const result = await pool.query('INSERT INTO topics (name, team_id) VALUES ($1, $2) RETURNING *', [name, teamId]);
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Fetch all teams with topics
app.get('/teams', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM teams');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Fetch topics by team ID
app.get('/topics/:teamId', async (req, res) => {
  const { teamId } = req.params;
  try {
    const result = await pool.query('SELECT * FROM topics WHERE team_id = $1', [teamId]);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Store a new recording
app.post('/recordings', upload.single('audio'), async (req, res) => {
  const { name, teamId, topicId } = req.body;
  const filePath = req.file.path;

  try {
    const result = await pool.query(
      'INSERT INTO recordings (name, file_path, team_id, topic_id) VALUES ($1, $2, $3, $4) RETURNING *',
      [name, filePath, teamId, topicId]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Fetch recordings for a specific team
app.get('/recordings/:teamId', async (req, res) => {
  const teamId = req.params.teamId;
  const result = await pool.query(
    `SELECT recordings.id, recordings.name, topics.name AS topic 
     FROM recordings 
     JOIN topics ON recordings.topic_id = topics.id 
     WHERE recordings.team_id = $1`,
    [teamId]
  );
  res.json(result.rows);
});

// Endpoint to get teams with their topics
app.get('/teams/topics', async (req, res) => {
  try {
    const query = `
      SELECT t.id AS team_id, t.name AS team_name, tp.id AS topic_id, tp.name AS topic_name, r.id AS recording_id, r.name AS recording_name, r.file_path
      FROM teams t
      LEFT JOIN topics tp ON t.id = tp.team_id
      LEFT JOIN recordings r ON tp.id = r.topic_id
      ORDER BY t.name;
    `;

    const result = await pool.query(query);

    // Structure the data into teams with topics and recordings
    const teamsMap = {};

    result.rows.forEach(row => {
      if (!teamsMap[row.team_id]) {
        teamsMap[row.team_id] = {
          id: row.team_id,
          name: row.team_name,
          topics: [],
        };
      }

      let topic = teamsMap[row.team_id].topics.find(t => t.id === row.topic_id);
      if (!topic) {
        topic = {
          id: row.topic_id,
          name: row.topic_name,
          recordings: [],
        };
        teamsMap[row.team_id].topics.push(topic);
      }

      if (row.recording_id) {
        topic.recordings.push({
          id: row.recording_id,
          name: row.recording_name,
          file_path: row.file_path,
        });
      }
    });

    const teamsWithTopics = Object.values(teamsMap);

    res.json(teamsWithTopics);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

app.get('/teams/:teamId/topics', async (req, res) => {
  const { teamId } = req.params;

  try {
    const query = `
      SELECT t.id AS team_id, tp.id AS topic_id, tp.name AS topic_name, r.id AS recording_id, r.name AS recording_name, r.file_path
      FROM topics tp
      LEFT JOIN recordings r ON tp.id = r.topic_id
      JOIN teams t ON t.id = tp.team_id
      WHERE t.id = $1
      ORDER BY tp.name;
    `;

    const result = await pool.query(query, [teamId]);

    const topicsMap = {};

    result.rows.forEach(row => {
      if (!topicsMap[row.topic_id]) {
        topicsMap[row.topic_id] = {
          id: row.topic_id,
          name: row.topic_name,
          recordings: [],
        };
      }

      if (row.recording_id) {
        topicsMap[row.topic_id].recordings.push({
          id: row.recording_id,
          name: row.recording_name,
          file_path: row.file_path,
        });
      }
    });

    const topicsWithRecordings = Object.values(topicsMap);

    res.json(topicsWithRecordings);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

// Serve audio files
app.get('/uploads/:filename', (req, res) => {
  const filePath = path.join(__dirname, 'uploads', req.params.filename);
  res.sendFile(filePath);
});

// Endpoint to download the recording
app.get('/recordings/file/:id', (req, res) => {

  // Load recording from the database
    pool.query('SELECT * FROM recordings WHERE id = $1', [req.params.id], (err, result) => {
        if (err) {
        console.error('Error fetching recording:', err);
        return res.status(500).send('Error fetching recording');
        }

        if (result.rows.length === 0) {
        return res.status(404).send('Recording not found');
        }

        const recording = result.rows[0];
        const filePath = recording.file_path;
        console.log('File path:', filePath);

        res.download(filePath, err => {
        if (err) {
            console.error('Error sending file:', err);
            res.status(500).send('Error downloading file');
        }
        });
    });

});

app.listen(3005, () => {
  console.log('Server is running on port 3005');
});
