import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function useToast() {
  function show(message, type = 'info', duration = 3000) {
    const id = ++toastId
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      remove(id)
    }, duration)
  }

  function remove(id) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  return { toasts, show, remove }
}

export function generateArticleShareText(article) {
  const dateFormatted = formatDateMonthYear(article.pub_date)
  let text = `${article.journal}`
  if (dateFormatted) {
    text += ` (${dateFormatted})`
  }
  text += `\n\n${article.title}\n\n`
  text += `Authors: ${formatAuthors(article.authors)}\n`
  text += `PMID: ${article.pmid}\n`
  if (article.doi) {
    text += `DOI: https://doi.org/${article.doi}\n`
  }
  return text
}

export function generateArticlesShareText(articles) {
  return articles.map(a => {
    const dateFormatted = formatDateMonthYear(a.pub_date)
    let text = a.journal
    if (dateFormatted) {
      text += ` (${dateFormatted})`
    }
    text += `\n${a.title}\n`
    text += `Authors: ${formatAuthors(a.authors)}\n`
    text += `PMID: ${a.pmid}\n`
    text += `DOI: ${a.doi || 'N/A'}\n`
    text += `${'─'.repeat(40)}`
    return text
  }).join('\n\n')
}

export async function shareContent(text, title = 'MedBrief Article') {
  if (navigator.share) {
    try {
      await navigator.share({ text, title })
      return { success: true, method: 'native' }
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.warn('Share cancelled or failed:', err)
      }
      return { success: false, method: 'native', error: err }
    }
  }

  try {
    await navigator.clipboard.writeText(text)
    return { success: true, method: 'clipboard' }
  } catch (err) {
    console.error('Clipboard failed:', err)
    return { success: false, method: 'clipboard', error: err }
  }
}

function formatDateMonthYear(dateStr) {
  if (!dateStr) return ''
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const parts = dateStr.split('-')
  if (parts.length !== 3) return ''
  const [year, month, day] = parts
  const monthIndex = parseInt(month) - 1
  if (isNaN(monthIndex) || monthIndex < 0 || monthIndex > 11) return ''
  return `${day}-${months[monthIndex]}-${year}`
}

function formatAuthors(authors) {
  if (!authors || authors.length === 0) return 'N/A'
  if (authors.length <= 3) return authors.join(', ')
  return authors.slice(0, 3).join(', ') + ' et al.'
}
