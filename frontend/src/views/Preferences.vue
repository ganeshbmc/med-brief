<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card p-4">
          <div class="d-flex align-items-center gap-3 mb-4">
            <router-link to="/account" class="text-muted">
              <ArrowLeft :size="20" />
            </router-link>
            <h2 class="fw-bold text-warm-dark mb-0">User Preferences</h2>
          </div>

          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border"></div>
          </div>

          <form v-else @submit.prevent="handleSave">
            <div class="mb-4">
              <label class="form-label fw-semibold">Font Size</label>
              <div class="btn-group w-100" role="group">
                <input type="radio" class="btn-check" id="fs-small" value="small" v-model="prefs.fontSize">
                <label class="btn btn-outline-secondary" for="fs-small">Small</label>
                
                <input type="radio" class="btn-check" id="fs-medium" value="medium" v-model="prefs.fontSize">
                <label class="btn btn-outline-secondary" for="fs-medium">Medium</label>
                
                <input type="radio" class="btn-check" id="fs-large" value="large" v-model="prefs.fontSize">
                <label class="btn btn-outline-secondary" for="fs-large">Large</label>
              </div>
              <div class="form-text text-muted mt-1">
                Choose your preferred reading font size
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold">Line Spacing</label>
              <div class="btn-group w-100" role="group">
                <input type="radio" class="btn-check" id="ls-normal" value="normal" v-model="prefs.lineSpacing">
                <label class="btn btn-outline-secondary" for="ls-normal">Normal</label>
                
                <input type="radio" class="btn-check" id="ls-relaxed" value="relaxed" v-model="prefs.lineSpacing">
                <label class="btn btn-outline-secondary" for="ls-relaxed">Relaxed</label>
              </div>
              <div class="form-text text-muted mt-1">
                Normal (1.5) or Relaxed (1.8) line height
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold">Default Date Range</label>
              <select class="form-select" v-model="prefs.defaultDays">
                <option :value="3">Last 3 days</option>
                <option :value="7">Last 7 days (Weekly)</option>
                <option :value="14">Last 14 days (Fortnightly)</option>
                <option :value="30">Last 30 days (Monthly)</option>
              </select>
              <div class="form-text text-muted mt-1">
                Default time period when generating new briefs
              </div>
            </div>

            <div class="d-flex gap-2" v-if="!saved">
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                {{ saving ? 'Saving...' : 'Save Preferences' }}
              </button>
              <router-link to="/account" class="btn btn-outline-secondary">Cancel</router-link>
            </div>

            <div v-if="saved" class="d-flex gap-2 flex-wrap">
              <router-link to="/account" class="btn btn-primary d-flex align-items-center gap-2">
                <ArrowLeft :size="18" />
                Back to Account Settings
              </router-link>
              <router-link to="/dashboard" class="btn btn-outline-secondary d-flex align-items-center gap-2">
                <LayoutDashboard :size="18" />
                Go to Dashboard
              </router-link>
            </div>

            <div v-if="message" :class="['alert mt-3 d-flex align-items-center gap-2', isError ? 'alert-danger' : 'alert-success']">
              <Check v-if="!isError" :size="18" />
              <AlertCircle v-else :size="18" />
              {{ message }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { ArrowLeft, Check, AlertCircle, LayoutDashboard } from 'lucide-vue-next'

const authStore = useAuthStore()

const prefs = ref({
  fontSize: 'medium',
  lineSpacing: 'normal',
  defaultDays: 7
})
const loading = ref(true)
const saving = ref(false)
const message = ref('')
const isError = ref(false)
const saved = ref(false)

async function loadPreferences() {
  loading.value = true
  try {
    await authStore.fetchPreferences()
    prefs.value = {
      fontSize: authStore.preferences?.fontSize || 'medium',
      lineSpacing: authStore.preferences?.lineSpacing || 'normal',
      defaultDays: authStore.preferences?.defaultDays || 7
    }
  } catch (e) {
    message.value = 'Failed to load preferences'
    isError.value = true
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  saving.value = true
  message.value = ''
  isError.value = false
  
  try {
    await authStore.updateUserPreferences(prefs.value)
    message.value = 'Preferences saved successfully!'
    saved.value = true
  } catch (e) {
    isError.value = true
    message.value = 'Failed to save preferences: ' + e.message
  } finally {
    saving.value = false
  }
}

function enableEdit() {
  saved.value = false
  message.value = ''
  isError.value = false
}

onMounted(() => {
  loadPreferences()
})
</script>
