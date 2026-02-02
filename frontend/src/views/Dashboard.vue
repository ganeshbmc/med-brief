<template>
  <div class="container" :class="preferencesClasses">
    <section class="masthead">
      <div class="d-flex flex-column flex-lg-row align-items-start align-items-lg-center justify-content-between gap-3">
        <div>
          <h1 class="masthead-title">Your research brief</h1>
          <p class="masthead-subtitle">{{ formatDateRange(store.fromDate, store.toDate) }} · Curated from your profile journals</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <button
            class="btn btn-light btn-sm d-inline-flex align-items-center gap-2"
            @click="refreshArticles"
            :disabled="store.loading"
            aria-label="Refresh articles"
          >
            <span v-if="store.loading" class="spinner-border spinner-border-sm"></span>
            <RefreshCw v-else :size="16" />
            Refresh
          </button>
          <router-link class="btn btn-outline-terracotta btn-sm" to="/profiles">Manage profiles</router-link>
        </div>
      </div>
      <div class="summary-grid mt-4">
        <div class="summary-tile">
          <div class="summary-label">Active profile</div>
          <div class="dropdown">
            <button
              class="btn btn-link text-decoration-none p-0 fw-semibold text-terracotta dropdown-toggle summary-value summary-value--clamp text-start"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ store.currentProfile?.name || 'None' }}
            </button>
            <ul class="dropdown-menu">
              <li v-for="p in store.profiles" :key="p.id">
                <button
                  type="button"
                  class="dropdown-item d-flex align-items-center justify-content-between w-100"
                  :class="{ active: store.selectedProfileId === p.id }"
                  @click="selectProfile(p.id)"
                >
                  {{ p.name }}
                  <Check v-if="store.selectedProfileId === p.id" :size="16" class="text-success" />
                </button>
              </li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <router-link class="dropdown-item text-terracotta fw-semibold d-flex align-items-center gap-2" to="/onboarding">
                  <Plus :size="16" />
                  Create New Profile
                </router-link>
              </li>
            </ul>
          </div>
        </div>
        <div class="summary-tile">
          <div class="summary-label">Journals tracked</div>
          <div class="summary-value">{{ store.currentProfile?.journal_ids?.length || 0 }}</div>
        </div>
        <div class="summary-tile">
          <div class="summary-label">Articles in range</div>
          <div class="summary-value">{{ filteredArticles.length }}</div>
        </div>
        <div class="summary-tile">
          <div class="summary-label">Abstracts available</div>
          <div class="summary-value">{{ articlesWithAbstract.length }}</div>
        </div>
      </div>
    </section>

    <!-- Loading Profiles State -->
    <div v-if="store.loadingProfiles" class="loading-state">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted">Preparing your brief settings...</p>
    </div>

    <!-- Profiles Error State -->
    <div v-else-if="store.profilesError" class="empty-state">
      <AlertTriangle :size="48" class="icon-muted text-warning" />
      <h4>We couldn't load your profiles</h4>
      <p class="text-muted">{{ store.profilesError }}</p>
      <div class="d-flex align-items-center gap-2">
        <button class="btn btn-primary" @click="retryProfiles">Retry</button>
        <router-link v-if="!authStore.isAuthenticated" to="/login" class="btn btn-outline-secondary">Sign In</router-link>
      </div>
    </div>

    <!-- No Profiles State -->
    <div v-else-if="store.profiles.length === 0" class="empty-state">
      <FileText :size="48" class="icon-muted" />
      <h4>Welcome to MedBrief!</h4>
      <p class="text-muted">You haven't created any profiles yet. Create one to start receiving personalized research briefs.</p>
      <router-link to="/onboarding" class="btn btn-primary">Create Your First Profile</router-link>
    </div>

    <!-- Main Content -->
    <template v-else>
      <!-- Filters -->
      <div class="section-card mb-4">
        <div class="filter-grid">
          <div>
            <label class="form-label small text-muted mb-2">Search</label>
            <div class="input-icon">
              <Search :size="18" class="icon-muted" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search articles, journals, abstracts"
                aria-label="Search articles"
              />
            </div>
          </div>
          <div>
            <label class="form-label small text-muted mb-2">Journal filter</label>
            <div class="dropdown">
              <button 
                class="btn btn-outline-secondary w-100 dropdown-toggle text-start d-flex align-items-center gap-2" 
                type="button" 
                data-bs-toggle="dropdown"
                data-bs-auto-close="outside"
              >
                <Newspaper :size="18" />
                {{ selectedJournals.length ? `${selectedJournals.length} journal(s)` : 'All journals' }}
              </button>
              <ul class="dropdown-menu journal-filter-dropdown" style="min-width: 320px; max-height: 360px; overflow-y: auto;">
                <li>
                  <button type="button" class="dropdown-item w-100 text-start" @click="selectedJournals = []">
                    <em>Clear filters</em>
                  </button>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li v-for="journal in availableJournals" :key="journal.name">
                  <button 
                    type="button"
                    class="dropdown-item d-flex align-items-center justify-content-between w-100" 
                    :class="{ 'text-muted': !journal.hasData }"
                    @click="toggleJournalFilter(journal.name)"
                    :title="!journal.hasData ? 'No articles found for this journal in the selected time period' : journal.name"
                    :disabled="!journal.hasData"
                  >
                    <span class="d-flex align-items-center flex-grow-1">
                      <input 
                        type="checkbox" 
                        class="form-check-input me-2 flex-shrink-0" 
                        :checked="selectedJournals.includes(journal.name)"
                        @change="toggleJournalFilter(journal.name)"
                        @click.stop
                        :disabled="!journal.hasData"
                      />
                      <span class="journal-name">{{ journal.name }}</span>
                      <AlertTriangle v-if="!journal.hasData" :size="14" class="ms-2 text-warning flex-shrink-0" />
                    </span>
                    <span class="badge ms-2 flex-shrink-0" :class="journal.count ? 'bg-primary' : 'bg-secondary'">{{ journal.count }}</span>
                  </button>
                </li>
              </ul>
            </div>
          </div>
          <div>
            <label class="form-label small text-muted mb-2">Quick range</label>
            <select v-model="store.daysPreset" class="form-select form-select-sm" @change="applyPreset">
              <option :value="1">Last 24 hours</option>
              <option :value="3">Last 3 days</option>
              <option :value="7">Last 7 days</option>
              <option :value="14">Last 14 days</option>
              <option :value="30">Last 30 days</option>
              <option :value="0">Custom</option>
            </select>
          </div>
          <div>
            <label class="form-label small text-muted mb-2">Sort</label>
            <select v-model="sortBy" class="form-select form-select-sm">
              <option value="date">By Date</option>
              <option value="journal">By Journal</option>
            </select>
          </div>
          <div>
            <label class="form-label small text-muted mb-2">From</label>
            <input
              type="date"
              v-model="localFromDate"
              class="form-control form-control-sm"
              @change="handleDateChange"
              aria-label="From date"
            />
          </div>
          <div>
            <label class="form-label small text-muted mb-2">To</label>
            <input
              type="date"
              v-model="localToDate"
              class="form-control form-control-sm"
              :max="store.todayDate"
              @change="handleDateChange"
              aria-label="To date"
            />
          </div>
          <div class="filter-toggle mt-2">
            <div class="form-check form-switch">
              <input
                type="checkbox"
                class="form-check-input"
                id="abstractOnly"
                v-model="showAbstractOnly"
              />
              <label class="form-check-label small text-warm-dark fw-medium" for="abstractOnly">
                Has abstract
              </label>
            </div>
            <span class="badge-soft">{{ articlesWithAbstract.length }} available</span>
          </div>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-4 pt-3 border-top flex-wrap gap-2">
          <div class="d-flex align-items-center gap-3">
            <small v-if="store.articles.length >= 500" class="text-warning d-flex align-items-center gap-1">
              <AlertTriangle :size="16" />
              Limited to newest 500 articles
            </small>
            <small class="text-muted">
              Showing {{ filteredArticles.length }} of {{ store.articles.length }} articles
              <span v-if="showAbstractOnly" class="text-terracotta-600">
                (with abstracts)
              </span>
            </small>
          </div>
          <div class="d-flex align-items-center gap-2">
            <button 
              class="btn btn-sm d-flex align-items-center gap-1" 
              :class="selectionMode ? 'btn-primary' : 'btn-outline-secondary'"
              @click="toggleSelectionMode"
              v-if="filteredArticles.length > 0"
            >
              <CheckSquare v-if="selectionMode" :size="16" />
              <Square v-else :size="16" />
              {{ selectionMode ? 'Selection (' + selectedArticles.length + ')' : 'Select' }}
            </button>
            <button 
              v-if="selectionMode"
              class="btn btn-sm btn-outline-secondary d-flex align-items-center gap-1"
              @click="selectAllArticles"
            >
              <CheckSquare :size="16" />
              Select All
            </button>
            <button 
              v-if="selectionMode && selectedArticles.length > 0"
              class="btn btn-sm btn-outline-danger d-flex align-items-center gap-1"
              @click="clearSelection"
            >
              <X :size="16" />
              Clear
            </button>
            <div class="dropdown" v-if="selectionMode && selectedArticles.length > 0">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1" type="button" data-bs-toggle="dropdown">
                <Download :size="16" />
                Export Selected
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('pdf')"><File :size="16" class="me-1" />PDF</button></li>
                <li><hr class="dropdown-divider"></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('txt')">TXT</button></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('ris')">RIS</button></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('nbib')">NBIB</button></li>
                <li><hr class="dropdown-divider"></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="shareSelectedArticles">
                  <Share2 :size="16" class="me-1" />Share
                </button></li>
              </ul>
            </div>
            <div class="dropdown" v-else-if="filteredArticles.length > 0 && !selectionMode">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1" type="button" data-bs-toggle="dropdown">
                <Download :size="16" />
                Export
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportAllArticles('pdf')"><File :size="16" class="me-1" />PDF</button></li>
                <li><hr class="dropdown-divider"></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportAllArticles('txt')">TXT</button></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportAllArticles('ris')">RIS</button></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="exportAllArticles('nbib')">NBIB</button></li>
                <li><hr class="dropdown-divider"></li>
                <li><button type="button" class="dropdown-item w-100 text-start" @click="shareAllArticles">
                  <Share2 :size="16" class="me-1" />Share
                </button></li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="store.loading && store.articles.length === 0" class="loading-state">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted">Fetching the latest articles...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredArticles.length === 0" class="empty-state">
        <FileText :size="48" class="icon-muted" />
        <h4>No articles found</h4>
        <p class="text-muted">{{ store.articles.length === 0 ? 'No new articles from your selected journals in this time period.' : 'Try adjusting your search or journal filters.' }}</p>
        <button v-if="selectedJournals.length > 0" class="btn btn-outline-primary" @click="selectedJournals = []">
          Clear Journal Filters
        </button>
      </div>

      <!-- Articles Grid -->
        <div v-else class="row g-4 mb-5">
          <div v-for="article in filteredArticles" :key="article.pmid" class="col-md-6 col-lg-4">
            <div 
              class="card article-card h-100 card-hover-lift" 
              :class="{ 
                'clickable-card': !selectionMode,
                'selected-card': selectedArticles.includes(String(article.pmid))
              }"
              @click="handleCardClick(article.pmid)"
            >
              <div v-if="selectionMode" class="selection-checkbox">
                <input 
                  type="checkbox" 
                  class="form-check-input" 
                  :checked="selectedArticles.includes(String(article.pmid))"
                  @click.stop="handleCardClick(article.pmid)"
                />
              </div>
              <div class="card-body d-flex flex-column">
                <div class="d-flex align-items-center gap-2 flex-wrap mb-3">
                  <span class="badge-journal">{{ article.journal }}</span>
                </div>
                <h6 class="card-title text-warm-dark">{{ article.title }}</h6>
                <div class="article-meta mb-2">
                  <span>{{ article.authors?.slice(0, 3).join(', ') }}{{ article.authors?.length > 3 ? ' et al.' : '' }}</span>
                </div>
              <p v-if="article.abstract" class="card-text text-muted small flex-grow-1 abstract-preview">
                <span v-if="article.abstract_source === 'publisher'" class="badge-soft me-2">Publisher Abstract</span>
                {{ truncateAbstract(article.abstract) }}
              </p>
                <div class="article-actions mt-3">
                  <small class="text-muted d-flex align-items-center gap-1">
                    <Calendar :size="14" />
                    {{ formatDateDisplay(article.pub_date) }}
                  </small>
                  <span v-if="!selectionMode" class="btn btn-sm btn-outline-primary d-inline-flex align-items-center gap-1">
                    View <ArrowRight :size="14" />
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
    </template>
  </div>

  <!-- Sticky Selection Bar (Moved outside container for better full-width handling) -->
  <div 
    v-if="selectionMode && selectedArticles.length > 0" 
    class="sticky-selection-bar d-flex justify-content-center justify-content-sm-between align-items-center flex-wrap gap-2"
  >
    <div class="d-flex align-items-center gap-2 gap-sm-3">
      <span class="fw-bold text-warm-dark">{{ selectedArticles.length }} <span class="d-none d-md-inline">selected</span></span>
      <button class="btn btn-sm btn-outline-danger" @click="clearSelection">Cancel</button>
    </div>
    <div class="dropdown">
      <button class="btn btn-primary btn-sm dropdown-toggle d-flex align-items-center gap-1" type="button" data-bs-toggle="dropdown">
        <Download :size="16" />
        Export <span class="d-none d-md-inline">Selected</span> ({{ selectedArticles.length }})
      </button>
      <ul class="dropdown-menu dropdown-menu-end">
        <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('pdf')"><File :size="16" class="me-1" />PDF</button></li>
        <li><hr class="dropdown-divider"></li>
        <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('txt')">TXT</button></li>
         <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('ris')">RIS</button></li>
        <li><button type="button" class="dropdown-item w-100 text-start" @click="exportSelectedArticles('nbib')">NBIB</button></li>
        <li><hr class="dropdown-divider"></li>
        <li><button type="button" class="dropdown-item w-100 text-start" @click="shareSelectedArticles">
          <Share2 :size="16" class="me-1" />Share
        </button></li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../stores/dashboard'
import { useAuthStore } from '../stores/auth'
import { formatDateDisplay, formatDateRange } from '@/utils/dateFormatter'
import {
  FileText, Check, Plus, RefreshCw, Search, Newspaper,
  AlertTriangle, CheckSquare, Square, X, Download,
  Calendar, ArrowRight, Share2, File
} from 'lucide-vue-next'
import { generateArticlesShareText, shareContent, useToast } from '@/utils/shareUtils'
import { exportToPdf } from '../services/api'

const router = useRouter()
const store = useDashboardStore()
const authStore = useAuthStore()
const { show } = useToast()

// User preferences classes
const preferencesClasses = computed(() => {
  const prefs = authStore.preferences || {}
  return {
    'font-small': prefs.fontSize === 'small',
    'font-medium': prefs.fontSize === 'medium' || !prefs.fontSize,
    'font-large': prefs.fontSize === 'large',
    'line-normal': prefs.lineSpacing === 'normal' || !prefs.lineSpacing,
    'line-relaxed': prefs.lineSpacing === 'relaxed',
  }
})

// Get default days from user preferences
const defaultDays = computed(() => authStore.preferences?.defaultDays || 7)

// Local state (not persisted across navigations)
const searchQuery = ref('')
const sortBy = ref('date')
const selectedJournals = ref([])
const selectionMode = ref(false)
const selectedArticles = ref([])

// Abstract filter state
const showAbstractOnly = ref(false)

// Local date refs for v-model binding (sync with store)
const localFromDate = ref(store.fromDate)
const localToDate = ref(store.toDate)

// Sync local dates with store
watch(() => store.fromDate, (val) => { localFromDate.value = val })
watch(() => store.toDate, (val) => { localToDate.value = val })

// Enhanced journal name normalization for robust matching
function normalizeJournalName(name) {
  if (!name) return ''
  return name.toLowerCase()
    .trim()
    .replace(/\s+/g, ' ')              // Normalize whitespace
    .replace(/\([^)]*\)/g, '')         // Remove content in parentheses (e.g., "heart (british cardiac society)" → "heart")
    .replace(/[.,;:]/g, '')            // Remove all punctuation
    .replace(/&/g, 'and')              // Normalize ampersands
    .replace(/^the\s+/, '')            // Remove leading "the"
    .replace(/\b(journal of|journal)\b/g, '') // Remove common words
    .replace(/\s+/g, ' ')              // Clean up spaces again
    .trim()
}

// Show all profile journals in dropdown (with article count)
// Uses enhanced ISSN and name matching for robust badge counting
const availableJournals = computed(() => {
  // Build comprehensive lookup maps from normalized names/abbreviations → ISSN and journal data
  const nameToIssn = {}
  const nameToJournal = {} // Map normalized names to full journal data
  const normalizedNames = new Set()
  
  store.profileJournals.forEach(j => {
    // Map normalized full name
    const normName = normalizeJournalName(j.name)
    normalizedNames.add(normName)
    nameToIssn[normName] = j.issn
    nameToJournal[normName] = j
    
    // Map normalized abbreviation if available
    if (j.iso_abbreviation) {
      const normAbbr = normalizeJournalName(j.iso_abbreviation)
      nameToIssn[normAbbr] = j.issn
      nameToJournal[normAbbr] = j
    }
    
    // Add additional common variations for better matching
    const variations = generateJournalVariations(j.name)
    variations.forEach(variation => {
      const normVar = normalizeJournalName(variation)
      if (!nameToIssn[normVar]) {
        nameToIssn[normVar] = j.issn
        nameToJournal[normVar] = j
      }
    })
  })
  
  // Count articles with enhanced matching
  const articleCountsByIssn = {}
  const articleCountsByName = {} // Fallback count by normalized name
  const unmatchedJournals = [] // Track unmatched for debugging
  
  store.articles.forEach(a => {
    const originalJournal = a.journal
    const journalKey = normalizeJournalName(originalJournal)
    const issn = nameToIssn[journalKey]
    
    if (issn) {
      // Primary match via ISSN
      articleCountsByIssn[issn] = (articleCountsByIssn[issn] || 0) + 1
    } else if (nameToJournal[journalKey]) {
      // Secondary match via normalized name (journal without ISSN)
      articleCountsByName[journalKey] = (articleCountsByName[journalKey] || 0) + 1
    } else {
      // Unmatched journal
      unmatchedJournals.push({
        original: originalJournal,
        normalized: journalKey
      })
    }
  })
  
  // Enhanced debug logging in development
  if (import.meta.env.DEV && unmatchedJournals.length > 0) {
    console.group(`[Journal Matching] ${unmatchedJournals.length} unmatched articles`)
    unmatchedJournals.forEach(({original, normalized}) => {
      console.log(`Original: "${original}" → Normalized: "${normalized}"`)
      console.log(`Available normalized names:`, Array.from(normalizedNames))
    })
    console.groupEnd()
  }
  
  return store.profileJournals.map(j => {
    const normName = normalizeJournalName(j.name)
    // Use ISSN count if available, otherwise fall back to name count
    const count = j.issn 
      ? (articleCountsByIssn[j.issn] || 0) 
      : (articleCountsByName[normName] || 0)
    
    return { 
      name: j.name, 
      issn: j.issn || '',
      isoAbbr: j.iso_abbreviation || '',
      count,
      hasData: count > 0
    }
  }).sort((a, b) => b.count - a.count || a.name.localeCompare(b.name))
})

// Generate common journal name variations for better matching
function generateJournalVariations(name) {
  const variations = []
  const lowerName = name.toLowerCase()
  
  // Add version without "The" prefix
  if (lowerName.startsWith('the ')) {
    variations.push(name.substring(4))
  }
  
  // Add version with "The" prefix if not already present
  if (!lowerName.startsWith('the ') && !lowerName.includes(' the ')) {
    variations.push(`The ${name}`)
  }
  
  // Add version without "Journal of" prefix
  if (lowerName.includes('journal of')) {
    const withoutJournalOf = name.replace(/^(the\s+)?journal\s+of\s+/i, '$1')
    variations.push(withoutJournalOf)
  }
  
  return variations
}

const filteredArticles = computed(() => {
  let result = [...store.articles]
  
  // Filter by selected journals using the same enhanced matching logic as badge counting
  if (selectedJournals.value.length > 0) {
    // Build comprehensive lookup maps (same logic as availableJournals)
    const nameToIssn = {}
    const nameToJournal = {}
    
    store.profileJournals.forEach(j => {
      // Map normalized full name
      const normName = normalizeJournalName(j.name)
      nameToIssn[normName] = j.issn
      nameToJournal[normName] = j
      
      // Map normalized abbreviation if available
      if (j.iso_abbreviation) {
        const normAbbr = normalizeJournalName(j.iso_abbreviation)
        nameToIssn[normAbbr] = j.issn
        nameToJournal[normAbbr] = j
      }
      
      // Add variations for better matching
      const variations = generateJournalVariations(j.name)
      variations.forEach(variation => {
        const normVar = normalizeJournalName(variation)
        if (!nameToIssn[normVar]) {
          nameToIssn[normVar] = j.issn
          nameToJournal[normVar] = j
        }
      })
    })
    
    // Get selected journal identifiers (both ISSN and normalized names)
    const selectedIssns = new Set()
    const selectedNames = new Set()
    
    selectedJournals.value.forEach(selectedName => {
      const journal = store.profileJournals.find(j => j.name === selectedName)
      if (journal?.issn) {
        selectedIssns.add(journal.issn)
      }
      // Add normalized name for fallback matching
      selectedNames.add(normalizeJournalName(selectedName))
    })
    
    // Enhanced filtering: ISSN-first with name fallback (consistent with badge counting)
    result = result.filter(a => {
      const journalKey = normalizeJournalName(a.journal)
      const articleIssn = nameToIssn[journalKey]
      const matchedJournal = nameToJournal[journalKey]
      
      // Primary match: ISSN-based
      if (articleIssn && selectedIssns.has(articleIssn)) {
        return true
      }
      
      // Secondary match: Name-based for journals without ISSN
      if (matchedJournal && !matchedJournal.issn && selectedNames.has(journalKey)) {
        return true
      }
      
      // Fallback: Check if article journal matches any selected journal by name
      return selectedJournals.value.some(selectedName => {
        const selectedNorm = normalizeJournalName(selectedName)
        const selectedJournal = store.profileJournals.find(j => j.name === selectedName)
        
        // Direct name match
        if (journalKey === selectedNorm) return true
        
        // Match via variations
        const variations = generateJournalVariations(selectedJournal?.name || selectedName)
        return variations.some(variation => normalizeJournalName(variation) === journalKey)
      })
    })
    
    // Debug logging for filtering in development
    if (import.meta.env.DEV) {
      const originalCount = store.articles.length
      const filteredCount = result.length
      console.log(`[Article Filtering] ${originalCount} → ${filteredCount} articles (${selectedJournals.value.length} journals selected)`)
    }
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

   // Filter by abstract availability
   if (showAbstractOnly.value) {
     result = result.filter(a => a.abstract && a.abstract.trim().length > 0)
   }

   // Sort
  if (sortBy.value === 'date') {
    result.sort((a, b) => b.pub_date.localeCompare(a.pub_date))
  } else if (sortBy.value === 'journal') {
    result.sort((a, b) => a.journal.localeCompare(b.journal))
  }
  
   return result
})

// Count of articles with abstracts available
const articlesWithAbstract = computed(() => {
  return store.articles.filter(a => a.abstract && a.abstract.trim().length > 0)
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

async function retryProfiles() {
  await store.loadProfiles(true)
  if (store.selectedProfileId) {
    await loadData()
  }
}

onMounted(async () => {
  console.log('Dashboard mounted - hasCache:', store.hasCache, 'hasLoadedArticles:', store.hasLoadedArticles, 'articles:', store.articles.length)
  console.log('Scroll position from store:', store.scrollPosition)
  const savedScroll = store.scrollPosition
  
  // Initialize date range from user preferences BEFORE loading profiles
  store.initializeDateRange()
  
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
  sessionStorage.setItem('selectedProfileId', store.selectedProfileId)
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
      // Issue #32: Exit selection mode if no articles are selected
      if (selectedArticles.value.length === 0) {
        selectionMode.value = false
      }
    }
  } else {
    openArticle(pmid)
  }
}

function selectAllArticles() {
  selectedArticles.value = filteredArticles.value.map(a => String(a.pmid))
}

function clearSelection() {
  selectedArticles.value = []
  selectionMode.value = false
}

function getAbstractLabel(article) {
  return article?.abstract_source === 'publisher' ? 'Publisher Abstract' : 'Abstract'
}

async function exportSelectedArticles(format) {
  const selectedList = filteredArticles.value.filter(a => selectedArticles.value.includes(a.pmid))
  if (!selectedList.length) return

  if (format === 'pdf') {
    try {
      const blob = await exportToPdf(store.selectedProfileId, {
        fromDate: store.fromDate,
        toDate: store.toDate,
        articleIds: selectedList.map(a => a.pmid).join(',')
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `selected_articles_${selectedArticles.value.length}.pdf`
      link.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      console.error('PDF export failed:', e)
      show('PDF export failed', 'error')
    }
    return
  }

  let content = ''
  let filename = `selected_articles_${selectedArticles.value.length}`

  if (format === 'txt') {
    content = selectedList.map(a => {
      const abstractLabel = getAbstractLabel(a)
      return `Title: ${a.title}\nAuthors: ${a.authors?.join(', ') || 'N/A'}\nJournal: ${a.journal}\nDate: ${formatDateDisplay(a.pub_date)}\nPMID: ${a.pmid}\nDOI: ${a.doi || 'N/A'}\n${abstractLabel}: ${a.abstract || 'N/A'}\nURL: ${a.pubmed_url}\n${'='.repeat(80)}`
    }).join('\n\n')
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

async function exportAllArticles(format) {
  const articlesList = filteredArticles.value
  if (!articlesList.length) return

  if (format === 'pdf') {
    try {
      const blob = await exportToPdf(store.selectedProfileId, {
        fromDate: store.fromDate,
        toDate: store.toDate
      })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `articles_${store.fromDate}_${store.toDate}.pdf`
      link.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      console.error('PDF export failed:', e)
      show('PDF export failed', 'error')
    }
    return
  }

  let content = ''
  let filename = `articles_${store.fromDate}_${store.toDate}`

  if (format === 'txt') {
    content = articlesList.map(a => {
      const abstractLabel = getAbstractLabel(a)
      return `Title: ${a.title}\nAuthors: ${a.authors?.join(', ') || 'N/A'}\nJournal: ${a.journal}\nDate: ${formatDateDisplay(a.pub_date)}\nPMID: ${a.pmid}\n${abstractLabel}: ${a.abstract || 'N/A'}\nURL: ${a.pubmed_url}\n${'='.repeat(80)}`
    }).join('\n\n')
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

async function shareSelectedArticles() {
  const selectedList = filteredArticles.value.filter(a => selectedArticles.value.includes(a.pmid))
  if (!selectedList.length) return

  const text = generateArticlesShareText(selectedList)
  const result = await shareContent(text, `MedBrief - ${selectedList.length} articles`)
  if (result.method === 'clipboard') {
    show(`Copied ${selectedList.length} articles to clipboard!`, 'success')
  }
}

async function shareAllArticles() {
  const articlesList = filteredArticles.value
  if (!articlesList.length) return

  const text = generateArticlesShareText(articlesList)
  const result = await shareContent(text, `MedBrief - ${articlesList.length} articles`)
  if (result.method === 'clipboard') {
    show(`Copied ${articlesList.length} articles to clipboard!`, 'success')
  }
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
  border: 2px solid rgba(224, 122, 95, 0.45) !important;
  background: var(--terracotta-100) !important;
}

/* Journal badge */
.badge-journal {
  background-color: var(--terracotta-100);
  color: var(--terracotta-600);
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Journal filter dropdown */
.journal-filter-dropdown .dropdown-item {
  padding: 0.5rem 1rem;
}

.journal-filter-dropdown .dropdown-item.text-muted {
  opacity: 0.7;
}

.journal-filter-dropdown .journal-name {
  word-break: break-word;
  line-height: 1.3;
}

.journal-filter-dropdown .form-check-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Sticky Selection Bar */
.sticky-selection-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1060;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.96);
  border-top: 1px solid var(--warm-200);
  box-shadow: var(--shadow-3);
  animation: slideUp var(--duration-medium) var(--ease-emphasized);
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

/* Abstract filter checkbox styling */
#abstractOnly:checked + label {
  color: var(--terracotta-600);
}

#abstractOnly:focus {
  box-shadow: 0 0 0 0.2rem var(--terracotta-100);
}

.form-check-input:checked {
  background-color: var(--terracotta-500);
  border-color: var(--terracotta-500);
}

</style>
