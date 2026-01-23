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
  const shareLink = article.doi ? `https://doi.org/${article.doi}` : `https://pubmed.ncbi.nlm.nih.gov/${article.pmid}/`
  
  let text = `*${article.title}*\n`
  text += `${article.journal}\n\n`
  
  text += `PMID: ${article.pmid}`
  if (dateFormatted) {
    text += ` • ${dateFormatted}`
  }
  text += `\n`
  
  text += `Authors: ${formatAuthors(article.authors)}\n\n`
  text += `${shareLink}`
  
  return text
}

export function generateArticlesShareText(articles) {
  const header = `*MedBrief Selection* (${articles.length} articles)\n\n`
  
  const body = articles.map((a, index) => {
    const dateFormatted = formatDateMonthYear(a.pub_date)
    const shareLink = a.doi ? `https://doi.org/${a.doi}` : `https://pubmed.ncbi.nlm.nih.gov/${a.pmid}/`
    
    let text = `${index + 1}. *${a.title}*\n`
    text += `   ${a.journal}\n`
    text += `   PMID: ${a.pmid}`
    if (dateFormatted) {
      text += ` • ${dateFormatted}`
    }
    text += `\n`
    text += `   ${shareLink}`
    return text
  }).join('\n\n')
  
  return header + body
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
  
  const year = parts[0] || ''
  const month = parts[1] || ''
  const day = parts[2] || ''
  
  if (!year) return ''

  let monthText = ''
  if (month) {
    let monthIndex = parseInt(month) - 1
    if (isNaN(monthIndex) || monthIndex < 0 || monthIndex > 11) {
      monthIndex = months.findIndex(m => m.toLowerCase() === month.toLowerCase().substring(0, 3))
    }
    if (monthIndex >= 0 && monthIndex <= 11) {
      monthText = months[monthIndex]
    }
  }

  let result = ''
  if (day) result += `${day}-`
  if (monthText) result += `${monthText}-`
  result += year
  
  return result
}

function formatAuthors(authors) {
  if (!authors || authors.length === 0) return 'N/A'
  if (authors.length <= 3) return authors.join(', ')
  return authors.slice(0, 3).join(', ') + ' et al.'
}
