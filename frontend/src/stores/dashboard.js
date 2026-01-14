import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getProfiles, generateBrief, getJournalsByIds } from '../services/api'
import { useAuthStore } from './auth'

export const useDashboardStore = defineStore('dashboard', () => {
    // Core data
    const articles = ref([])
    const profiles = ref([])
    const selectedProfileId = ref(null)
    const profileJournals = ref([])

    // Date range
    const todayDate = new Date().toISOString().split('T')[0]
    const fromDate = ref(new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])
    const toDate = ref(todayDate)
    const daysPreset = ref(7)

    // Loading states
    const loading = ref(false)
    const loadingProfiles = ref(false)

    // Track if data has been loaded this session
    const hasLoadedProfiles = ref(false)
    const hasLoadedArticles = ref(false)

    // Scroll position preservation
    const scrollPosition = ref(0)

    // Computed
    const currentProfile = computed(() => {
        return profiles.value.find(p => p.id === selectedProfileId.value)
    })

    const hasCache = computed(() => {
        return hasLoadedArticles.value && articles.value.length >= 0
    })

    // Initialize date range from user preferences
    function initializeDateRange() {
        const authStore = useAuthStore()
        const defaultDays = authStore.preferences?.defaultDays || 7
        if (!hasLoadedProfiles.value && !hasLoadedArticles.value) {
            applyPreset(defaultDays)
        }
    }

    // Actions
    async function loadProfiles(force = false) {
        if (!force && hasLoadedProfiles.value) return

        loadingProfiles.value = true
        try {
            profiles.value = await getProfiles()
            hasLoadedProfiles.value = true
            if (profiles.value.length > 0 && !selectedProfileId.value) {
                selectedProfileId.value = profiles.value[0].id
            }
            // When force-refreshing, also invalidate journal and article caches
            // so they get re-fetched with updated profile data
            if (force) {
                loadedJournalsForProfileId.value = null
                profileJournals.value = []
                hasLoadedArticles.value = false
                articles.value = []
            }
        } catch (e) {
            console.error('Failed to load profiles:', e)
        } finally {
            loadingProfiles.value = false
        }
    }

    // Track if journals have been loaded for current profile
    const loadedJournalsForProfileId = ref(null)

    async function loadProfileJournals() {
        // Skip if already loaded for this profile
        if (loadedJournalsForProfileId.value === selectedProfileId.value && profileJournals.value.length > 0) {
            console.log('Using cached profile journals')
            return
        }

        if (!currentProfile.value?.journal_ids?.length) {
            profileJournals.value = []
            return
        }
        try {
            profileJournals.value = await getJournalsByIds(currentProfile.value.journal_ids)
            loadedJournalsForProfileId.value = selectedProfileId.value
            console.log('Fetched profile journals from API')
        } catch (e) {
            console.error('Failed to load journals:', e)
            profileJournals.value = []
        }
    }

    async function fetchArticles(force = false) {
        if (!selectedProfileId.value) return

        // Skip if we have cached data and not forcing refresh
        if (!force && hasCache.value) {
            console.log('Using cached dashboard data')
            return
        }

        loading.value = true
        try {
            articles.value = await generateBrief(selectedProfileId.value, {
                fromDate: fromDate.value,
                toDate: toDate.value
            })
            hasLoadedArticles.value = true
            console.log('Fetched fresh articles from API')
        } catch (e) {
            console.error('Failed to fetch articles:', e)
            articles.value = []
        } finally {
            loading.value = false
        }
    }

    function setProfile(profileId) {
        if (profileId !== selectedProfileId.value) {
            selectedProfileId.value = profileId
            // Clear cache when profile changes
            hasLoadedArticles.value = false
            articles.value = []
        }
    }

    function setDateRange(from, to) {
        const changed = from !== fromDate.value || to !== toDate.value
        fromDate.value = from
        toDate.value = to
        if (changed) {
            // Clear cache when date range changes
            hasLoadedArticles.value = false
        }
    }

    function applyPreset(days) {
        if (days > 0) {
            daysPreset.value = days
            const newToDate = todayDate
            const newFromDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            setDateRange(newFromDate, newToDate)
        } else {
            daysPreset.value = 0
        }
    }

    // Clear all cache (for logout, etc.)
    function clearCache() {
        articles.value = []
        profiles.value = []
        selectedProfileId.value = null
        profileJournals.value = []
        hasLoadedProfiles.value = false
        hasLoadedArticles.value = false
        scrollPosition.value = 0
    }

    // Scroll position functions
    function saveScrollPosition() {
        scrollPosition.value = window.scrollY
        console.log('Saved scroll position:', scrollPosition.value)
    }

    return {
        // State
        articles,
        profiles,
        selectedProfileId,
        profileJournals,
        fromDate,
        toDate,
        daysPreset,
        todayDate,
        loading,
        loadingProfiles,
        hasLoadedArticles,
        // Computed
        currentProfile,
        hasCache,
        // Actions
        loadProfiles,
        loadProfileJournals,
        fetchArticles,
        setProfile,
        setDateRange,
        applyPreset,
        clearCache,
        saveScrollPosition,
        scrollPosition,
        initializeDateRange,
    }
})
