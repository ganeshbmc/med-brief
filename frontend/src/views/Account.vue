<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card p-4">
          <h2 class="fw-bold text-warm-dark mb-4">Account Settings</h2>
          
          <form @submit.prevent="handleSave">
            <div class="mb-3">
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

            <div class="mb-4">
              <label class="form-label">Full Name</label>
              <input 
                v-model="fullName" 
                type="text" 
                class="form-control" 
                placeholder="Enter your name"
                :disabled="saved"
                :readonly="saved"
              />
            </div>

            <div v-if="message" :class="['alert', isError ? 'alert-danger' : 'alert-success', 'd-flex align-items-center gap-2']">
              <AlertCircle v-if="isError" :size="18" />
              <CheckCircle v-else :size="18" />
              {{ message }}
            </div>

            <!-- Show navigation options after successful save -->
            <div v-if="saved" class="d-flex gap-2 flex-wrap">
              <button type="button" @click="resetEdit" class="btn btn-primary d-flex align-items-center gap-2">
                <Edit :size="18" />
                Edit
              </button>
              <router-link to="/dashboard" class="btn btn-outline-secondary d-flex align-items-center gap-2">
                <LayoutDashboard :size="18" />
                Go to Dashboard
              </router-link>
              <router-link to="/profiles" class="btn btn-outline-secondary d-flex align-items-center gap-2">
                <Users :size="18" />
                Manage Profiles
              </router-link>
            </div>
            <!-- Show form buttons before save -->
            <div v-else class="d-flex gap-2">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Save Changes
              </button>
              <router-link to="/dashboard" class="btn btn-outline-secondary">Cancel</router-link>
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
import { AlertCircle, CheckCircle, LayoutDashboard, Users, Edit } from 'lucide-vue-next'

const authStore = useAuthStore()
const fullName = ref('')
const loading = ref(false)
const message = ref('')
const isError = ref(false)
const saved = ref(false)

onMounted(async () => {
    if (!authStore.user) {
        await authStore.fetchUser()
    }
    fullName.value = authStore.user?.full_name || ''
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
    saved.value = false
    message.value = ''
}
</script>
