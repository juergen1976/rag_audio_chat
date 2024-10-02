<template>
  <div class="container mx-auto py-8 px-4 bg-dark text-gray">
    <h1 class="text-3xl font-bold mb-6 text-primary">Audio Recorder for AudioGPT</h1>

    <!-- Team and Topic selection -->
    <div class="mb-6 space-y-4">
      <div>
        <label for="team" class="block text-lg font-semibold mb-2 text-white">Select a team:</label>
        <select
          v-model="selectedTeam"
          @change="onTeamChange"
          class="block w-full p-2 border border-gray-500 bg-dark-light text-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
        >
          <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
        </select>
      </div>

      <div v-if="topics.length">
        <label for="topic" class="block text-lg font-semibold mb-2 text-white">Select a topic:</label>
        <select
          v-model="selectedTopic"
          class="block w-full p-2 border border-gray-500 bg-dark-light text-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
        >
          <option v-for="topic in topics" :key="topic.id" :value="topic.id">{{ topic.name }}</option>
        </select>
      </div>

      <div>
        <input
          v-model="recordingName"
          placeholder="Recording name"
          class="block w-full p-2 border border-gray-500 bg-dark-light text-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
        />
      </div>
    </div>

    <!-- Recording Controls -->
    <div class="mb-6">
      <button
        @click="startRecording"
        :disabled="isRecording"
        class="px-4 py-2 bg-primary text-white rounded-md shadow hover:bg-red-700 disabled:opacity-50"
      >
        Start Recording
      </button>
      <button
        @click="stopRecording"
        :disabled="!isRecording"
        class="ml-4 px-4 py-2 bg-red-600 text-white rounded-md shadow hover:bg-red-700 disabled:opacity-50"
      >
        Stop Recording
      </button>
    </div>

    <!-- Recording Preview and Save -->
    <div v-if="audioURL" class="mb-6">
      <h3 class="text-lg font-semibold mb-2 text-white">Preview</h3>
      <audio :src="audioURL" controls class="w-full mb-4 bg-dark-light"></audio>
      <button
        @click="saveRecording"
        class="px-4 py-2 bg-primary text-white rounded-md shadow hover:bg-red-700"
      >
        Save Recording
      </button>
    </div>

    <!-- Recordings Table -->
    <div>
      <h2 class="text-2xl font-bold mb-4 text-primary">Recordings of the Team</h2>
      <table class="min-w-full bg-dark-light rounded-md shadow-md text-white">
        <thead>
          <tr class="bg-dark text-left text-sm uppercase font-semibold text-gray">
            <th class="px-4 py-2 border-b border-gray-500">Recording name</th>
            <th class="px-4 py-2 border-b border-gray-500">Topic</th>
            <th class="px-4 py-2 border-b border-gray-500">Download</th>
              <th class="px-4 py-2 border-b border-gray-500">Transcription</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="recordings.length === 0">
            <td class="px-4 py-2 border-b border-gray-500" colspan="3">No recordings available for the team.</td>
          </tr>
          <tr v-for="recording in recordings" :key="recording.name" class="text-sm hover:bg-gray-700">
            <td class="px-4 py-2 border-b border-gray-500">{{ recording.name }}</td>
            <td class="px-4 py-2 border-b border-gray-500">{{ recording.topic }}</td>
             <td class="px-4 py-2 border-b border-gray-500">
                  <a
                    :href="`http://localhost:3005/recordings/file/${recording.id}`"
                    class="text-primary hover:underline"
                    download
                  >
                    Download
                  </a>
            </td>
             <td class="px-4 py-2 border-b border-gray-500 text-ellipsis text-wrap">{{ recording.transcribed_text }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      teams: [],
      topics: [],
      recordings: [],
      selectedTeam: null,
      selectedTopic: null,
      recordingName: '',
      mediaRecorder: null,
      audioChunks: [],
      audioURL: null,
      isRecording: false,
    };
  },
  methods: {
    async fetchTeams() {
      const response = await axios.get('http://localhost:3005/teams');
      this.teams = response.data;
    },
    async fetchTopics() {
      const response = await axios.get(`http://localhost:3005/topics/${this.selectedTeam}`);
      this.topics = response.data;
    },
    async fetchRecordings() {
      const response = await axios.get(`http://localhost:3005/recordings/${this.selectedTeam}`);
      this.recordings = response.data;
    },
    onTeamChange() {
      this.fetchTopics();
      this.fetchRecordings();
    },
    startRecording() {
      this.audioChunks = [];
      this.isRecording = true;
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = (event) => {
          this.audioChunks.push(event.data);
        };
        this.mediaRecorder.start();
      });
    },
    stopRecording() {
      this.mediaRecorder.stop();
      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        this.audioURL = URL.createObjectURL(audioBlob);
        this.isRecording = false;
      };
    },
    async saveRecording() {
      const formData = new FormData();
      const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
      formData.append('audio', audioBlob, `${this.recordingName}.wav`);
      formData.append('name', this.recordingName);
      formData.append('teamId', this.selectedTeam);
      formData.append('topicId', this.selectedTopic);

      await axios.post('http://localhost:3005/recordings', formData);
      alert('Recording saved successfully!');
      this.audioURL = null;
      this.recordingName = '';
      this.fetchRecordings();  // Refresh recordings
    },
  },
  created() {
    this.fetchTeams();
  },
};
</script>

<style>
/* Additional custom styles if needed */
</style>
