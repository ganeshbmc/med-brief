<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card p-4">
          <div class="text-center mb-4">
            <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="mb-3" style="height: 48px; background-color: #ffffff; border-radius: 8px;" />
            <h2 class="fw-bold text-warm-dark">Reset Password</h2>
            <p class="text-muted">Enter your email to receive a reset link</p>
          </div>

          <form v-if="!sent" @submit.prevent="handleSubmit">
            <div class="mb-4">
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
            <h4 class="fw-bold text-warm-dark mb-3">Check Your Email</h4>
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