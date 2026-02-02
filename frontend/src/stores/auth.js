import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getPreferences, updatePreferences as apiUpdatePreferences } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token') || null)
    const user = ref(null)
    const preferences = ref({ fontSize: 'medium', lineSpacing: 'normal', defaultDays: 7 })

    const isAuthenticated = computed(() => !!token.value)

    async function login(email, password) {
        const formData = new URLSearchParams()
        formData.append('username', email)
        formData.append('password', password)

        let response
        try {
            response = await fetch('/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
            })
        } catch (e) {
            throw new Error('Unable to connect to server. Is the backend running?')
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({}))
            throw new Error(error.detail || 'Sign in failed')
        }

        const data = await response.json()
        token.value = data.access_token
        localStorage.setItem('token', data.access_token)
        await fetchUser()
        return data
    }

    async function register(email, password) {
        let response
        try {
            response = await fetch('/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            })
        } catch (e) {
            throw new Error('Unable to connect to server. Is the backend running?')
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({}))
            throw new Error(error.detail || 'Registration failed')
        }

        const data = await response.json()
        token.value = data.access_token
        localStorage.setItem('token', data.access_token)
        return data
    }

    function logout() {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
    }

    function getAuthHeaders() {
        return token.value ? { Authorization: `Bearer ${token.value}` } : {}
    }

    async function fetchUser() {
        if (!token.value) return
        try {
            const response = await fetch('/auth/me', {
                headers: getAuthHeaders(),
            })
            if (response.ok) {
                user.value = await response.json()
                if (user.value.preferences) {
                    preferences.value = { ...preferences.value, ...user.value.preferences }
                }
            }
        } catch (e) {
            console.error('Failed to fetch user', e)
        }
    }

    async function fetchPreferences() {
        try {
            const prefs = await getPreferences()
            preferences.value = { ...preferences.value, ...prefs }
        } catch (e) {
            console.error('Failed to fetch preferences', e)
        }
    }

    async function updateUserPreferences(newPrefs) {
        try {
            const updated = await apiUpdatePreferences(newPrefs)
            preferences.value = { ...preferences.value, ...updated }
            return updated
        } catch (e) {
            throw e
        }
    }

    async function updateProfile(fullName) {
        try {
            const response = await fetch('/auth/me', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...getAuthHeaders(),
                },
                body: JSON.stringify({ full_name: fullName }),
            })

            if (!response.ok) throw new Error('Failed to update profile')

            user.value = await response.json()
            return user.value
        } catch (e) {
            throw e
        }
    }

    return { token, user, isAuthenticated, preferences, login, register, logout, getAuthHeaders, fetchUser, updateProfile, fetchPreferences, updateUserPreferences }
})
