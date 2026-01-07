<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card p-4 p-md-5">
          <div class="text-center mb-4">
            <img src="/medbrief_icon.png" alt="MedBrief" class="mb-3" style="width: 64px; height: 64px;" />
            <h2 class="fw-bold text-warm-dark">Welcome to MedBrief!</h2>
            <p class="text-muted">Let's personalize your experience</p>
          </div>

          <!-- Progress Steps -->
          <div class="d-flex justify-content-center mb-5">
            <div 
              v-for="n in 3" 
              :key="n" 
              class="step-indicator mx-2"
              :class="{ active: step >= n, completed: step > n }"
            >
              <Check v-if="step > n" :size="18" />
              <span v-else>{{ n }}</span>
            </div>
          </div>

          <!-- Step 1: Specialty Selection -->
          <div v-if="step === 1" class="step-content">
            <h5 class="mb-4 fw-semibold text-warm-dark">What's your medical specialty?</h5>
            <div class="row g-3">
              <div 
                v-for="spec in specialties" 
                :key="spec.value" 
                class="col-md-4"
              >
                <div 
                  class="specialty-card p-3 rounded-3 text-center d-flex align-items-center justify-content-center gap-2"
                  :class="{ 
                    selected: selectedSpecialty === spec.value,
                    'custom-highlight': spec.isCustom && selectedSpecialty !== spec.value
                  }"
                  @click="selectSpecialty(spec.value)"
                >
                  <Sparkles v-if="spec.isCustom" :size="16" />
                  {{ spec.label }}
                </div>
              </div>
            </div>
          </div>

          <!-- Step 2: Journal Selection -->
          <div v-if="step === 2" class="step-content">
            <h5 class="mb-3 fw-semibold text-warm-dark">Select journals to follow</h5>
            
            <!-- Search Box -->
            <div class="mb-4">
              <div class="input-group">
                <span class="input-group-text bg-white">
                  <Search :size="18" class="icon-muted" />
                </span>
                <input 
                  v-model="searchQuery" 
                  type="text" 
                  class="form-control" 
                  placeholder="Search journals by name or ISSN..."
                  @input="debouncedSearch"
                />
              </div>
              <small class="text-muted">Search across all journals or select from suggestions below</small>
            </div>
            
            <!-- Search Results -->
            <div v-if="searchQuery && searchResults.length > 0" class="mb-4">
              <h6 class="text-muted mb-2">Search Results</h6>
              <div class="row g-2">
                <div v-for="journal in searchResults" :key="'search-' + (journal.issn || journal.id || journal.name)" class="col-md-6">
                  <div 
                    class="journal-card p-2 rounded-3 d-flex align-items-center"
                    :class="{ selected: isJournalSelected(journal) }"
                    @click="toggleJournal(journal)"
                  >
                    <Newspaper :size="18" class="me-2 icon-muted" />
                    <div class="flex-grow-1 overflow-hidden">
                      <div class="fw-semibold text-truncate small text-warm-dark">{{ journal.name }}</div>
                      <small class="text-muted">{{ journal.iso_abbreviation }} · {{ journal.issn }}</small>
                    </div>
                    <Check v-if="journal.is_local" :size="16" class="text-success ms-2" title="In our database" />
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="searchQuery && searching" class="mb-4 text-center text-muted">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Searching...
            </div>
            
            <div v-else-if="searchQuery && searchResults.length === 0" class="mb-4 text-center text-muted">
              <FileText :size="24" class="mb-2 icon-muted" />
              <p class="mb-1">No journals found matching "{{ searchQuery }}"</p>
              <small class="text-info d-flex align-items-center justify-content-center gap-1">
                <Lightbulb :size="14" /> Tip: Use ISSN for accurate results
              </small>
            </div>
            
            <!-- ISSN hint after search results -->
            <div v-if="searchQuery && searchResults.length > 0 && !searching" class="mb-3 text-center">
              <small class="text-muted d-flex align-items-center justify-content-center gap-1">
                <Lightbulb :size="14" />
                Didn't find what you're looking for? Try searching with the journal's <strong>ISSN</strong> for more accurate results.
              </small>
            </div>
            
            <!-- Preset Journals -->
            <div v-if="!searchQuery">
              <div v-if="loadingJournals" class="text-center py-4">
                <div class="spinner-border" role="status"></div>
                <p class="mt-2 text-muted">Loading journals...</p>
              </div>
              <div v-else-if="journals.length === 0" class="text-center py-4">
                <FileText :size="32" class="icon-muted mb-2" />
                <p class="text-muted">No preset journals for this specialty. Use search above to find journals.</p>
              </div>
              <div v-else>
                <h6 class="text-muted mb-2">Suggested for {{ getSpecialtyLabel() }}</h6>
                <div class="row g-2">
                  <div v-for="journal in journals" :key="journal.id" class="col-md-6">
                    <div 
                      class="journal-card p-2 rounded-3 d-flex align-items-center"
                      :class="{ selected: selectedJournalIds.includes(journal.id) }"
                      @click="toggleJournal(journal)"
                    >
                      <Newspaper :size="18" class="me-2 icon-muted" />
                      <div class="flex-grow-1 overflow-hidden">
                        <div class="fw-semibold text-truncate small text-warm-dark">{{ journal.name }}</div>
                        <small class="text-muted">{{ journal.iso_abbreviation }}</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Selected Count -->
            <div v-if="totalSelectedCount > 0" class="mt-3 text-center">
              <span class="badge bg-primary">{{ totalSelectedCount }} journal(s) selected</span>
            </div>
          </div>

          <!-- Step 3: Profile Name -->
          <div v-if="step === 3" class="step-content">
            <h5 class="mb-4 fw-semibold text-warm-dark">Name your profile</h5>
            <div class="mb-4">
              <div class="input-group">
                <span class="input-group-text bg-white">
                  <FileText :size="18" class="icon-muted" />
                </span>
                <input 
                  v-model="profileName" 
                  type="text" 
                  class="form-control form-control-lg" 
                  placeholder="e.g., My Cardiology Feed"
                />
              </div>
              <small class="text-muted">You can create multiple profiles later for different interests</small>
            </div>
            <div v-if="error" class="alert alert-danger d-flex align-items-center gap-2">
              <AlertCircle :size="18" />
              {{ error }}
            </div>
          </div>

          <!-- Navigation Buttons -->
          <div class="d-flex justify-content-between mt-5">
            <button 
              v-if="step > 1" 
              class="btn btn-outline-secondary px-4 d-flex align-items-center gap-2"
              @click="step--"
            >
              <ArrowLeft :size="18" />
              Back
            </button>
            <div v-else></div>
            <button 
              class="btn btn-primary px-4 d-flex align-items-center gap-2"
              :disabled="!canProceed || saving"
              @click="nextStep"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm"></span>
              {{ step === 3 ? 'Create Profile' : 'Continue' }}
              <ArrowRight v-if="step < 3" :size="18" />
              <Check v-else :size="18" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getPresetJournals, searchJournals, searchPubmedJournals, createProfile } from '../services/api'
import { 
  BookOpen, Check, Sparkles, Search, Newspaper, FileText, 
  Lightbulb, AlertCircle, ArrowLeft, ArrowRight 
} from 'lucide-vue-next'

const router = useRouter()

const step = ref(1)
const selectedSpecialty = ref('')
const journals = ref([])
const selectedJournalIds = ref([])
const selectedNewJournals = ref([])  // PubMed journals not in DB
const loadingJournals = ref(false)
const profileName = ref('')
const error = ref('')
const saving = ref(false)

// Search state
const searchQuery = ref('')
const searchResults = ref([])
const searching = ref(false)
let searchTimeout = null

const specialties = [
  { value: 'Custom', label: 'Custom Profile', isCustom: true },
  { value: 'Cardiology', label: 'Cardiology' },
  { value: 'Oncology', label: 'Oncology' },
  { value: 'Neurology', label: 'Neurology' },
  { value: 'Pediatrics', label: 'Pediatrics' },
  { value: 'Medicine', label: 'Internal Medicine' },
  { value: 'Surgery', label: 'Surgery' },
  { value: 'Psychiatry', label: 'Psychiatry' },
  { value: 'Emergency', label: 'Emergency Medicine' },
]

const canProceed = computed(() => {
  if (step.value === 1) return selectedSpecialty.value
  // Allow skip if no journals found, require selection if journals exist
  if (step.value === 2) return totalSelectedCount.value > 0
  if (step.value === 3) return profileName.value.trim()
  return true
})

const totalSelectedCount = computed(() => {
  return selectedJournalIds.value.length + selectedNewJournals.value.length
})

function getSpecialtyLabel() {
  const spec = specialties.find(s => s.value === selectedSpecialty.value)
  return spec?.label || selectedSpecialty.value
}

async function selectSpecialty(specialty) {
  selectedSpecialty.value = specialty
  // Pre-set profile name based on specialty
  const spec = specialties.find(s => s.value === specialty)
  if (spec && specialty !== 'Custom') {
    profileName.value = `My ${spec.label} Brief`
  } else {
    profileName.value = 'My Custom Brief'
  }
}

// Debounced search function - uses PubMed search for Custom profiles
function debouncedSearch() {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(async () => {
    if (searchQuery.value.length >= 2) {
      searching.value = true
      try {
        // Use PubMed search for Custom specialty, local DB for others
        if (selectedSpecialty.value === 'Custom') {
          searchResults.value = await searchPubmedJournals(searchQuery.value)
        } else {
          searchResults.value = await searchJournals(searchQuery.value)
        }
      } catch (e) {
        console.error('Search failed:', e)
        searchResults.value = []
      } finally {
        searching.value = false
      }
    } else {
      searchResults.value = []
    }
  }, 300)
}

// Load journals when moving to step 2
watch(step, async (newStep) => {
  if (newStep === 2 && journals.value.length === 0 && selectedSpecialty.value !== 'Custom') {
    loadingJournals.value = true
    try {
      journals.value = await getPresetJournals(selectedSpecialty.value)
    } catch (e) {
      console.error('Failed to load journals:', e)
      journals.value = []
    } finally {
      loadingJournals.value = false
    }
  }
})

function isJournalSelected(journal) {
  // For local DB journals (have id)
  if (journal.id) {
    return selectedJournalIds.value.includes(journal.id)
  }
  // For PubMed journals (use issn as identifier)
  return selectedNewJournals.value.some(j => j.issn === journal.issn)
}

function toggleJournal(journal) {
  // For local DB journals (have id)
  if (journal.id) {
    const idx = selectedJournalIds.value.indexOf(journal.id)
    if (idx === -1) {
      selectedJournalIds.value.push(journal.id)
    } else {
      selectedJournalIds.value.splice(idx, 1)
    }
  } else {
    // For PubMed journals (no id, use issn)
    const idx = selectedNewJournals.value.findIndex(j => j.issn === journal.issn)
    if (idx === -1) {
      selectedNewJournals.value.push({
        name: journal.name,
        issn: journal.issn,
        iso_abbreviation: journal.iso_abbreviation,
      })
    } else {
      selectedNewJournals.value.splice(idx, 1)
    }
  }
}

async function nextStep() {
  if (step.value < 3) {
    step.value++
  } else {
    // Create profile and navigate to dashboard
    saving.value = true
    error.value = ''
    try {
      await createProfile(
        profileName.value.trim(), 
        selectedJournalIds.value,
        selectedNewJournals.value
      )
      router.push('/profiles?created=1')
    } catch (e) {
      error.value = e.message || 'Failed to create profile'
    } finally {
      saving.value = false
    }
  }
}
</script>

<style scoped>
.step-indicator {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--warm-200);
  color: var(--warm-500);
  font-weight: 600;
  transition: all 0.3s ease;
}

.step-indicator.active {
  background: var(--terracotta-500);
  color: white;
}

.step-indicator.completed {
  background: var(--sage-500);
  color: white;
}

.specialty-card,
.journal-card {
  border: 2px solid var(--warm-200);
  cursor: pointer;
  transition: all 0.2s ease;
}

.specialty-card:hover,
.journal-card:hover {
  border-color: var(--terracotta-500);
  background: var(--terracotta-100);
}

.specialty-card.selected,
.journal-card.selected {
  border-color: var(--terracotta-500);
  background: var(--terracotta-100);
}

.specialty-card.custom-highlight {
  background: var(--terracotta-500);
  color: white;
  border-color: transparent;
}

.specialty-card.custom-highlight:hover {
  opacity: 0.9;
  border-color: transparent;
  background: var(--terracotta-600);
}

.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.input-group-text {
  border-color: var(--warm-200);
  border-right: none;
}

.input-group .form-control {
  border-left: none;
}
</style>
