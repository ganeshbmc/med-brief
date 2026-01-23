<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card p-4">
          <div class="text-center mb-4">
            <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="mb-3" style="height: 48px; background-color: rgba(255, 255, 255, 0.9); border-radius: 8px;" />
            <h2 class="fw-bold text-warm-dark">Create Account</h2>
            <p class="text-muted">Join MedBrief for personalized research briefs</p>
          </div>
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <div class="input-group">
                <span class="input-group-text bg-white">
                  <Mail :size="18" class="icon-muted" />
                </span>
                <input
                  v-model="email"
                  type="email"
                  class="form-control form-control-lg"
                  placeholder="you@example.com"
                  required
                />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <div class="input-group">
                <span class="input-group-text bg-white">
                  <Lock :size="18" class="icon-muted" />
                </span>
                <input
                  v-model="password"
                  type="password"
                  class="form-control form-control-lg"
                  placeholder="••••••••"
                  required
                  minlength="8"
                />
              </div>
            </div>
            <div class="mb-4">
              <label class="form-label">Confirm Password</label>
              <div class="input-group">
                <span class="input-group-text bg-white">
                  <Lock :size="18" class="icon-muted" />
                </span>
                <input
                  v-model="confirmPassword"
                  type="password"
                  class="form-control form-control-lg"
                  placeholder="••••••••"
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

<style scoped>
.input-group-text {
  border-color: var(--warm-200);
  border-right: none;
}

.input-group .form-control {
  border-left: none;
}

.input-group .form-control:focus {
  border-color: var(--warm-200);
  box-shadow: none;
}

.input-group:focus-within {
  box-shadow: 0 0 0 0.2rem var(--terracotta-100);
  border-radius: 0.375rem;
}

.input-group:focus-within .input-group-text,
.input-group:focus-within .form-control {
  border-color: var(--terracotta-500);
}
</style>
