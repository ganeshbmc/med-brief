<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/">
          <span class="me-2">📚</span>MedBrief
        </router-link>
        <div class="navbar-nav ms-auto">
          <template v-if="authStore.isAuthenticated">
            <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
            <router-link class="nav-link" to="/profiles">Profiles</router-link>
            <a class="nav-link" href="#" @click.prevent="authStore.logout()">Logout</a>
          </template>
          <template v-else>
            <router-link class="nav-link" to="/login">Login</router-link>
            <router-link class="nav-link" to="/register">Register</router-link>
          </template>
        </div>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
</script>

<style>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
main {
  padding: 2rem 0;
}
</style>
