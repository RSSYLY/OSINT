<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="bg-gray-800 text-white p-4">
      <div class="container mx-auto flex justify-between items-center">
        <div class="text-2xl font-bold">Your Logo</div>
        <nav class="space-x-4">
          <a href="#" class="hover:text-gray-400">Home</a>
          <a href="#" class="hover:text-gray-400">About</a>
          <a href="#" class="hover:text-gray-400">Contact</a>
        </nav>
      </div>
    </div>

  </header>
  <RouterView />
</template>

<style scoped>
</style>