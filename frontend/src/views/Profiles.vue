<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="text-warm-dark fw-bold mb-1">Manage Profiles</h2>
        <p class="text-muted mb-0">Edit, add, or remove journals from your profiles</p>
      </div>
      <router-link to="/dashboard" class="btn btn-light d-flex align-items-center gap-2">
        <ArrowLeft :size="18" />
        Back to Dashboard
      </router-link>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success d-flex align-items-center gap-2 mb-4" role="alert">
      <CheckCircle :size="18" />
      {{ successMessage }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border"></div>
      <p class="text-muted mt-3">Loading profiles...</p>
    </div>

    <!-- No Profiles -->
    <div v-else-if="profiles.length === 0" class="empty-state">
      <Users :size="48" class="icon-muted mb-3" />
      <h4>No profiles yet</h4>
      <p class="text-muted">Create your first profile to get started.</p>
      <router-link to="/onboarding" class="btn btn-primary">Create Profile</router-link>
    </div>

    <!-- Profiles List -->
    <div v-else class="row g-4">
      <div v-for="profile in profiles" :key="profile.id" class="col-md-6">
        <div class="card h-100 profile-card" :class="{ 'editing': editingId === profile.id }" @click="handleCardClick(profile)">
          <div class="card-header d-flex justify-content-between align-items-center flex-wrap gap-2">
            <div v-if="editingId !== profile.id" class="d-flex align-items-center gap-2 flex-wrap">
              <h5 class="mb-0 text-warm-dark">{{ profile.name }}</h5>
              <span v-if="profile.is_default" class="badge bg-terracotta-100 text-terracotta-600 d-flex align-items-center gap-1">
                <Star :size="12" /> Current Default
              </span>
            </div>
            <div v-else class="flex-grow-1 me-2">
              <input 
                v-model="editName" 
                class="form-control form-control-sm" 
                placeholder="Profile name"
              />
            </div>
            <div class="d-flex gap-1 flex-wrap">
              <button 
                v-if="editingId !== profile.id && !profile.is_default"
                class="btn btn-sm btn-outline-terracotta d-flex align-items-center gap-1" 
                @click.stop="setAsDefault(profile.id)"
                title="Set as default profile"
              >
                <Star :size="14" /> Set Default
              </button>
              <button 
                v-if="editingId !== profile.id"
                class="btn btn-sm btn-outline-primary d-flex align-items-center gap-1" 
                @click.stop="startEdit(profile)"
              >
                <Edit2 :size="14" /> Edit
              </button>
              <template v-else>
                <button class="btn btn-sm btn-success d-flex align-items-center gap-1" @click.stop="saveEdit(profile.id)" :disabled="saving">
                  <Check :size="14" /> {{ saving ? '...' : 'Save' }}
                </button>
                <button class="btn btn-sm btn-secondary d-flex align-items-center gap-1" @click.stop="cancelEdit">
                  <X :size="14" /> Cancel
                </button>
              </template>
              <button 
                class="btn btn-sm btn-outline-danger d-flex align-items-center gap-1" 
                @click.stop="confirmDelete(profile)"
                :disabled="profiles.length === 1"
                :title="profiles.length === 1 ? 'Cannot delete your only profile' : 'Delete profile'"
              >
                <Trash2 :size="14" />
              </button>
            </div>
          </div>
          <div class="card-body">
            <p class="text-muted small mb-2">
              {{ profile.journal_ids.length }} journal(s) selected
            </p>
            
            <!-- Edit Mode: Journal Selection -->
            <div v-if="editingId === profile.id">
              <div class="mb-3">
                <div class="input-group">
                  <span class="input-group-text bg-white border-end-0">
                    <Search :size="16" class="icon-muted" />
                  </span>
                  <input 
                    v-model="journalSearch" 
                    class="form-control form-control-sm border-start-0" 
                    placeholder="Search journals..."
                    @input="debouncedSearch"
                  />
                </div>
              </div>
              
              <!-- Search Results -->
              <div v-if="journalSearch && searchResults.length > 0" class="mb-3">
                <small class="text-muted">Search results:</small>
                <div class="journal-list">
                  <div 
                    v-for="j in searchResults" 
                    :key="'search-' + j.id"
                    class="journal-item d-flex align-items-center p-2 rounded"
                    :class="{ selected: editJournalIds.includes(j.id) }"
                    @click="toggleJournal(j.id)"
                  >
                    <input type="checkbox" class="form-check-input me-2" :checked="editJournalIds.includes(j.id)" />
                    <div>
                      <div class="small fw-semibold text-warm-dark">{{ j.name }}</div>
                      <small class="text-muted">{{ j.category }}</small>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Selected Journals -->
              <div>
                <small class="text-muted">Selected journals ({{ editJournalIds.length }}):</small>
                <div class="selected-journals mt-2">
                  <span 
                    v-for="jId in editJournalIds" 
                    :key="jId" 
                    class="badge badge-journal me-1 mb-1 d-inline-flex align-items-center gap-1"
                    style="cursor: pointer;"
                    @click="toggleJournal(jId)"
                  >
                    {{ getJournalName(jId) }}
                    <X :size="12" />
                  </span>
                  <span v-if="editJournalIds.length === 0" class="text-muted small">
                    No journals selected
                  </span>
                </div>
              </div>
            </div>
            
            <!-- View Mode: Journal List -->
            <div v-else>
              <div class="journal-tags">
                <span 
                  v-for="jId in profile.journal_ids.slice(0, 5)" 
                  :key="jId" 
                  class="badge bg-secondary me-1 mb-1"
                >
                  {{ getJournalName(jId) }}
                </span>
                <span v-if="profile.journal_ids.length > 5" class="badge bg-light text-dark">
                  +{{ profile.journal_ids.length - 5 }} more
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add New Profile Card -->
      <div class="col-md-6">
        <router-link to="/onboarding" class="card h-100 text-decoration-none add-profile-card">
          <div class="card-body d-flex flex-column align-items-center justify-content-center text-center py-5">
            <Plus :size="48" class="text-terracotta mb-3" />
            <h5 class="text-terracotta">Create New Profile</h5>
            <p class="text-muted small">Add another profile for different research interests</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="deleteTarget" class="modal-backdrop" @click="deleteTarget = null">
      <div class="modal-dialog" @click.stop>
        <div class="card p-4">
          <div class="d-flex align-items-center gap-2 mb-3">
            <AlertTriangle :size="24" class="text-danger" />
            <h5 class="mb-0">Delete Profile?</h5>
          </div>
          <p class="text-muted">Are you sure you want to delete "{{ deleteTarget.name }}"? This cannot be undone.</p>
          <div class="d-flex gap-2 justify-content-end">
            <button type="button" class="btn btn-secondary" @click.stop.prevent="deleteTarget = null" style="pointer-events: auto;">Cancel</button>
            <button type="button" class="btn btn-danger d-flex align-items-center gap-1" @click.stop.prevent="doDelete" :disabled="deleting" style="pointer-events: auto;">
              <Trash2 :size="16" />
              {{ deleting ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getProfiles, searchJournals, updateProfile, deleteProfile, getJournalsByIds, setDefaultProfile } from '../services/api'
import { useDashboardStore } from '../stores/dashboard'
import { useToast } from '@/utils/shareUtils'
import { 
  ArrowLeft, Users, Edit2, Check, X, Trash2, Search, Plus, AlertTriangle, CheckCircle, Star 
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const store = useDashboardStore()
const { show } = useToast()

const profiles = ref([])
const loading = ref(true)
const editingId = ref(null)
const editName = ref('')
const editJournalIds = ref([])
const journalSearch = ref('')
const searchResults = ref([])
const saving = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)
const successMessage = ref('')
const allJournals = ref({}) // Cache journal names

let searchTimeout = null

async function loadProfiles() {
  loading.value = true
  try {
    profiles.value = await getProfiles()
  } catch (e) {
    console.error('Failed to load profiles:', e)
  } finally {
    loading.value = false
  }
}

function startEdit(profile) {
  editingId.value = profile.id
  editName.value = profile.name
  editJournalIds.value = [...profile.journal_ids]
  journalSearch.value = ''
  searchResults.value = []
}

function cancelEdit() {
  editingId.value = null
  editName.value = ''
  editJournalIds.value = []
  journalSearch.value = ''
  searchResults.value = []
}

async function saveEdit(profileId) {
  if (!editName.value.trim()) return
  
  saving.value = true
  try {
    const updated = await updateProfile(profileId, editName.value.trim(), editJournalIds.value)
    const idx = profiles.value.findIndex(p => p.id === profileId)
    if (idx !== -1) {
      profiles.value[idx] = updated
    }
    // Force dashboard store to reload profiles so changes appear on dashboard
    store.loadProfiles(true)
    successMessage.value = 'Profile updated successfully!'
    setTimeout(() => { successMessage.value = '' }, 5000)
    cancelEdit()
  } catch (e) {
    console.error('Failed to update profile:', e)
    alert('Failed to update profile: ' + e.message)
  } finally {
    saving.value = false
  }
}

function debouncedSearch() {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    if (journalSearch.value.length >= 2) {
      try {
        const results = await searchJournals(journalSearch.value)
        searchResults.value = results
        // Cache journal names
        results.forEach(j => { allJournals.value[j.id] = j.name })
      } catch (e) {
        searchResults.value = []
      }
    } else {
      searchResults.value = []
    }
  }, 300)
}

function toggleJournal(journalId) {
  const idx = editJournalIds.value.indexOf(journalId)
  if (idx === -1) {
    editJournalIds.value.push(journalId)
  } else {
    editJournalIds.value.splice(idx, 1)
  }
}

function getJournalName(journalId) {
  return allJournals.value[journalId] || `Journal #${journalId}`
}

function confirmDelete(profile) {
  deleteTarget.value = profile
}

async function setAsDefault(profileId) {
  try {
    await setDefaultProfile(profileId)
    await loadProfiles()
    // Also refresh the dashboard store to pick up the new default
    store.loadProfiles(true)
    show('Default profile updated!', 'success')
  } catch (e) {
    show('Failed to set default: ' + e.message, 'error')
  }
}

async function doDelete() {
  if (!deleteTarget.value) return
  
  deleting.value = true
  const deletedName = deleteTarget.value.name
  try {
    await deleteProfile(deleteTarget.value.id)
    profiles.value = profiles.value.filter(p => p.id !== deleteTarget.value.id)
    deleteTarget.value = null
    successMessage.value = `Profile "${deletedName}" was deleted successfully.`
    // Force dashboard store to reload profiles
    store.loadProfiles(true)
    // Auto-hide success message after 5 seconds
    setTimeout(() => { successMessage.value = '' }, 5000)
  } catch (e) {
    console.error('Failed to delete:', e)
    alert('Failed to delete profile: ' + e.message)
  } finally {
    deleting.value = false
  }
}

// Load journal names for all profiles
async function loadJournalNames() {
  try {
    // Collect all unique journal IDs from all profiles
    const allIds = new Set()
    profiles.value.forEach(p => {
      p.journal_ids.forEach(id => allIds.add(id))
    })
    
    if (allIds.size > 0) {
      const journals = await getJournalsByIds([...allIds])
      journals.forEach(j => { allJournals.value[j.id] = j.name })
    }
  } catch (e) {
    console.error('Failed to load journal names:', e)
  }
}

onMounted(async () => {
  await loadProfiles()
  loadJournalNames()
  
  // Check for success message from profile creation
  if (route.query.created === '1') {
    successMessage.value = 'Profile created successfully!'
    // Force dashboard store to reload profiles so new profile shows up
    store.loadProfiles(true)
    // Remove query param from URL
    router.replace({ path: '/profiles' })
    // Auto-hide success message after 5 seconds
    setTimeout(() => { successMessage.value = '' }, 5000)
  }
})

// Handle profile card click - navigate to dashboard with that profile active
function handleCardClick(profile) {
  // Don't navigate if we're in edit mode
  if (editingId.value === profile.id) return
  
  // Set the profile in the dashboard store and navigate
  store.setProfile(profile.id)
  router.push('/dashboard')
}
</script>

<style scoped>
.journal-list {
  max-height: 200px;
  overflow-y: auto;
}

.journal-item {
  cursor: pointer;
  border: 1px solid var(--warm-200);
  margin-bottom: 4px;
}

.journal-item:hover {
  background: var(--cream-50);
}

.journal-item.selected {
  background: var(--terracotta-100);
  border-color: var(--terracotta-500);
}

.add-profile-card {
  border: 2px dashed var(--warm-200);
  transition: all 0.2s;
}

.add-profile-card:hover {
  border-color: var(--terracotta-500);
  background: var(--terracotta-100);
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

.card-header {
  background-color: white;
  border-bottom: 1px solid var(--warm-200);
}

.badge-journal {
  background-color: var(--terracotta-100);
  color: var(--terracotta-600);
}

.input-group-text {
  border-color: var(--warm-200);
}

.profile-card {
  cursor: pointer;
  transition: all 0.2s ease;
}

.profile-card:hover:not(.editing) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-color: var(--terracotta-500);
}

.profile-card.editing {
  cursor: default;
}
</style>
