<template>
  <div class="container auth-shell py-5">
    <div class="row justify-content-center w-100">
      <div class="col-md-6 col-lg-5">
        <div class="auth-card">
          <div class="auth-header">
            <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 52px;" />
            <div class="auth-title">Create account</div>
            <div class="auth-subtitle">Start your personalized weekly research brief.</div>
          </div>
          <form @submit.prevent="handleRegister">
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
            <div class="mb-3">
              <label class="form-label">Password</label>
              <div class="input-icon">
                <Lock :size="18" class="icon-muted" />
                <input
                  v-model="password"
                  type="password"
                  placeholder="••••••••"
                  autocomplete="new-password"
                  required
                  minlength="8"
                />
              </div>
            </div>
            <div class="mb-4">
              <label class="form-label">Confirm Password</label>
              <div class="input-icon">
                <Lock :size="18" class="icon-muted" />
                <input
                  v-model="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  autocomplete="new-password"
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
              <UserPlus v-else :size="18" />
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
import { Mail, Lock, AlertCircle, UserPlus } from 'lucide-vue-next'

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

<style scoped></style>
