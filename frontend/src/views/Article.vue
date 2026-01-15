<template>
  <div class="container py-4" :class="preferencesClasses">
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
            <li><a class="dropdown-item" href="#" @click.prevent="exportAs('pdf')"><File :size="14" class="me-1" />PDF</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#" @click.prevent="exportAs('txt')">TXT (Plain Text)</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="exportAs('ris')">RIS (EndNote, Zotero)</a></li>
            <li><a class="dropdown-item" href="#" @click.prevent="exportAs('nbib')">NBIB (PubMed)</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#" @click.prevent="handleShare">
              <Share2 :size="14" class="me-1" />Share
            </a></li>
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
        {{ formatDateDisplay(article.pub_date) }}
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

    <!-- Sticky Navigation -->
    <StickyArticleNavigation
      :hasPrev="hasPrev"
      :hasNext="hasNext"
      @navigate="navigateTo"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ArrowLeft, ArrowRight, Download, ExternalLink, Share2, File } from 'lucide-vue-next'
import { formatDateDisplay } from '@/utils/dateFormatter'
import { generateArticleShareText, shareContent, useToast } from '@/utils/shareUtils'
import html2pdf from 'html2pdf.js'
import StickyArticleNavigation from '@/components/StickyArticleNavigation.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { show } = useToast()

const article = ref(null)
const articles = ref([])
const currentIndex = ref(-1)

const hasPrev = computed(() => currentIndex.value > 0)
const hasNext = computed(() => currentIndex.value < articles.value.length - 1)

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

async function handleShare() {
  const text = generateArticleShareText(article.value)
  const result = await shareContent(text, article.value.title)
  if (result.method === 'clipboard') {
    show('Copied to clipboard!', 'success')
  }
}

async function exportAs(format) {
  const a = article.value

  if (format === 'pdf') {
    try {
      // Create a temporary HTML element for PDF generation
      const tempDiv = document.createElement('div')
      tempDiv.innerHTML = `
        <div style="
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          font-size: 12pt;
          line-height: 1.6;
          margin: 50px;
          color: #1f2937;
          max-width: 800px;
        ">
          <div style="
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #e07a5f;
            padding-bottom: 25px;
          ">
            <h1 style="
              font-size: 24pt;
              margin: 0;
              font-weight: 600;
              color: #1f2937;
            ">MedBrief Article</h1>
          </div>

          <div style="
            background: #fef3f2;
            color: #e07a5f;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 10pt;
            font-weight: 500;
            display: inline-block;
            margin-bottom: 20px;
          ">${a.journal}</div>

          <h1 style="
            font-size: 18pt;
            font-weight: 600;
            margin-bottom: 15px;
            line-height: 1.3;
            color: #1f2937;
          ">${a.title}</h1>

          <div style="
            font-size: 11pt;
            color: #374151;
            margin-bottom: 8px;
          ">${formatAuthors(a.authors)}</div>

          <div style="
            font-size: 11pt;
            color: #6b7280;
            margin-bottom: 15px;
            font-weight: 500;
          ">Published: ${formatDateDisplay(a.pub_date)}</div>

          <div style="margin-bottom: 20px;">
            ${a.pmid ? `<a href="https://pubmed.ncbi.nlm.nih.gov/${a.pmid}/" style="
              display: inline-block;
              margin-right: 15px;
              color: #059669;
              text-decoration: none;
              font-weight: 500;
              font-size: 10pt;
              padding: 6px 12px;
              background: #ecfdf5;
              border-radius: 6px;
              border: 1px solid #d1fae5;
            " target="_blank">PMID: ${a.pmid}</a>` : ''}

            ${a.doi ? `<a href="https://doi.org/${a.doi}" style="
              display: inline-block;
              margin-right: 15px;
              color: #059669;
              text-decoration: none;
              font-weight: 500;
              font-size: 10pt;
              padding: 6px 12px;
              background: #ecfdf5;
              border-radius: 6px;
              border: 1px solid #d1fae5;
            " target="_blank">DOI: ${a.doi}</a>` : ''}
          </div>

          <div style="
            background: #f9fafb;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #e07a5f;
            line-height: 1.6;
          ">
            <div style="
              font-weight: 600;
              margin-bottom: 10px;
              color: #1f2937;
              font-size: 12pt;
            ">Abstract:</div>
            <div>${a.abstract || 'No abstract available for this article.'}</div>
          </div>
        </div>
      `

      document.body.appendChild(tempDiv)

      const opt = {
        margin: 1,
        filename: `article_${a.pmid}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      }

      html2pdf().set(opt).from(tempDiv).save().then(() => {
        document.body.removeChild(tempDiv)
        show('Article exported as PDF', 'success')
      }).catch((error) => {
        document.body.removeChild(tempDiv)
        console.error('PDF generation failed:', error)
        show('PDF export failed', 'error')
      })

    } catch (e) {
      console.error('Export failed:', e)
      show('Export failed', 'error')
    }
    return
  }

  let content = ''
  let filename = `article_${a.pmid}`
  let mimeType = 'text/plain'

  if (format === 'txt') {
    content = `Title: ${a.title}\n\nAuthors: ${a.authors?.join(', ') || 'N/A'}\n\nJournal: ${a.journal}\n\nDate: ${formatDateDisplay(a.pub_date)}\n\nPMID: ${a.pmid}\n\nAbstract:\n${a.abstract || 'N/A'}\n\nPubMed URL: ${a.pubmed_url}`
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
    window.scrollTo(0, 0)
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
