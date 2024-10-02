<template>
  <div class="min-h-screen bg-dark text-gray flex flex-col">
    <header class="bg-dark-light p-4 shadow-lg">
      <nav class="container mx-auto flex justify-between items-center">
        <div>
          <router-link to="/" class="text-primary text-2xl font-bold hover:text-red-700">Your company AudioGPT</router-link>
        </div>
        <div>
          <router-link to="/" class="text-gray mx-4 hover:text-white">Recorder</router-link>
          <router-link to="/admin" class="text-gray mx-4 hover:text-white">Admin</router-link>
        </div>
      </nav>
    </header>

      <!-- Banner Section -->
    <div class="text-white py-12 px-6">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 items-center">

        <!-- Text Section -->
        <div class="text-right">
          <h1 class="text-4xl font-bold mb-4">Welcome at AudioGPT</h1>
          <p class="text-lg">
            In this portal you can record knowledge via microphone so that it is stored in the internal database as text.
            An internal AI is used for this purpose, which converts your voice recording into text.
            The recordings are made available to the AI in the data center so that your team can access them later using AudioGPT and ask questions based on the stored knowledge.
            can ask questions based on the stored knowledge.
            Create a new team and a new topic for your team and start saving knowledge.
          </p>
        </div>

        <!-- Image Section -->
        <div class="flex justify-center md:justify-start">
          <img src="./assets/ai_bot.jpg" alt="Placeholder Image" class="rounded-lg shadow-lg" width="300">
        </div>

      </div>
    </div>

    <main class="flex-grow container mx-auto py-8 px-4">
      <router-view></router-view>
    </main>
    <footer class="bg-dark-light p-4 text-center text-gray">
      © 2024 AudioGPT von YourCompany
    </footer>
  </div>
</template>

<style>
/* Custom styles for App.vue can be added here */
</style>
