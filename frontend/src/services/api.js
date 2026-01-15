/**
 * API Service - Centralized API helper with auth headers
 */

import { useAuthStore } from '../stores/auth'

const BASE_URL = ''  // Empty because Vite proxy handles /api and /auth

/**
 * Make an authenticated API request
 */
async function request(endpoint, options = {}) {
    const authStore = useAuthStore()

    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...authStore.getAuthHeaders(),
            ...options.headers,
        },
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, config)

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }))
        throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
}

/**
 * Journal API
 */
export async function searchJournals(query) {
    return request(`/api/journals/search?q=${encodeURIComponent(query)}`)
}

export async function getPresetJournals(category) {
    return request(`/api/journals/presets/${encodeURIComponent(category)}`)
}

export async function getJournalsByIds(ids) {
    if (!ids || ids.length === 0) return []
    return request(`/api/journals/by-ids?ids=${ids.join(',')}`)
}

/**
 * Search PubMed/NLM Catalog for journals
 */
export async function searchPubmedJournals(query) {
    return request(`/api/journals/pubmed-search?q=${encodeURIComponent(query)}`)
}

/**
 * Profile API
 */
export async function getProfiles() {
    return request('/api/profiles/')
}

export async function createProfile(name, journalIds, newJournals = []) {
    return request('/api/profiles/', {
        method: 'POST',
        body: JSON.stringify({
            name,
            journal_ids: journalIds,
            new_journals: newJournals
        }),
    })
}

/**
 * Briefs API
 */
export async function generateBrief(profileId, { days = 7, fromDate = null, toDate = null } = {}) {
    let url = `/api/briefs/generate?profile_id=${profileId}`
    if (fromDate && toDate) {
        url += `&from_date=${fromDate}&to_date=${toDate}`
    } else {
        url += `&days=${days}`
    }
    return request(url)
}

/**
 * Update a profile
 */
export async function updateProfile(profileId, name, journalIds) {
    return request(`/api/profiles/${profileId}`, {
        method: 'PUT',
        body: JSON.stringify({ name, journal_ids: journalIds }),
    })
}

/**
 * Delete a profile
 */
export async function deleteProfile(profileId) {
    return request(`/api/profiles/${profileId}`, {
        method: 'DELETE',
    })
}

/**
 * Set a profile as the default profile
 */
export async function setDefaultProfile(profileId) {
    return request(`/api/profiles/${profileId}/set-default`, {
        method: 'POST',
    })
}

/**
 * Get user preferences
 */
export async function getPreferences() {
    return request('/api/preferences/')
}

/**
 * Update user preferences
 */
export async function updatePreferences(prefs) {
    return request('/api/preferences/', {
        method: 'PUT',
        body: JSON.stringify(prefs),
    })
}

/**
 * Export brief as PDF
 */
export async function exportToPdf(profileId, { days = 7, fromDate = null, toDate = null, articleIds = null } = {}) {
    let url = `/api/briefs/export-pdf?profile_id=${profileId}`
    if (fromDate && toDate) {
        url += `&from_date=${fromDate}&to_date=${toDate}`
    } else {
        url += `&days=${days}`
    }
    if (articleIds) {
        url += `&article_ids=${encodeURIComponent(articleIds)}`
    }

    // Use fetch directly for file download
    const authStore = useAuthStore()
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            ...authStore.getAuthHeaders(),
        },
    })

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Export failed' }))
        throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.blob()  // Return blob for file download
}

/**
 * Request password reset email
 */
export async function requestPasswordReset(email) {
    // Use fetch directly since this doesn't require auth
    const response = await fetch('/auth/forgot-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
    })

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }))
        throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
}

/**
 * Reset password with token
 */
export async function resetPassword(token, newPassword) {
    // Use fetch directly since this doesn't require auth
    const response = await fetch('/auth/reset-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            token,
            new_password: newPassword
        }),
    })

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }))
        throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
}

