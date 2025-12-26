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
 * Profile API
 */
export async function getProfiles() {
    return request('/api/profiles/')
}

export async function createProfile(name, journalIds) {
    return request('/api/profiles/', {
        method: 'POST',
        body: JSON.stringify({ name, journal_ids: journalIds }),
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

