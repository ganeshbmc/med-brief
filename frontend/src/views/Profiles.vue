<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="text-white fw-bold mb-1">Manage Profiles</h2>
        <p class="text-white-50 mb-0">Edit, add, or remove journals from your profiles</p>
      </div>
      <router-link to="/dashboard" class="btn btn-light">
        ← Back to Dashboard
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-light"></div>
      <p class="text-white mt-3">Loading profiles...</p>
    </div>

    <!-- No Profiles -->
    <div v-else-if="profiles.length === 0" class="card p-5 text-center">
      <h4>No profiles yet</h4>
      <p class="text-muted">Create your first profile to get started.</p>
      <router-link to="/onboarding" class="btn btn-primary">Create Profile</router-link>
    </div>

    <!-- Profiles List -->
    <div v-else class="row g-4">
      <div v-for="profile in profiles" :key="profile.id" class="col-md-6">
        <div class="card h-100">
          <div class="card-header d-flex justify-content-between align-items-center">
            <div v-if="editingId !== profile.id">
              <h5 class="mb-0">{{ profile.name }}</h5>
            </div>
            <div v-else class="flex-grow-1 me-2">
              <input 
                v-model="editName" 
                class="form-control form-control-sm" 
                placeholder="Profile name"
              />
            </div>
            <div class="btn-group btn-group-sm">
              <button 
                v-if="editingId !== profile.id"
                class="btn btn-outline-primary" 
                @click="startEdit(profile)"
              >
                ✏️ Edit
              </button>
              <template v-else>
                <button class="btn btn-success" @click="saveEdit(profile.id)" :disabled="saving">
                  {{ saving ? '...' : '✓ Save' }}
                </button>
                <button class="btn btn-secondary" @click="cancelEdit">
                  ✕ Cancel
                </button>
              </template>
              <button 
                class="btn btn-outline-danger" 
                @click="confirmDelete(profile)"
                :disabled="profiles.length === 1"
                :title="profiles.length === 1 ? 'Cannot delete your only profile' : 'Delete profile'"
              >
                🗑️
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
                <input 
                  v-model="journalSearch" 
                  class="form-control form-control-sm" 
                  placeholder="🔍 Search journals..."
                  @input="debouncedSearch"
                />
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
                      <div class="small fw-semibold">{{ j.name }}</div>
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
                    class="badge bg-primary me-1 mb-1"
                    style="cursor: pointer;"
                    @click="toggleJournal(jId)"
                  >
                    {{ getJournalName(jId) }} ✕
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
            <div class="display-4 text-primary mb-3">➕</div>
            <h5 class="text-primary">Create New Profile</h5>
            <p class="text-muted small">Add another profile for different research interests</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="deleteTarget" class="modal-backdrop" @click="deleteTarget = null">
      <div class="modal-dialog" @click.stop>
        <div class="card p-4">
          <h5>Delete Profile?</h5>
          <p class="text-muted">Are you sure you want to delete "{{ deleteTarget.name }}"? This cannot be undone.</p>
          <div class="d-flex gap-2 justify-content-end">
            <button class="btn btn-secondary" @click="deleteTarget = null">Cancel</button>
            <button class="btn btn-danger" @click="doDelete" :disabled="deleting">
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
import { getProfiles, searchJournals, updateProfile, deleteProfile } from '../services/api'

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

async function doDelete() {
  if (!deleteTarget.value) return
  
  deleting.value = true
  try {
    await deleteProfile(deleteTarget.value.id)
    profiles.value = profiles.value.filter(p => p.id !== deleteTarget.value.id)
    deleteTarget.value = null
  } catch (e) {
    console.error('Failed to delete:', e)
    alert('Failed to delete profile: ' + e.message)
  } finally {
    deleting.value = false
  }
}

// Pre-load journal names for existing profiles
async function loadJournalNames() {
  try {
    // Search for common terms to populate cache
    const terms = ['lancet', 'jama', 'nature', 'circulation', 'bmj']
    for (const term of terms) {
      const results = await searchJournals(term)
      results.forEach(j => { allJournals.value[j.id] = j.name })
    }
  } catch (e) {
    // Ignore
  }
}

onMounted(async () => {
  await loadProfiles()
  loadJournalNames()
})
</script>

<style scoped>
.journal-list {
  max-height: 200px;
  overflow-y: auto;
}

.journal-item {
  cursor: pointer;
  border: 1px solid #eee;
  margin-bottom: 4px;
}

.journal-item:hover {
  background: #f8f9fa;
}

.journal-item.selected {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.add-profile-card {
  border: 2px dashed #dee2e6;
  transition: all 0.2s;
}

.add-profile-card:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
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
}
</style>
