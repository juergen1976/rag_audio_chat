<template>
  <div class="min-h-screen bg-dark text-gray flex flex-col">
    <header class="bg-dark-light p-4 shadow-lg">
      <nav class="container mx-auto flex justify-between items-center">
        <div>
          <router-link to="/" class="text-primary text-2xl font-bold hover:text-red-700">Alexander Bürkle AudioGPT</router-link>
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
          <h1 class="text-4xl font-bold mb-4">Willkommen bei AudioGPT</h1>
          <p class="text-lg">
            In diesem Portal können Sie Wissen per Mikrofon aufnehmen, so das es in der internen Datenbank als Text abgespeichert wird.
            Hierzu wird eine interne KI benuzt, die ihre Sprachaufnahme in Text umwandelt.
            Im Rechenzentrum werden die Aufnahmen der KI zur Verfügung gestellt, so das ihr Team später mittels AlexGPT darauf zugreifen kann und
            auf dem gespeicherten Wissen Fragen stellen kann.
            Erstellen Sie für Ihr Team ein neues Team und ein neues Thema und fangen Sie an Wissen zu speichern.
          </p>
        </div>

        <!-- Image Section -->
        <div class="flex justify-center md:justify-start">
          <img src="./assets/ai_bot.jpg" alt="Placeholder Image" class="rounded-lg shadow-lg">
        </div>

      </div>
    </div>

    <main class="flex-grow container mx-auto py-8 px-4">
      <router-view></router-view>
    </main>
    <footer class="bg-dark-light p-4 text-center text-gray">
      © 2024 AudioGPT von Alexander Bürkle
    </footer>
  </div>
</template>

<style>
/* Custom styles for App.vue can be added here */
</style>
