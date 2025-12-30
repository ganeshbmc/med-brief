import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Onboarding from '../views/Onboarding.vue'
import Profiles from '../views/Profiles.vue'
import Article from '../views/Article.vue'
import Account from '../views/Account.vue'

const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register },
    { path: '/onboarding', name: 'Onboarding', component: Onboarding, meta: { requiresAuth: true } },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/profiles', name: 'Profiles', component: Profiles, meta: { requiresAuth: true } },
    { path: '/article/:pmid', name: 'Article', component: Article, meta: { requiresAuth: true } },
    { path: '/account', name: 'Account', component: Account, meta: { requiresAuth: true } },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        // If user navigated back/forward, use saved position
        if (savedPosition) {
            return savedPosition
        }
        // Otherwise scroll to top
        return { top: 0 }
    }
})

// Navigation guard
// Navigation guard
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Auth Guard: Redirect unauthenticated users to login
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
        return
    }

    // Guest Guard: Redirect authenticated users to dashboard if they try to access guest pages
    const guestRoutes = ['Home', 'Login', 'Register']
    if (guestRoutes.includes(to.name) && authStore.isAuthenticated) {
        next('/dashboard')
        return
    }

    next()
})

export default router
