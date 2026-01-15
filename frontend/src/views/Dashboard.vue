<template>
  <div class="container py-4" :class="preferencesClasses">
    <!-- Header Section -->
    <!-- Header Section -->
    <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-3">
      <div>
        <h2 class="text-warm-dark fw-bold mb-1">Your Brief</h2>
        <p class="text-warm-muted mb-0">Research from {{ formatDateRange(store.fromDate, store.toDate) }}</p>
      </div>
    </div>

    <!-- No Profiles State -->
    <div v-if="!store.loadingProfiles && store.profiles.length === 0" class="empty-state">
      <FileText :size="48" class="icon-muted mb-3" />
      <h4 class="mb-3">Welcome to MedBrief!</h4>
      <p class="text-muted mb-4">You haven't created any profiles yet. Create one to start receiving personalized research briefs.</p>
      <router-link to="/onboarding" class="btn btn-primary px-4">Create Your First Profile</router-link>
    </div>

    <!-- Loading Profiles State -->
    <div v-else-if="store.loadingProfiles" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted mt-3">Loading your profiles...</p>
    </div>

    <!-- Main Content -->
    <template v-else>
      <!-- Control Bar: Profile Selector & Stats -->
      <div class="d-flex align-items-center justify-content-between mb-4 flex-wrap gap-3">
        <!-- Left: Profile Selector -->
        <div class="d-flex align-items-center gap-2">
          <span class="text-muted small fw-semibold ls-1">Current Profile:</span>
          <div class="dropdown">
            <button 
              class="btn btn-link text-decoration-none p-0 fw-bold text-warm-dark dropdown-toggle d-flex align-items-center gap-2" 
              type="button" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              {{ store.currentProfile?.name }}
            </button>
            <ul class="dropdown-menu">
              <li v-for="p in store.profiles" :key="p.id">
                <a 
                  class="dropdown-item d-flex align-items-center justify-content-between" 
                  :class="{ active: store.selectedProfileId === p.id }"
                  href="#" 
                  @click.prevent="selectProfile(p.id)"
                >
                  {{ p.name }}
                  <Check v-if="store.selectedProfileId === p.id" :size="16" class="text-success" />
                </a>
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

        <!-- Right: Stats & Actions -->
        <div class="d-flex align-items-center gap-3">
          <span class="text-muted small">{{ store.currentProfile?.journal_ids?.length || 0 }} journals</span>
          <div class="vr text-muted opacity-25"></div>
          <span class="badge bg-terracotta-100 text-dark rounded-pill px-3" style="color: var(--terracotta-700) !important;">
            {{ filteredArticles.length }} article{{ filteredArticles.length !== 1 ? 's' : '' }}
            <span v-if="showAbstractOnly" class="text-terracotta-600">(with abstracts)</span>
          </span>
          <div class="vr text-muted opacity-25"></div>
          
          <button 
            class="btn btn-light btn-sm btn-icon text-muted" 
            @click="refreshArticles" 
            :disabled="store.loading"
            title="Refresh Articles"
          >
            <span v-if="store.loading" class="spinner-border spinner-border-sm"></span>
            <RefreshCw v-else :size="18" />
          </button>
        </div>
      </div>
      
      <!-- Filters -->
      <div class="card mb-4 p-3">
        <div class="row g-3 align-items-center">
          <div class="col-md-3">
            <div class="input-group">
              <span class="input-group-text bg-white border-end-0">
                <Search :size="18" class="icon-muted" />
              </span>
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-control border-start-0" 
                placeholder="Search articles..."
              />
            </div>
          </div>
          <div class="col-md-3">
            <!-- Journal Filter Dropdown -->
            <div class="dropdown">
              <button 
                class="btn btn-outline-secondary w-100 dropdown-toggle text-start d-flex align-items-center gap-2" 
                type="button" 
                data-bs-toggle="dropdown"
                data-bs-auto-close="outside"
              >
                <Newspaper :size="18" />
                {{ selectedJournals.length ? `${selectedJournals.length} journal(s)` : 'All Journals' }}
              </button>
              <ul class="dropdown-menu journal-filter-dropdown" style="min-width: 350px; max-height: 400px; overflow-y: auto;">
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="selectedJournals = []">
                    <em>Clear filters</em>
                  </a>
                </li>
                <li><hr class="dropdown-divider" /></li>
                 <li v-for="journal in availableJournals" :key="journal.name">
                   <a 
                     class="dropdown-item d-flex align-items-center justify-content-between" 
                     :class="{ 'text-muted': !journal.hasData }"
                     href="#" 
                     @click.prevent="toggleJournalFilter(journal.name)"
                     :title="!journal.hasData ? 'No articles found for this journal in the selected time period' : journal.name"
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
                   </a>
                 </li>
              </ul>
            </div>
          </div>
          <!-- Responsive Filter Controls: All in one row on lg, two rows on sm/md -->
          <div class="col-12 col-lg-auto">
            <div class="d-flex gap-2 flex-wrap">
              <!-- Quick Select -->
              <div>
                <label class="form-label small text-muted mb-1">Quick Select</label>
                <select v-model="store.daysPreset" class="form-select form-select-sm" @change="applyPreset">
                  <option :value="1">Last 24 hours</option>
                  <option :value="3">Last 3 days</option>
                  <option :value="7">Last 7 days</option>
                  <option :value="14">Last 14 days</option>
                  <option :value="30">Last 30 days</option>
                  <option :value="0">Custom</option>
                </select>
              </div>
               <!-- Sort -->
               <div>
                 <label class="form-label small text-muted mb-1">Sort</label>
                 <select v-model="sortBy" class="form-select form-select-sm">
                   <option value="date">By Date</option>
                   <option value="journal">By Journal</option>
                 </select>
               </div>
               <!-- Abstract Only Filter -->
               <div class="d-flex align-items-center mt-2">
                 <div class="form-check">
                   <input
                     type="checkbox"
                     class="form-check-input"
                     id="abstractOnly"
                     v-model="showAbstractOnly"
                   />
                   <label class="form-check-label small text-warm-dark fw-medium" for="abstractOnly">
                     With abstract only
                   </label>
                 </div>
                 <span class="badge bg-terracotta-100 text-terracotta-700 ms-2 rounded-pill" style="font-size: 0.7rem;">
                   {{ articlesWithAbstract.length }} available
                 </span>
               </div>
               <!-- From -->
              <div>
                <label class="form-label small text-muted mb-1">From</label>
                <input type="date" v-model="localFromDate" class="form-control form-control-sm" @change="handleDateChange" />
              </div>
              <!-- To -->
              <div>
                <label class="form-label small text-muted mb-1">To</label>
                <input type="date" v-model="localToDate" class="form-control form-control-sm" :max="store.todayDate" @change="handleDateChange" />
              </div>
            </div>
          </div>
        </div>
        <!-- Article count, limit warning, and export buttons -->
        <div class="d-flex justify-content-between align-items-center mt-2 pt-2 border-top flex-wrap gap-2">
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
          <!-- Selection toggle and bulk export -->
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
            <!-- Export dropdown for selected articles -->
            <div class="dropdown" v-if="selectionMode && selectedArticles.length > 0">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1" type="button" data-bs-toggle="dropdown">
                <Download :size="16" />
                Export Selected
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('pdf')"><File :size="16" class="me-1" />PDF</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('txt')">TXT</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('ris')">RIS</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('nbib')">NBIB</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click.prevent="shareSelectedArticles">
                  <Share2 :size="16" class="me-1" />Share via...
                </a></li>
              </ul>
            </div>
            <!-- Export dropdown for all articles -->
            <div class="dropdown" v-else-if="filteredArticles.length > 0 && !selectionMode">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1" type="button" data-bs-toggle="dropdown">
                <Download :size="16" />
                Export
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#" @click.prevent="exportAllArticles('pdf')"><File :size="16" class="me-1" />PDF</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportAllArticles('txt')">TXT</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportAllArticles('ris')">RIS</a></li>
                <li><a class="dropdown-item" href="#" @click.prevent="exportAllArticles('nbib')">NBIB</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click.prevent="shareAllArticles">
                  <Share2 :size="16" class="me-1" />Share via...
                </a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="store.loading && store.articles.length === 0" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted mt-3">Fetching latest articles...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredArticles.length === 0" class="empty-state">
        <FileText :size="48" class="icon-muted mb-3" />
        <h4>No articles found</h4>
        <p class="text-muted">{{ store.articles.length === 0 ? 'No new articles from your selected journals in this time period.' : 'Try adjusting your search or journal filters.' }}</p>
        <button v-if="selectedJournals.length > 0" class="btn btn-outline-primary mt-2" @click="selectedJournals = []">
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
              <h6 class="card-title fw-semibold text-warm-dark">{{ article.title }}</h6>
              <p class="card-text text-muted small mb-2">
                {{ article.authors?.slice(0, 3).join(', ') }}{{ article.authors?.length > 3 ? ' et al.' : '' }}
              </p>
              <p v-if="article.abstract" class="card-text text-muted small flex-grow-1 abstract-preview">
                {{ truncateAbstract(article.abstract) }}
              </p>
              <div class="d-flex justify-content-between align-items-center mt-3 pt-3 border-top">
                <small class="text-muted d-flex align-items-center gap-1">
                  <Calendar :size="14" />
                  {{ formatDateDisplay(article.pub_date) }}
                </small>
                <span v-if="!selectionMode" class="btn btn-sm btn-outline-primary d-flex align-items-center gap-1">
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
    class="sticky-selection-bar bg-white border-top shadow-lg px-3 py-2 d-flex justify-content-center justify-content-sm-between align-items-center flex-wrap gap-2"
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
        <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('pdf')"><File :size="16" class="me-1" />PDF</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('txt')">TXT</a></li>
        <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('ris')">RIS</a></li>
        <li><a class="dropdown-item" href="#" @click.prevent="exportSelectedArticles('nbib')">NBIB</a></li>
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
    content = selectedList.map(a => 
      `Title: ${a.title}\nAuthors: ${a.authors?.join(', ') || 'N/A'}\nJournal: ${a.journal}\nDate: ${formatDateDisplay(a.pub_date)}\nPMID: ${a.pmid}\nDOI: ${a.doi || 'N/A'}\nAbstract: ${a.abstract || 'N/A'}\nURL: ${a.pubmed_url}\n${'='.repeat(80)}`
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
    content = articlesList.map(a => 
      `Title: ${a.title}\nAuthors: ${a.authors?.join(', ') || 'N/A'}\nJournal: ${a.journal}\nDate: ${formatDateDisplay(a.pub_date)}\nPMID: ${a.pmid}\nAbstract: ${a.abstract || 'N/A'}\nURL: ${a.pubmed_url}\n${'='.repeat(80)}`
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
  border: 2px solid var(--terracotta-500) !important;
  background: var(--terracotta-100) !important;
}

/* Journal badge */
.badge-journal {
  background-color: var(--terracotta-100);
  color: var(--terracotta-600);
  padding: 0.35rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Search input group */
.input-group-text {
  border-color: var(--warm-200);
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

/* Utilities */
.ls-1 {
  letter-spacing: 1px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background-color: var(--warm-200);
  color: var(--warm-dark) !important;
}

/* Sticky Selection Bar */
.sticky-selection-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1060;
  animation: slideUp 0.3s ease-out;
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
