<template>
  <div class="container py-4">
    <!-- Back Navigation -->
    <div class="mb-4">
      <button @click="goBack" class="btn btn-outline-light">
        ← Back to Dashboard
      </button>
    </div>

    <!-- Loading -->
    <div v-if="!article" class="text-center py-5">
      <div class="spinner-border text-light"></div>
      <p class="text-white mt-3">Loading article...</p>
    </div>

    <!-- Article Content -->
    <div v-else class="card">
      <!-- Header -->
      <div class="card-header bg-light">
        <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
          <span class="badge bg-primary">{{ article.journal }}</span>
          <div class="btn-group btn-group-sm">
            <button class="btn btn-outline-secondary" @click="exportAs('txt')">📄 TXT</button>
            <button class="btn btn-outline-secondary" @click="exportAs('ris')">📋 RIS</button>
            <button class="btn btn-outline-secondary" @click="exportAs('nbib')">📑 NBIB</button>
          </div>
        </div>
      </div>

      <!-- Body -->
      <div class="card-body">
        <!-- Title -->
        <h3 class="card-title fw-bold mb-3">{{ article.title }}</h3>

        <!-- Authors -->
        <p class="text-muted mb-2">
          <strong>Authors:</strong> {{ article.authors?.join(', ') || 'Not available' }}
        </p>

        <!-- Journal & Date -->
        <p class="text-muted mb-2">
          <strong>Published:</strong> {{ article.pub_date }} in <em>{{ article.journal }}</em>
        </p>

        <!-- DOI -->
        <p v-if="article.doi" class="mb-4">
          <strong>DOI:</strong>&nbsp;
          <a :href="`https://doi.org/${article.doi}`" target="_blank" class="doi-link">
            {{ article.doi }}
          </a>
        </p>

        <!-- Abstract (Centered, Prominent) -->
        <div class="abstract-section my-4 p-4 bg-light rounded">
          <h5 class="fw-semibold mb-3">Abstract</h5>
          <p class="mb-0 abstract-text">
            {{ article.abstract || 'Abstract not available for this article.' }}
          </p>
        </div>

        <!-- Links -->
        <div class="d-flex gap-3 flex-wrap mt-4 pt-3 border-top">
          <a :href="article.pubmed_url" target="_blank" class="btn btn-primary">
            🔗 View on PubMed
          </a>
          <a v-if="article.doi" :href="`https://doi.org/${article.doi}`" target="_blank" class="btn btn-success">
            📖 Full Text (DOI)
          </a>
          <a :href="`https://pubmed.ncbi.nlm.nih.gov/${article.pmid}/?format=pubmed`" target="_blank" class="btn btn-outline-secondary">
            📋 PubMed Format
          </a>
        </div>

        <!-- Citation Info -->
        <div class="mt-4 pt-3 border-top">
          <small class="text-muted">
            <strong>PMID:</strong> {{ article.pmid }}
          </small>
        </div>
      </div>

      <!-- Footer Navigation -->
      <div class="card-footer bg-light d-flex justify-content-between">
        <button 
          v-if="hasPrev" 
          @click="navigateTo(-1)" 
          class="btn btn-outline-primary"
        >
          ← Previous Article
        </button>
        <div v-else></div>
        <button 
          v-if="hasNext" 
          @click="navigateTo(1)" 
          class="btn btn-outline-primary"
        >
          Next Article →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const article = ref(null)
const articles = ref([]) // All articles for navigation
const currentIndex = ref(-1)

const hasPrev = computed(() => currentIndex.value > 0)
const hasNext = computed(() => currentIndex.value < articles.value.length - 1)

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
  loadArticle()
})
</script>

<style scoped>
.abstract-section {
  border-left: 4px solid #667eea;
}

.abstract-text {
  line-height: 1.8;
  text-align: justify;
  white-space: pre-wrap;
}

.doi-link {
  color: #0d6efd;
  text-decoration: none;
}

.doi-link:hover {
  text-decoration: underline;
}
</style>
