<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-10 col-lg-8">
        <h2 class="fw-bold text-warm-dark mb-4">Account Settings</h2>
        
        <div class="settings-grid">
          <!-- User Details Card -->
          <router-link to="/account" class="settings-card" @click.prevent="openUserDetails">
            <div class="card-icon">
              <User :size="24" />
            </div>
            <div class="card-content">
              <h4>User Details</h4>
              <p class="text-muted mb-2">{{ authStore.user?.full_name || 'Not set' }}</p>
              <p class="text-muted mb-0 small">{{ authStore.user?.email }}</p>
            </div>
            <ArrowRight :size="20" class="card-arrow" />
          </router-link>

          <!-- User Preferences Card -->
          <router-link to="/preferences" class="settings-card">
            <div class="card-icon">
              <Settings :size="24" />
            </div>
            <div class="card-content">
              <h4>User Preferences</h4>
              <p class="text-muted mb-0">Customize font size, line spacing, and default date range</p>
            </div>
            <ArrowRight :size="20" class="card-arrow" />
          </router-link>

          <!-- Manage Journal Profiles Card -->
          <router-link to="/profiles" class="settings-card">
            <div class="card-icon">
              <Users :size="24" />
            </div>
            <div class="card-content">
              <h4>Manage Journal Profiles</h4>
              <p class="text-muted mb-0">{{ profileCount }} profile{{ profileCount !== 1 ? 's' : '' }} configured</p>
            </div>
            <ArrowRight :size="20" class="card-arrow" />
          </router-link>

          <!-- Go to Dashboard Card -->
          <router-link to="/dashboard" class="settings-card">
            <div class="card-icon">
              <LayoutDashboard :size="24" />
            </div>
            <div class="card-content">
              <h4>Go to Dashboard</h4>
              <p class="text-muted mb-0">View your research briefs</p>
            </div>
            <ArrowRight :size="20" class="card-arrow" />
          </router-link>
        </div>

          <!-- User Details Modal -->
        <div v-if="showUserDetails" class="modal-backdrop" @click="closeUserDetails">
          <div class="modal-dialog" @click.stop>
            <div class="card p-4">
              <h4 class="fw-bold text-warm-dark mb-4">User Details</h4>
              
              <form @submit.prevent="handleSave">
                <div class="mb-3">
                  <label class="form-label">Full Name</label>
                  <input 
                    v-model="fullName" 
                    type="text" 
                    class="form-control" 
                    placeholder="Enter your name"
                  />
                </div>

                <div class="mb-4">
                  <label class="form-label">Email Address</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    :value="authStore.user?.email" 
                    disabled 
                    readonly
                  />
                  <div class="form-text">Email cannot be changed.</div>
                </div>

                <div v-if="message" :class="['alert mb-3 d-flex align-items-center gap-2', isError ? 'alert-danger' : 'alert-success']">
                  <CheckCircle v-if="!isError" :size="18" />
                  <AlertCircle v-else :size="18" />
                  {{ message }}
                </div>

                <div class="d-flex gap-2">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    {{ loading ? 'Saving...' : 'Save Changes' }}
                  </button>
                  <button type="button" class="btn btn-outline-secondary" @click="closeUserDetails">Cancel</button>
                </div>
              </form>
            </div>
          </div>
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
const showUserDetails = ref(false)

const profileCount = computed(() => dashboardStore.profiles.length || 0)

onMounted(async () => {
    if (!authStore.user) {
        await authStore.fetchUser()
    }
    if (dashboardStore.profiles.length === 0) {
        await dashboardStore.loadProfiles()
    }
    fullName.value = authStore.user?.full_name || ''
})

function openUserDetails() {
    fullName.value = authStore.user?.full_name || ''
    message.value = ''
    isError.value = false
    showUserDetails.value = true
}

function closeUserDetails() {
    showUserDetails.value = false
}

async function handleSave() {
    loading.value = true
    message.value = ''
    isError.value = false
    
    try {
        await authStore.updateProfile(fullName.value)
        message.value = 'Profile updated successfully'
        setTimeout(() => {
            showUserDetails.value = false
        }, 1500)
    } catch (e) {
        isError.value = true
        message.value = e.message
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

@media (max-width: 576px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

.settings-card {
  background: white;
  border: 1px solid var(--warm-200);
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
  min-height: 140px;
}

.settings-card:hover {
  border-color: var(--terracotta-500);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  color: inherit;
}

.card-icon {
  color: var(--warm-500);
  flex-shrink: 0;
  padding-top: 0.25rem;
}

.card-content {
  flex: 1;
  min-width: 0;
}

.card-content h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--warm-900);
  margin-bottom: 0.5rem;
}

.card-content p {
  font-size: 0.875rem;
  margin-bottom: 0;
  word-break: break-word;
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

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-dialog {
  max-width: 400px;
  width: 100%;
  margin: 1rem;
  position: relative;
  z-index: 1051;
}
</style>
