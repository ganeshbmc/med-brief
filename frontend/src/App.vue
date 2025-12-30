<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-warm">
      <div class="container">
        <router-link class="navbar-brand d-flex align-items-center" :to="authStore.isAuthenticated ? '/dashboard' : '/'">
          <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="me-2" style="height: 28px;" />
          <span>MedBrief</span>
        </router-link>
        
        <!-- Hamburger Toggle Button -->
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <Menu :size="24" />
        </button>
        
        <!-- Collapsible Nav Content -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <div class="navbar-nav ms-auto d-flex align-items-lg-center gap-2">
            <template v-if="authStore.isAuthenticated">
              <router-link class="nav-link d-flex align-items-center gap-1" to="/dashboard">
                <LayoutDashboard :size="18" />
                <span>Dashboard</span>
              </router-link>
              <router-link class="nav-link d-flex align-items-center gap-1" to="/profiles">
                <Users :size="18" />
                <span>Profiles</span>
              </router-link>
              <a class="nav-link d-flex align-items-center gap-1" href="#" @click.prevent="handleLogout()">
                <LogOut :size="18" />
                <span>Logout</span>
              </a>
            </template>
            <template v-else>
              <router-link class="nav-link" to="/login">Login</router-link>
              <router-link class="btn btn-primary btn-sm" to="/register">Register</router-link>
            </template>
          </div>
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
import { useDashboardStore } from './stores/dashboard'
import { useRouter } from 'vue-router'
import { LayoutDashboard, Users, LogOut, Menu } from 'lucide-vue-next'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const router = useRouter()

function handleLogout() {
    authStore.logout()
    dashboardStore.clearCache()
    router.push('/login')
}
</script>

<style>
#app {
  min-height: 100vh;
  background-color: var(--cream-50);
}
main {
  padding: 2rem 0;
}

/* Custom hamburger styling */
.navbar-toggler {
  border: none;
  padding: 0.5rem;
  color: var(--warm-700);
}

.navbar-toggler:focus {
  box-shadow: none;
}
</style>
