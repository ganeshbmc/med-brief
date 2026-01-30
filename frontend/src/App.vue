<template>
  <div id="app" class="app-shell">
    <a class="skip-link" href="#main-content">Skip to content</a>
    <nav class="navbar navbar-expand-lg navbar-warm py-3">
      <div class="container">
        <router-link class="navbar-brand d-flex align-items-center gap-2" :to="authStore.isAuthenticated ? '/dashboard' : '/'">
          <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 32px;" />
          <span class="brand-mark">MedBrief</span>
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
              <router-link class="nav-link nav-pill d-flex align-items-center gap-1" to="/dashboard">
                <LayoutDashboard :size="18" />
                <span>Dashboard</span>
              </router-link>
              <router-link class="nav-link nav-pill d-flex align-items-center gap-1" to="/profiles">
                <Users :size="18" />
                <span>Profiles</span>
              </router-link>
              <router-link class="nav-link nav-pill d-flex align-items-center gap-1" to="/preferences">
                <SlidersHorizontal :size="18" />
                <span>Preferences</span>
              </router-link>

              
              <!-- User Dropdown -->
              <div class="dropdown">
                <a 
                  class="nav-link dropdown-toggle nav-pill d-flex align-items-center gap-1" 
                  href="#" 
                  role="button" 
                  data-bs-toggle="dropdown" 
                  aria-expanded="false"
                >
                  <User :size="18" />
                  <span>{{ authStore.user?.full_name || authStore.user?.email?.split('@')[0] || 'Account' }}</span>
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li>
                    <router-link class="dropdown-item d-flex align-items-center gap-2" to="/account">
                      <Settings :size="16" />
                      Account Settings
                    </router-link>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item text-danger d-flex align-items-center gap-2" href="#" @click.prevent="handleLogout()">
                      <LogOut :size="16" />
                      Logout
                    </a>
                  </li>
                </ul>
              </div>
            </template>
            <template v-else>
              <div class="nav-auth-actions d-flex flex-column flex-lg-row align-items-center gap-2">
                <router-link class="btn btn-outline-terracotta btn-sm" to="/login">Login</router-link>
                <router-link class="btn btn-primary btn-sm" to="/register">Register</router-link>
              </div>
            </template>
          </div>
        </div>
      </div>
    </nav>
    <main id="main-content">
      <router-view />
    </main>
    <Toast />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useDashboardStore } from './stores/dashboard'
import { useRouter } from 'vue-router'
import { LayoutDashboard, Users, LogOut, Menu, User, Settings, SlidersHorizontal } from 'lucide-vue-next'
import Toast from '@/components/Toast.vue'

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
.brand-mark {
  font-family: var(--font-display);
  font-size: 1.2rem;
  letter-spacing: 0.02em;
}

main {
  padding: 1.5rem 0 3rem;
}

.skip-link {
  position: absolute;
  left: -999px;
  top: 8px;
  padding: 0.5rem 1rem;
  background: #FFFFFF;
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-2);
  z-index: 2000;
}

.skip-link:focus {
  left: 16px;
}

.navbar-toggler {
  border: none;
  padding: 0.5rem;
  color: var(--warm-700);
}

.navbar-toggler:focus {
  box-shadow: none;
}

.nav-auth-actions .btn {
  min-width: 120px;
  justify-content: center;
}

@media (max-width: 991.98px) {
  .nav-auth-actions {
    width: 100%;
  }

  .nav-auth-actions .btn {
    align-self: center;
  }
}
</style>
