<template>
  <div class="min-h-screen bg-dark text-gray flex flex-col">
    <header class="bg-dark-light p-4 shadow-lg">
      <nav class="container mx-auto flex justify-between items-center">
        <div>
          <router-link to="/" class="text-primary text-2xl font-bold hover:text-red-700">Alexander Bürkle Audio Chat</router-link>
        </div>
        <div>
          <router-link to="/" class="text-gray mx-4 hover:text-white">Recorder</router-link>
          <router-link to="/admin" class="text-gray mx-4 hover:text-white">Admin</router-link>
        </div>
      </nav>
    </header>
    <main class="flex-grow container mx-auto py-8 px-4">
      <router-view></router-view>
    </main>
    <footer class="bg-dark-light p-4 text-center text-gray">
      © 2024 AB Chat Audio App von Alexander Bürkle
    </footer>
  </div>
</template>

<style>
/* Custom styles for App.vue can be added here */
</style>
