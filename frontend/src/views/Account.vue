<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-10 col-lg-8">
        <h2 class="fw-bold text-warm-dark mb-4">Account Settings</h2>
        
        <div class="settings-grid">
          <!-- Profile Section -->
          <div class="settings-card">
            <div class="card-icon">
              <User :size="20" />
            </div>
            <div class="card-content flex-grow-1">
              <h4 class="mb-3">Profile</h4>
              
              <form @submit.prevent="handleSave">
                <div class="mb-3">
                  <label class="form-label small text-muted mb-1">Email Address</label>
                  <input 
                    type="email" 
                    class="form-control form-control-sm" 
                    :value="authStore.user?.email" 
                    disabled 
                    readonly
                  />
                  <div class="form-text small">Email cannot be changed.</div>
                </div>

                <div class="mb-3">
                  <label class="form-label small text-muted mb-1">Full Name</label>
                  <input 
                    v-model="fullName" 
                    type="text" 
                    class="form-control form-control-sm" 
                    placeholder="Enter your name"
                    :disabled="saved"
                    :readonly="saved"
                  />
                </div>

                <div v-if="message" :class="['alert mb-3 d-flex align-items-center gap-2 py-2', isError ? 'alert-danger' : 'alert-success']">
                  <CheckCircle v-if="!isError" :size="16" />
                  <AlertCircle v-else :size="16" />
                  <span class="small">{{ message }}</span>
                </div>

                <div class="d-flex gap-2" v-if="!saved">
                  <button type="submit" class="btn btn-primary btn-sm" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                    {{ loading ? 'Saving...' : 'Save' }}
                  </button>
                  <button type="button" class="btn btn-outline-secondary btn-sm" @click="resetEdit" v-if="authStore.user?.full_name">
                    Cancel
                  </button>
                </div>

                <div v-if="saved" class="d-flex gap-2">
                  <button type="button" @click="enableEdit" class="btn btn-primary btn-sm d-flex align-items-center gap-1">
                    <Edit :size="14" /> Edit
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- User Preferences - HIGHLIGHTED -->
          <router-link to="/preferences" class="settings-card settings-card--highlight">
            <div class="card-icon card-icon--highlight">
              <Settings :size="24" />
            </div>
            <div class="card-content">
              <h4>User Preferences</h4>
              <p class="text-muted mb-0">Customize font size, line spacing, and default date range</p>
            </div>
            <ArrowRight :size="20" class="card-arrow" />
          </router-link>

          <!-- Navigation Cards -->
          <router-link to="/profiles" class="settings-card">
            <div class="card-icon">
              <Users :size="20" />
            </div>
            <div class="card-content">
              <h4>Manage Profiles</h4>
              <p class="text-muted mb-0">{{ profileCount }} profile{{ profileCount !== 1 ? 's' : '' }} configured</p>
            </div>
            <ArrowRight :size="20" class="card-arrow" />
          </router-link>

          <router-link to="/dashboard" class="settings-card">
            <div class="card-icon">
              <LayoutDashboard :size="20" />
            </div>
            <div class="card-content">
              <h4>Go to Dashboard</h4>
              <p class="text-muted mb-0">View your research briefs</p>
            </div>
            <ArrowRight :size="20" class="card-arrow" />
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useDashboardStore } from '../stores/dashboard'
import { AlertCircle, CheckCircle, LayoutDashboard, Users, Edit, Settings, ArrowRight } from 'lucide-vue-next'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

const fullName = ref('')
const loading = ref(false)
const message = ref('')
const isError = ref(false)
const saved = ref(false)

const profileCount = computed(() => dashboardStore.profiles.length || 0)

onMounted(async () => {
    if (!authStore.user) {
        await authStore.fetchUser()
    }
    if (dashboardStore.profiles.length === 0) {
        await dashboardStore.loadProfiles()
    }
    fullName.value = authStore.user?.full_name || ''
    if (fullName.value) {
        saved.value = true
    }
})

async function handleSave() {
    loading.value = true
    message.value = ''
    isError.value = false
    
    try {
        await authStore.updateProfile(fullName.value)
        message.value = 'Profile updated successfully'
        saved.value = true
    } catch (e) {
        isError.value = true
        message.value = e.message
    } finally {
        loading.value = false
    }
}

function resetEdit() {
    fullName.value = authStore.user?.full_name || ''
}

function enableEdit() {
    saved.value = false
    message.value = ''
    isError.value = false
}
</script>

<style scoped>
.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.settings-card {
  background: white;
  border: 1px solid var(--warm-200);
  border-radius: 0.75rem;
  padding: 1.25rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
}

.settings-card:hover {
  border-color: var(--terracotta-500);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  color: inherit;
}

.settings-card--highlight {
  border-color: var(--terracotta-500);
  background: linear-gradient(135deg, rgba(224, 122, 95, 0.08) 0%, white 50%);
}

.card-icon {
  color: var(--warm-500);
  flex-shrink: 0;
  padding-top: 0.25rem;
}

.card-icon--highlight {
  color: var(--terracotta-500);
}

.card-content {
  flex: 1;
  min-width: 0;
}

.card-content h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--warm-900);
  margin-bottom: 0.25rem;
}

.card-content p {
  font-size: 0.875rem;
  margin-bottom: 0;
}

.card-arrow {
  color: var(--warm-500);
  flex-shrink: 0;
  margin-top: 0.25rem;
  opacity: 0.5;
  transition: all 0.2s ease;
}

.settings-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(4px);
  color: var(--terracotta-500);
}

.settings-card--highlight .card-arrow {
  color: var(--terracotta-500);
  opacity: 1;
}
</style>
