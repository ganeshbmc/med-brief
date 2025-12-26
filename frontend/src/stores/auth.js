import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token') || null)
    const user = ref(null)

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
            throw new Error(error.detail || 'Login failed')
        }

        const data = await response.json()
        token.value = data.access_token
        localStorage.setItem('token', data.access_token)
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

    return { token, user, isAuthenticated, login, register, logout, getAuthHeaders }
})
