<template>
  <div class="container mx-auto py-8 px-4 bg-dark text-gray">
    <h1 class="text-3xl font-bold mb-6 text-primary">Administration</h1>

    <!-- Create Team -->
    <div class="mb-8 space-y-4">
      <h2 class="text-2xl font-bold mb-4 text-white">Neues Team anlegen</h2>
      <div>
        <input
          v-model="newTeamName"
          placeholder="Team Name"
          class="block w-full p-2 border border-gray-500 bg-dark-light text-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
        />
      </div>
      <button
        @click="createTeam"
        class="px-4 py-2 bg-primary text-white rounded-md shadow hover:bg-red-700"
      >
        Team anlegen
      </button>
    </div>

    <!-- Create Topic -->
    <div class="mb-8 space-y-4">
      <h2 class="text-2xl font-bold mb-4 text-white">Neues Thema anlegen</h2>
      <div>
        <label class="block text-lg font-semibold mb-2 text-white">Team auswählen:</label>
        <select
          v-model="selectedTeam"
          class="block w-full p-2 border border-gray-500 bg-dark-light text-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
        >
          <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
        </select>
      </div>
      <div>
        <input
            v-model="newTopicName"
            placeholder="Thema"
            class="block w-full p-2 border border-gray-500 bg-dark-light text-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
        />
      </div>
      <button
          @click="createTopic"
          class="px-4 py-2 bg-primary text-white rounded-md shadow hover:bg-red-700"
      >
        Thema anlegen
      </button>
    </div>

    <!-- Teams and Topics Table -->
    <div>
      <h2 class="text-2xl font-bold mb-4 text-primary">Teams und Themen</h2>
      <table class="min-w-full bg-dark-light rounded-md shadow-md text-white">
        <thead>
        <tr class="bg-dark text-left text-sm uppercase font-semibold text-gray">
          <th class="px-4 py-2 border-b border-gray-500">Team</th>
          <th class="px-4 py-2 border-b border-gray-500">Thema</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="team in teamsWithTopics" :key="team.id" class="text-sm hover:bg-gray-700">
          <td class="px-4 py-2 border-b border-gray-500">{{ team.name }}</td>
          <td class="px-4 py-2 border-b border-gray-500">
            <ul>
              <li v-for="topic in team.topics" :key="topic.id">{{ topic.name }}</li>
            </ul>
          </td>
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
      newTeamName: '',
      newTopicName: '',
      selectedTeam: null,
      teams: [],
      teamsWithTopics: [],
    };
  },
  methods: {
    async fetchTeams() {
      const response = await axios.get('http://localhost:3005/teams');
      this.teams = response.data;
      this.fetchTeamsWithTopics();
    },
    async fetchTeamsWithTopics() {
      const response = await axios.get('http://localhost:3005/teams/topics');
      this.teamsWithTopics = response.data;
    },
    async createTeam() {
      await axios.post('http://localhost:3005/teams', {name: this.newTeamName});
      this.newTeamName = '';
      this.fetchTeams();  // Refresh teams
    },
    async createTopic() {
      await axios.post('http://localhost:3005/topics', {name: this.newTopicName, teamId: this.selectedTeam});
      this.newTopicName = '';
      this.fetchTeamsWithTopics();  // Refresh topics
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
