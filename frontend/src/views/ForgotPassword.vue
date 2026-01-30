<template>
  <div class="container auth-shell py-5">
    <div class="row justify-content-center w-100">
      <div class="col-md-6 col-lg-5">
        <div class="auth-card">
          <div class="auth-header">
            <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 52px;" />
            <div class="auth-title">Reset password</div>
            <div class="auth-subtitle">We'll send a reset link to your inbox.</div>
          </div>

          <form v-if="!sent" @submit.prevent="handleSubmit">
            <div class="mb-4">
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

            <div v-if="error" class="alert alert-danger d-flex align-items-center gap-2">
              <AlertCircle :size="18" />
              {{ error }}
            </div>

            <button type="submit" class="btn btn-primary w-100 btn-lg d-flex align-items-center justify-content-center gap-2" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              <Mail :size="18" v-else />
              {{ loading ? 'Sending...' : 'Send Reset Link' }}
            </button>
          </form>

          <div v-else class="text-center">
            <div class="mb-4">
              <CheckCircle :size="48" class="text-success" />
            </div>
            <h4 class="fw-bold text-warm-dark mb-3">Check your email</h4>
            <p class="text-muted mb-4">
              If an account exists for <strong>{{ email }}</strong>, we've sent password reset instructions.
            </p>
            <p class="text-muted small mb-4">
              Didn't receive the email? Check your spam folder or try again.
            </p>
            <router-link to="/login" class="btn btn-outline-terracotta">
              Back to Login
            </router-link>
          </div>

          <p class="text-center mt-4 text-muted">
            Remember your password?
            <router-link to="/login" class="text-decoration-none">Sign In</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Mail, AlertCircle, CheckCircle } from 'lucide-vue-next'
import { requestPasswordReset } from '../services/api'

const email = ref('')
const error = ref('')
const loading = ref(false)
const sent = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true

  try {
    await requestPasswordReset(email.value)
    sent.value = true
  } catch (e) {
    error.value = e.message || 'Failed to send reset email'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped></style>
