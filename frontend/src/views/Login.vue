<template>
  <div class="container auth-shell py-5">
    <div class="row justify-content-center w-100">
      <div class="col-md-6 col-lg-5">
        <div class="auth-card">
          <div class="auth-header">
            <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 52px;" />
            <div class="auth-title">Sign in</div>
            <div class="auth-subtitle">Welcome back to your weekly brief.</div>
          </div>
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <div class="input-icon">
                <Mail :size="18" class="icon-muted" />
                <input
                  v-model="email"
                  type="email"
                  placeholder="you@example.com"
                  autocomplete="email"
                  required
                />
              </div>
            </div>
            <div class="mb-4">
              <label class="form-label">Password</label>
              <div class="input-icon">
                <Lock :size="18" class="icon-muted" />
                <input
                  v-model="password"
                  type="password"
                  placeholder="••••••••"
                  autocomplete="current-password"
                  required
                />
              </div>
            </div>
            <div v-if="error" class="alert alert-danger d-flex align-items-center gap-2">
              <AlertCircle :size="18" />
              {{ error }}
            </div>
            <button type="submit" class="btn btn-primary w-100 btn-lg d-flex align-items-center justify-content-center gap-2" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              <LogIn v-else :size="18" />
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>
          <p class="text-center mt-3 auth-footer-link">
            <router-link to="/forgot-password" class="text-decoration-none auth-footer-link">
              Forgot password?
            </router-link>
          </p>
          <p class="text-center mt-4 text-muted">
            Don't have an account?
            <router-link to="/register" class="text-decoration-none">Register</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useDashboardStore } from '../stores/dashboard'
import { Mail, Lock, AlertCircle, LogIn } from 'lucide-vue-next'
import { useToast } from '@/utils/shareUtils'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const dashboardStore = useDashboardStore()
const { show } = useToast()

onMounted(() => {
  if (route.query?.reason === 'session-expired') {
    show('Session expired. Please sign in again.', 'error')
    router.replace({ query: {} })
  }
})

async function handleLogin() {
  error.value = ''
  loading.value = true
  
  // Clear any previous session data
  dashboardStore.clearCache()
  
  try {
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-footer-link {
  color: var(--warm-500);
}
</style>
