<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card p-4">
          <h2 class="text-center mb-4 fw-bold">Create Account</h2>
          <form @submit.prevent="handleRegister">
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
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input
                v-model="password"
                type="password"
                class="form-control form-control-lg"
                placeholder="••••••••"
                required
                minlength="8"
              />
            </div>
            <div class="mb-4">
              <label class="form-label">Confirm Password</label>
              <input
                v-model="confirmPassword"
                type="password"
                class="form-control form-control-lg"
                placeholder="••••••••"
                required
              />
            </div>
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <button type="submit" class="btn btn-primary w-100 btn-lg" :disabled="loading">
              {{ loading ? 'Creating Account...' : 'Create Account' }}
            </button>
          </form>
          <p class="text-center mt-4 text-muted">
            Already have an account?
            <router-link to="/login" class="text-decoration-none">Sign In</router-link>
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
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const authStore = useAuthStore()

async function handleRegister() {
  error.value = ''
  
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  
  loading.value = true
  try {
    await authStore.register(email.value, password.value)
    router.push('/onboarding')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
