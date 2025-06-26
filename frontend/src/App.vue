<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div>
    <header class="bg-light p-3 mb-4">
      <nav>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
        <RouterLink to="/admin">Admin</RouterLink>
        <RouterLink to="/dashboard">User</RouterLink>
      </nav>
    </header>

    <main class="container">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
header {
  border-bottom: 1px solid #ccc;
}

nav {
  display: flex;
  gap: 1rem;
  font-size: 1rem;
}

nav a {
  text-decoration: none;
  color: #007bff;
  font-weight: 500;
}

nav a.router-link-exact-active {
  font-weight: bold;
  color: #0056b3;
}
</style>

