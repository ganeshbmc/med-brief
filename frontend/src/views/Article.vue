<template>
  <div class="container py-4">
    <!-- Back Navigation -->
    <div class="mb-4">
      <a @click.prevent="goBack" href="#" class="text-link d-inline-flex align-items-center gap-1">
        <ArrowLeft :size="16" />
        Back to Dashboard
      </a>
    </div>

    <!-- Loading -->
    <div v-if="!article" class="text-center py-5">
      <div class="spinner-border"></div>
      <p class="text-muted mt-3">Loading article...</p>
    </div>

    <!-- Article Content (Borderless Layout) -->
    <article v-else class="article-content">
      <!-- Journal Badge & Export -->
      <div class="d-flex justify-content-between align-items-start flex-wrap gap-2 mb-4">
        <span class="badge-journal">{{ article.journal }}</span>
        
        <!-- Export Dropdown -->
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1" type="button" data-bs-toggle="dropdown">
            <Download :size="14" />
            Export
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="#" @click.prevent="exportAs('txt')">TXT (Plain Text)</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="exportAs('ris')">RIS (EndNote, Zotero)</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="exportAs('nbib')">NBIB (PubMed)</a></li>
          </ul>
        </div>
      </div>

      <!-- Title -->
      <h2 class="fw-bold mb-3 text-warm-dark">{{ article.title }}</h2>

      <!-- Authors (no prefix, with et al.) -->
      <p class="text-muted mb-2">
        {{ formatAuthors(article.authors) }}
      </p>

      <!-- Publication Date (simplified) -->
      <p class="text-muted small mb-3">
        {{ article.pub_date }}
      </p>

      <!-- Metadata Links (PMID, DOI) -->
      <div class="d-flex gap-3 flex-wrap mb-4 small">
        <a :href="article.pubmed_url" target="_blank" class="text-link">
          PMID: {{ article.pmid }}
          <ExternalLink :size="12" class="ms-1" />
        </a>
        <a v-if="article.doi" :href="`https://doi.org/${article.doi}`" target="_blank" class="text-link">
          DOI: {{ article.doi }}
          <ExternalLink :size="12" class="ms-1" />
        </a>
      </div>

      <!-- Abstract -->
      <div class="abstract-section my-4 pt-4">
        <h5 class="fw-semibold mb-3 text-warm-dark">Abstract</h5>
        <p class="mb-0 abstract-text">
          {{ article.abstract || 'Abstract not available for this article.' }}
        </p>
      </div>

      <!-- Footer Navigation -->
      <div class="d-flex justify-content-between align-items-center mt-5 pt-3 border-top">
        <a 
          v-if="hasPrev" 
          @click.prevent="navigateTo(-1)" 
          href="#"
          class="text-link d-flex align-items-center gap-1"
        >
          <ArrowLeft :size="14" />
          Previous
        </a>
        <div v-else></div>
        <a 
          v-if="hasNext" 
          @click.prevent="navigateTo(1)" 
          href="#"
          class="text-link d-flex align-items-center gap-1"
        >
          Next
          <ArrowRight :size="14" />
        </a>
      </div>
    </article>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, ArrowRight, Download, ExternalLink } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const article = ref(null)
const articles = ref([]) // All articles for navigation
const currentIndex = ref(-1)

const hasPrev = computed(() => currentIndex.value > 0)
const hasNext = computed(() => currentIndex.value < articles.value.length - 1)

function formatAuthors(authors) {
  if (!authors || authors.length === 0) return 'Authors not available'
  if (authors.length <= 3) return authors.join(', ')
  return authors.slice(0, 3).join(', ') + ' et al.'
}

function goBack() {
  router.push('/dashboard')
}

function navigateTo(offset) {
  const newIndex = currentIndex.value + offset
  if (newIndex >= 0 && newIndex < articles.value.length) {
    const newArticle = articles.value[newIndex]
    router.push(`/article/${newArticle.pmid}`)
  }
}

function exportAs(format) {
  const a = article.value
  let content = ''
  let filename = `article_${a.pmid}`
  let mimeType = 'text/plain'
  
  if (format === 'txt') {
    content = `Title: ${a.title}\n\nAuthors: ${a.authors?.join(', ') || 'N/A'}\n\nJournal: ${a.journal}\n\nDate: ${a.pub_date}\n\nPMID: ${a.pmid}\n\nAbstract:\n${a.abstract || 'N/A'}\n\nPubMed URL: ${a.pubmed_url}`
    filename += '.txt'
  } else if (format === 'ris') {
    content = `TY  - JOUR\nTI  - ${a.title}\n${a.authors?.map(auth => `AU  - ${auth}`).join('\n') || ''}\nJO  - ${a.journal}\nPY  - ${a.pub_date?.split('-')[0] || ''}\nAB  - ${a.abstract || ''}\nAN  - ${a.pmid}\nUR  - ${a.pubmed_url}\nER  - `
    filename += '.ris'
  } else if (format === 'nbib') {
    content = `PMID- ${a.pmid}\nTI  - ${a.title}\n${a.authors?.map(auth => `FAU - ${auth}`).join('\n') || ''}\nJT  - ${a.journal}\nDP  - ${a.pub_date || ''}\nAB  - ${a.abstract || ''}\nSO  - ${a.journal}. ${a.pub_date}.`
    filename += '.nbib'
  }
  
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

function loadArticle() {
  const storedArticles = sessionStorage.getItem('dashboardArticles')
  const pmid = route.params.pmid
  
  if (storedArticles) {
    articles.value = JSON.parse(storedArticles)
    currentIndex.value = articles.value.findIndex(a => a.pmid === pmid)
    if (currentIndex.value >= 0) {
      article.value = articles.value[currentIndex.value]
    }
  }
  
  if (!article.value) {
    console.warn('Article not found in session')
  }
}

// Watch for route param changes (for prev/next navigation)
watch(() => route.params.pmid, (newPmid) => {
  if (newPmid) {
    loadArticle()
  }
})

onMounted(() => {
  window.scrollTo(0, 0)
  loadArticle()
})
</script>

<style scoped>
.article-content {
  max-width: 800px;
  margin: 0 auto;
}

.abstract-section {
  border-top: 1px solid var(--warm-200);
}

.abstract-text {
  line-height: 1.8;
  text-align: justify;
  white-space: pre-wrap;
  color: var(--warm-700);
}

.text-link {
  color: var(--terracotta-500);
  text-decoration: none;
  cursor: pointer;
}

.text-link:hover {
  text-decoration: underline;
  color: var(--terracotta-600);
}

.badge-journal {
  background-color: var(--terracotta-100);
  color: var(--terracotta-600);
  padding: 0.35rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}
</style>
