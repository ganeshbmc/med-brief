<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-9">
        <div class="install-topbar d-flex align-items-center justify-content-between gap-3 mb-4">
          <router-link v-if="!authStore.isAuthenticated" to="/" class="install-topbar__link d-inline-flex align-items-center gap-2">
            <ArrowLeft :size="16" />
            Back to Home
          </router-link>
          <div class="install-topbar__right ms-auto">
            <router-link v-if="authStore.isAuthenticated" to="/dashboard" class="install-topbar__link d-inline-flex align-items-center gap-2">
              Go to Dashboard
              <ArrowRight :size="16" />
            </router-link>
            <router-link v-else to="/login" class="install-topbar__link d-inline-flex align-items-center gap-2">
              Sign In
              <ArrowRight :size="16" />
            </router-link>
          </div>
        </div>
        <div class="install-hero mb-4">
          <div class="install-badge d-inline-flex align-items-center gap-2 mb-3">
            <Download :size="18" />
            Install
          </div>
          <h1 class="fw-bold text-warm-dark mb-3">Install MedBrief on your phone</h1>
          <p class="text-muted mb-0">
            Add MedBrief to your home screen for one-tap access. Most mobile browsers, including Chrome and Edge,
            support this via an “Add to home screen” or “Add to phone” option.
          </p>
        </div>

        <div class="install-choice d-flex flex-wrap gap-2 mb-4">
          <button
            type="button"
            class="btn d-flex align-items-center gap-2"
            :class="selectedPlatform === 'android' ? 'btn-primary' : 'btn-outline-terracotta'"
            @click="selectedPlatform = 'android'"
          >
            <Smartphone :size="18" />
            Android
          </button>
          <button
            type="button"
            class="btn d-flex align-items-center gap-2"
            :class="selectedPlatform === 'iphone' ? 'btn-primary' : 'btn-outline-terracotta'"
            @click="selectedPlatform = 'iphone'"
          >
            <Phone :size="18" />
            iPhone
          </button>
        </div>

        <div class="install-panel card border-0 shadow-sm">
          <div class="card-body p-4">
            <div v-if="selectedPlatform === 'android'" class="install-content">
              <div class="platform-header d-flex align-items-center gap-3 mb-3">
                <div class="platform-icon">
                  <Smartphone :size="22" />
                </div>
                <div>
                  <h2 class="h5 fw-semibold text-warm-dark mb-1">Android install steps</h2>
                  <p class="text-muted mb-0">Best on Chrome, Edge, or Samsung Internet.</p>
                </div>
              </div>
              <ol class="install-steps">
                <li>Open MedBrief in your mobile browser.</li>
                <li>Tap the browser menu (three dots or “More”).</li>
                <li>Select <strong>Add to Home screen</strong> or <strong>Add to phone</strong>.</li>
                <li>Confirm the name, then tap <strong>Add</strong>.</li>
              </ol>
              <div class="alert alert-info d-flex align-items-start gap-2 mt-4 mb-0" role="alert">
                <Info :size="18" class="mt-1" />
                The installed app opens full-screen and keeps your MedBrief icon on the home screen.
              </div>
            </div>

            <div v-else class="install-content">
              <div class="platform-header d-flex align-items-center gap-3 mb-3">
                <div class="platform-icon">
                  <Phone :size="22" />
                </div>
                <div>
                  <h2 class="h5 fw-semibold text-warm-dark mb-1">iPhone install steps</h2>
                  <p class="text-muted mb-0">Recommended in Safari (works on most iOS browsers).</p>
                </div>
              </div>
              <ol class="install-steps">
                <li>Open MedBrief in Safari (or your preferred iOS browser).</li>
                <li>Tap the <strong>Share</strong> icon at the bottom of the screen.</li>
                <li>Select <strong>Add to Home Screen</strong>.</li>
                <li>Edit the name if you want, then tap <strong>Add</strong>.</li>
              </ol>
              <div class="alert alert-info d-flex align-items-start gap-2 mt-4 mb-0" role="alert">
                <Info :size="18" class="mt-1" />
                Your home screen will now include a MedBrief icon that launches quickly like an app.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ArrowLeft, ArrowRight, Download, Smartphone, Phone, Info } from 'lucide-vue-next'

const selectedPlatform = ref('android')
const authStore = useAuthStore()
</script>

<style scoped>
.install-hero {
  padding: 2rem;
  border-radius: 24px;
  background: linear-gradient(140deg, rgba(224, 122, 95, 0.12), rgba(255, 255, 255, 0.95));
  border: 1px solid rgba(224, 122, 95, 0.2);
}

.install-topbar__link {
  color: var(--warm-700);
  text-decoration: none;
  font-weight: 600;
  white-space: nowrap;
}

.install-topbar__link:hover {
  color: var(--terracotta-600);
}

.install-badge {
  background: rgba(224, 122, 95, 0.16);
  color: var(--terracotta-600);
  padding: 0.4rem 0.85rem;
  border-radius: 999px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
}

.install-panel {
  border-radius: 24px;
}

.platform-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--terracotta-100);
  color: var(--terracotta-600);
}

.install-steps {
  margin: 0;
  padding-left: 1.4rem;
  color: var(--warm-700);
}

.install-steps li {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

.install-steps li:last-child {
  margin-bottom: 0;
}

@media (max-width: 767.98px) {
  .install-hero {
    padding: 1.5rem;
  }

  .install-panel .card-body {
    padding: 1.5rem;
  }

  .install-topbar {
    flex-wrap: nowrap;
  }
}
</style>
