<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card p-4">
          <h2 class="text-center mb-4 fw-bold">Sign In</h2>
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input
                v-model="email"
                type="email"
                class="form-control form-control-lg"
                placeholder="you@example.com"
                required
              />
            </div>
            <div class="mb-4">
              <label class="form-label">Password</label>
              <input
                v-model="password"
                type="password"
                class="form-control form-control-lg"
                placeholder="••••••••"
                required
              />
            </div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <button type="submit" class="btn btn-primary w-100 btn-lg" :disabled="loading">
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const authStore = useAuthStore()

async function handleLogin() {
  error.value = ''
  loading.value = true
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
