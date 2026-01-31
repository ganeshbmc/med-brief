<template>
  <div class="container auth-shell py-5">
    <div class="row justify-content-center w-100">
      <div class="col-md-6 col-lg-5">
        <div class="auth-card">
          <div class="auth-header">
            <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 52px;" />
            <div class="auth-title">Set a new password</div>
            <div class="auth-subtitle">Choose a strong password for your MedBrief account.</div>
          </div>

          <form v-if="!success" @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label">New Password</label>
              <div class="input-group input-group-pill">
                <span class="input-group-text">
                  <Lock :size="18" class="icon-muted" />
                </span>
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control"
                  placeholder="••••••••"
                  autocomplete="new-password"
                  required
                  minlength="8"
                />
                <button type="button" class="btn btn-outline-secondary" @click="showPassword = !showPassword" aria-label="Toggle password visibility">
                  <Eye :size="18" v-if="!showPassword" />
                  <EyeOff :size="18" v-else />
                </button>
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label">Confirm Password</label>
              <div class="input-group input-group-pill">
                <span class="input-group-text">
                  <Lock :size="18" class="icon-muted" />
                </span>
                <input
                  v-model="confirmPassword"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control"
                  placeholder="••••••••"
                  autocomplete="new-password"
                  required
                />
              </div>
              <small v-if="password && confirmPassword && password !== confirmPassword" class="text-danger">
                Passwords do not match
              </small>
            </div>

            <div v-if="error" class="alert alert-danger d-flex align-items-center gap-2">
              <AlertCircle :size="18" />
              {{ error }}
            </div>

            <button
              type="submit"
              class="btn btn-primary w-100 btn-lg d-flex align-items-center justify-content-center gap-2"
              :disabled="loading || password !== confirmPassword"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              <Lock :size="18" v-else />
              {{ loading ? 'Resetting...' : 'Reset Password' }}
            </button>
          </form>

          <div v-else class="text-center">
            <div class="mb-4">
              <CheckCircle :size="48" class="text-success" />
            </div>
            <h4 class="fw-bold text-warm-dark mb-3">Password reset</h4>
            <p class="text-muted mb-4">
              Your password has been reset successfully.
            </p>
            <router-link to="/login" class="btn btn-primary btn-lg">
              Sign In
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Lock, Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-vue-next'
import { resetPassword } from '../services/api'

const route = useRoute()
const router = useRouter()

const token = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const error = ref('')
const loading = ref(false)
const success = ref(false)

onMounted(() => {
  token.value = route.query.token
  if (!token.value) {
    error.value = 'Reset token is missing. Please use the link from your email.'
  }
})

async function handleSubmit() {
  error.value = ''
  loading.value = true

  try {
    await resetPassword(token.value, password.value)
    success.value = true
  } catch (e) {
    error.value = e.message || 'Failed to reset password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped></style>
