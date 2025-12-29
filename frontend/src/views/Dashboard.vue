<template>
  <div class="container py-4">
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-3">
      <div>
        <h2 class="text-white fw-bold mb-1">Your Brief</h2>
        <p class="text-white-50 mb-0">Research from {{ store.fromDate }} to {{ store.toDate }}</p>
      </div>
      <div class="d-flex gap-2 align-items-center">
        <!-- Profile Selector -->
        <div v-if="store.profiles.length > 0" class="dropdown">
          <button 
            class="btn btn-light dropdown-toggle" 
            type="button" 
            data-bs-toggle="dropdown" 
            aria-expanded="false"
          >
            📋 {{ store.currentProfile?.name || 'Select Profile' }}
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li v-for="p in store.profiles" :key="p.id">
              <a 
                class="dropdown-item" 
                :class="{ active: store.selectedProfileId === p.id }"
                href="#" 
                @click.prevent="selectProfile(p.id)"
              >
                {{ p.name }}
                <small v-if="store.selectedProfileId === p.id" class="text-success ms-2">✓</small>
              </a>
            </li>
            <li><hr class="dropdown-divider" /></li>
            <li>
              <router-link class="dropdown-item text-primary fw-semibold" to="/onboarding">
                ➕ Create New Profile
              </router-link>
            </li>
          </ul>
        </div>
        
        <button class="btn btn-light" @click="refreshArticles" :disabled="store.loading">
          <span v-if="store.loading" class="spinner-border spinner-border-sm me-1"></span>
          {{ store.loading ? 'Loading...' : '🔄 Refresh' }}
        </button>
      </div>
    </div>

    <!-- No Profiles State -->
    <div v-if="!store.loadingProfiles && store.profiles.length === 0" class="card p-5 text-center">
      <h4 class="mb-3">Welcome to MedBrief!</h4>
      <p class="text-muted mb-4">You haven't created any profiles yet. Create one to start receiving personalized research briefs.</p>
      <router-link to="/onboarding" class="btn btn-primary px-4">Create Your First Profile</router-link>
    </div>

    <!-- Loading Profiles State -->
    <div v-else-if="store.loadingProfiles" class="text-center py-5">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-white mt-3">Loading your profiles...</p>
    </div>

    <!-- Main Content -->
    <template v-else>
      <!-- Current Profile Info with Article Count -->
      <div class="card mb-4 p-3 bg-light">
        <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
          <div>
            <strong>{{ store.currentProfile?.name }}</strong>
            <span class="text-muted ms-2">· {{ store.currentProfile?.journal_ids?.length || 0 }} journals</span>
          </div>
          <div>
            <span class="badge bg-primary me-2">{{ filteredArticles.length }} article{{ filteredArticles.length !== 1 ? 's' : '' }}</span>
            <small class="text-muted">{{ store.profiles.length }} profile{{ store.profiles.length !== 1 ? 's' : '' }}</small>
          </div>
        </div>
      </div>
      
      <!-- Filters -->
      <div class="card mb-4 p-3">
        <div class="row g-3 align-items-center">
          <div class="col-md-3">
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control" 
              placeholder="🔍 Search articles..."
            />
          </div>
          <div class="col-md-3">
            <!-- Journal Filter Dropdown -->
            <div class="dropdown">
              <button 
                class="btn btn-outline-secondary w-100 dropdown-toggle text-start" 
                type="button" 
                data-bs-toggle="dropdown"
                data-bs-auto-close="outside"
              >
                {{ selectedJournals.length ? `${selectedJournals.length} journal(s)` : 'All Journals' }}
              </button>
              <ul class="dropdown-menu w-100" style="max-height: 300px; overflow-y: auto;">
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="selectedJournals = []">
                    <em>Clear filters</em>
                  </a>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li v-for="journal in availableJournals" :key="journal.name">
                  <a 
                    class="dropdown-item d-flex align-items-center justify-content-between" 
                    href="#" 
                    @click.prevent="toggleJournalFilter(journal.name)"
                  >
                    <span class="d-flex align-items-center">
                      <input 
                        type="checkbox" 
                        class="form-check-input me-2" 
                        :checked="selectedJournals.includes(journal.name)"
                        @click.stop
                      />
                      <span class="text-truncate" style="max-width: 200px;">{{ journal.name }}</span>
                    </span>
                    <span class="badge" :class="journal.count ? 'bg-primary' : 'bg-secondary'">{{ journal.count }}</span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-auto">
            <label class="form-label small text-muted mb-1">Quick Select</label>
            <select v-model="store.daysPreset" class="form-select form-select-sm" @change="applyPreset">
              <option :value="7">Last 7 days</option>
              <option :value="14">Last 14 days</option>
              <option :value="30">Last 30 days</option>
              <option :value="0">Custom</option>
            </select>
          </div>
          <div class="col-auto">
            <label class="form-label small text-muted mb-1">From</label>
            <input type="date" v-model="localFromDate" class="form-control form-control-sm" @change="handleDateChange" />
          </div>
          <div class="col-auto">
            <label class="form-label small text-muted mb-1">To</label>
            <input type="date" v-model="localToDate" class="form-control form-control-sm" :max="store.todayDate" @change="handleDateChange" />
          </div>
          <div class="col-auto">
            <label class="form-label small text-muted mb-1">Sort</label>
            <select v-model="sortBy" class="form-select form-select-sm">
              <option value="date">By Date</option>
              <option value="journal">By Journal</option>
            </select>
          </div>
        </div>
        <!-- Article count, limit warning, and export buttons -->
        <div class="d-flex justify-content-between align-items-center mt-2 pt-2 border-top flex-wrap gap-2">
          <div class="d-flex align-items-center gap-3">
            <small v-if="store.articles.length >= 500" class="text-warning">
              ⚠️ Limited to newest 500 articles
            </small>
            <small class="text-muted">
              Showing {{ filteredArticles.length }} of {{ store.articles.length }} articles
            </small>
          </div>
          <!-- Selection toggle and bulk export -->
          <div class="d-flex align-items-center gap-2">
            <button 
              class="btn btn-sm" 
              :class="selectionMode ? 'btn-primary' : 'btn-outline-secondary'"
              @click="toggleSelectionMode"
              v-if="filteredArticles.length > 0"
            >
              {{ selectionMode ? '✓ Selection Mode (' + selectedArticles.length + ')' : '☐ Select' }}
            </button>
            <button 
              v-if="selectionMode && selectedArticles.length > 0"
              class="btn btn-sm btn-outline-danger"
              @click="selectedArticles = []"
            >
              Clear
            </button>
            <!-- Export dropdown for selected articles -->
            <div class="dropdown" v-if="selectionMode && selectedArticles.length > 0">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                Export Selected
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('txt')">📄 TXT</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('ris')">📋 RIS</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('nbib')">📑 NBIB</a></li>
              </ul>
            </div>
            <!-- Export dropdown for all articles -->
            <div class="dropdown" v-else-if="filteredArticles.length > 0 && !selectionMode">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                Export
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#" @click.prevent="exportAllArticles('txt')">📄 TXT</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportAllArticles('ris')">📋 RIS</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportAllArticles('nbib')">📑 NBIB</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="store.loading && store.articles.length === 0" class="text-center py-5">
        <div class="spinner-border text-light" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-white mt-3">Fetching latest articles...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredArticles.length === 0" class="text-center py-5">
        <div class="card p-5">
          <h4>No articles found</h4>
          <p class="text-muted">{{ store.articles.length === 0 ? 'No new articles from your selected journals in this time period.' : 'Try adjusting your search or journal filters.' }}</p>
          <button v-if="selectedJournals.length > 0" class="btn btn-outline-primary mt-2" @click="selectedJournals = []">
            Clear Journal Filters
          </button>
        </div>
      </div>

      <!-- Articles Grid -->
      <div v-else class="row g-4">
        <div v-for="article in filteredArticles" :key="article.pmid" class="col-md-6 col-lg-4">
          <div 
            class="card article-card h-100" 
            :class="{ 
              'clickable-card': !selectionMode,
              'selected-card': selectedArticles.includes(String(article.pmid))
            }"
            @click="handleCardClick(article.pmid)"
          >
            <!-- Selection checkbox overlay -->
            <div v-if="selectionMode" class="selection-checkbox">
              <input 
                type="checkbox" 
                class="form-check-input" 
                :checked="selectedArticles.includes(String(article.pmid))"
                @click.stop="handleCardClick(article.pmid)"
              />
            </div>
            <div class="card-body d-flex flex-column">
              <span class="badge-journal mb-3 align-self-start">
                {{ article.journal }}
              </span>
              <h6 class="card-title fw-bold">{{ article.title }}</h6>
              <p class="card-text text-muted small mb-2">
                {{ article.authors?.slice(0, 3).join(', ') }}{{ article.authors?.length > 3 ? ' et al.' : '' }}
              </p>
              <p v-if="article.abstract" class="card-text text-muted small flex-grow-1 abstract-preview">
                {{ truncateAbstract(article.abstract) }}
              </p>
              <div class="d-flex justify-content-between align-items-center mt-3 pt-3 border-top">
                <small class="text-muted">{{ article.pub_date }}</small>
                <span v-if="!selectionMode" class="btn btn-sm btn-outline-primary">
                  View Details →
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../stores/dashboard'

const router = useRouter()
const store = useDashboardStore()

// Local state (not persisted across navigations)
const searchQuery = ref('')
const sortBy = ref('date')
const selectedJournals = ref([])
const selectionMode = ref(false)
const selectedArticles = ref([])

// Local date refs for v-model binding (sync with store)
const localFromDate = ref(store.fromDate)
const localToDate = ref(store.toDate)

// Sync local dates with store
watch(() => store.fromDate, (val) => { localFromDate.value = val })
watch(() => store.toDate, (val) => { localToDate.value = val })

// Show all profile journals in dropdown (with article count)
const availableJournals = computed(() => {
  const articleCounts = {}
  store.articles.forEach(a => {
    const key = a.journal.toLowerCase()
    articleCounts[key] = (articleCounts[key] || 0) + 1
  })
  
  return store.profileJournals.map(j => {
    const nameKey = j.name.toLowerCase()
    const abbrKey = j.iso_abbreviation?.toLowerCase() || ''
    const count = articleCounts[nameKey] || articleCounts[abbrKey] || 0
    return { name: j.name, count }
  }).sort((a, b) => a.name.localeCompare(b.name))
})

const filteredArticles = computed(() => {
  let result = [...store.articles]
  
  // Filter by selected journals
  if (selectedJournals.value.length > 0) {
    result = result.filter(a => selectedJournals.value.includes(a.journal))
  }
  
  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(a => 
      a.title.toLowerCase().includes(query) || 
      a.abstract?.toLowerCase().includes(query) ||
      a.journal.toLowerCase().includes(query)
    )
  }
  
  // Sort
  if (sortBy.value === 'date') {
    result.sort((a, b) => b.pub_date.localeCompare(a.pub_date))
  } else if (sortBy.value === 'journal') {
    result.sort((a, b) => a.journal.localeCompare(b.journal))
  }
  
  return result
})

function truncateAbstract(text, maxLength = 150) {
  if (!text || text.length <= maxLength) return text
  return text.substring(0, maxLength).trim() + '...'
}

function selectProfile(profileId) {
  store.setProfile(profileId)
  selectedJournals.value = []
  // Fetch articles since profile changed
  loadData()
}

function toggleJournalFilter(journalName) {
  const idx = selectedJournals.value.indexOf(journalName)
  if (idx === -1) {
    selectedJournals.value.push(journalName)
  } else {
    selectedJournals.value.splice(idx, 1)
  }
}

function applyPreset() {
  store.applyPreset(store.daysPreset)
  if (store.daysPreset > 0) {
    loadData()
  }
}

function handleDateChange() {
  store.setDateRange(localFromDate.value, localToDate.value)
  store.daysPreset = 0
  loadData()
}

async function refreshArticles() {
  selectedJournals.value = []
  await store.fetchArticles(true) // Force refresh
}

async function loadData() {
  await store.loadProfileJournals()
  await store.fetchArticles() // Will use cache if available
}

onMounted(async () => {
  console.log('Dashboard mounted - hasCache:', store.hasCache, 'hasLoadedArticles:', store.hasLoadedArticles, 'articles:', store.articles.length)
  console.log('Scroll position from store:', store.scrollPosition)
  const savedScroll = store.scrollPosition  // Capture before async ops
  
  await store.loadProfiles()
  if (store.selectedProfileId) {
    await loadData()
  }
  console.log('Dashboard load complete - articles:', store.articles.length)
  
  // Restore scroll position after DOM updates (use setTimeout for reliable timing)
  if (savedScroll > 0) {
    setTimeout(() => {
      window.scrollTo(0, savedScroll)
      console.log('Restored scroll to:', savedScroll)
    }, 100)
  }
})

// Save scroll position before leaving Dashboard (for any navigation)
onBeforeUnmount(() => {
  store.saveScrollPosition()
  console.log('Dashboard unmounting - saved scroll position')
})

// Open article detail view
function openArticle(pmid) {
  store.saveScrollPosition()  // Save scroll before leaving
  sessionStorage.setItem('dashboardArticles', JSON.stringify(filteredArticles.value))
  router.push(`/article/${pmid}`)
}

// Selection mode functions
function toggleSelectionMode() {
  selectionMode.value = !selectionMode.value
  if (!selectionMode.value) {
    selectedArticles.value = []
  }
}

function handleCardClick(pmid) {
  if (selectionMode.value) {
    const pmidStr = String(pmid)
    const idx = selectedArticles.value.indexOf(pmidStr)
    if (idx === -1) {
      selectedArticles.value.push(pmidStr)
    } else {
      selectedArticles.value.splice(idx, 1)
    }
  } else {
    openArticle(pmid)
  }
}

function exportSelectedArticles(format) {
  const selectedList = filteredArticles.value.filter(a => selectedArticles.value.includes(a.pmid))
  if (!selectedList.length) return
  
  let content = ''
  let filename = `selected_articles_${selectedArticles.value.length}`
  
  if (format === 'txt') {
    content = selectedList.map(a => 
      `Title: ${a.title}\nAuthors: ${a.authors?.join(', ') || 'N/A'}\nJournal: ${a.journal}\nDate: ${a.pub_date}\nPMID: ${a.pmid}\nDOI: ${a.doi || 'N/A'}\nAbstract: ${a.abstract || 'N/A'}\nURL: ${a.pubmed_url}\n${'='.repeat(80)}`
    ).join('\n\n')
    filename += '.txt'
  } else if (format === 'ris') {
    content = selectedList.map(a => 
      `TY  - JOUR\nTI  - ${a.title}\n${a.authors?.map(auth => `AU  - ${auth}`).join('\n') || ''}\nJO  - ${a.journal}\nPY  - ${a.pub_date?.split('-')[0] || ''}\nAB  - ${a.abstract || ''}\nDO  - ${a.doi || ''}\nAN  - ${a.pmid}\nUR  - ${a.pubmed_url}\nER  - `
    ).join('\n\n')
    filename += '.ris'
  } else if (format === 'nbib') {
    content = selectedList.map(a => 
      `PMID- ${a.pmid}\nTI  - ${a.title}\n${a.authors?.map(auth => `FAU - ${auth}`).join('\n') || ''}\nJT  - ${a.journal}\nDP  - ${a.pub_date || ''}\nAB  - ${a.abstract || ''}\nAID - ${a.doi || ''} [doi]\nSO  - ${a.journal}. ${a.pub_date}.`
    ).join('\n\n')
    filename += '.nbib'
  }
  
  const blob = new Blob([content], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

function exportAllArticles(format) {
  const articlesList = filteredArticles.value
  if (!articlesList.length) return
  
  let content = ''
  let filename = `articles_${store.fromDate}_${store.toDate}`
  
  if (format === 'txt') {
    content = articlesList.map(a => 
      `Title: ${a.title}\nAuthors: ${a.authors?.join(', ') || 'N/A'}\nJournal: ${a.journal}\nDate: ${a.pub_date}\nPMID: ${a.pmid}\nAbstract: ${a.abstract || 'N/A'}\nURL: ${a.pubmed_url}\n${'='.repeat(80)}`
    ).join('\n\n')
    filename += '.txt'
  } else if (format === 'ris') {
    content = articlesList.map(a => 
      `TY  - JOUR\nTI  - ${a.title}\n${a.authors?.map(auth => `AU  - ${auth}`).join('\n') || ''}\nJO  - ${a.journal}\nPY  - ${a.pub_date?.split('-')[0] || ''}\nAB  - ${a.abstract || ''}\nAN  - ${a.pmid}\nUR  - ${a.pubmed_url}\nER  - `
    ).join('\n\n')
    filename += '.ris'
  } else if (format === 'nbib') {
    content = articlesList.map(a => 
      `PMID- ${a.pmid}\nTI  - ${a.title}\n${a.authors?.map(auth => `FAU - ${auth}`).join('\n') || ''}\nJT  - ${a.journal}\nDP  - ${a.pub_date || ''}\nAB  - ${a.abstract || ''}\nSO  - ${a.journal}. ${a.pub_date}.`
    ).join('\n\n')
    filename += '.nbib'
  }
  
  const blob = new Blob([content], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.abstract-preview {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Ensure dropdown appears above article cards */
.card:has(.dropdown) {
  position: relative;
  z-index: 100;
}

.dropdown-menu {
  z-index: 1050;
}

/* Clickable article cards */
.clickable-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.clickable-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

/* Selection mode */
.article-card {
  position: relative;
}

.selection-checkbox {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
}

.selection-checkbox .form-check-input {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.selected-card {
  border: 2px solid #0d6efd;
  background: rgba(13, 110, 253, 0.05);
}
</style>
