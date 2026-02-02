<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-9 text-center">
        <div class="hero-icon mb-4">
          <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 80px;" />
        </div>
        <p class="hero-kicker">Medical research, distilled</p>
        <h1 class="display-3 fw-bold mb-3 text-warm-dark">Build a reading habit across the journals you trust.</h1>
        <div class="d-flex gap-3 justify-content-center flex-wrap mt-3">
          <router-link to="/register" class="btn btn-primary btn-lg px-4 fw-semibold d-flex align-items-center gap-2">
            <UserPlus :size="20" />
            Get Started
          </router-link>
          <router-link to="/login" class="btn btn-outline-primary btn-lg px-4 d-flex align-items-center gap-2">
            <LogIn :size="20" />
            Sign In
          </router-link>
        </div>
        <router-link to="/install" class="install-callout d-inline-flex align-items-center gap-2 mt-3">
          <Smartphone :size="18" />
          <span>Install on iOS/Android for one-tap access (mobile only).</span>
          <span class="install-callout__cta">Learn how</span>
        </router-link>
      </div>
    </div>

    <div class="landing-advantages mt-5">
      <div class="landing-advantages__header">
        <h2 class="fw-bold text-warm-dark mb-2">Key advantages, distilled.</h2>
        <p class="text-muted mb-0">
          Follow your favorite journals in one place, keep a steady reading rhythm, and share highlights in seconds.
        </p>
      </div>
      <div class="row g-3 mt-2">
        <div class="col-md-6">
          <div class="advantage-item">
            <Calendar :size="18" class="advantage-icon" />
            <div>
              <h3 class="advantage-title">Habit-first cadence</h3>
              <p class="advantage-text">Stay consistent with scheduled reading windows that fit your rhythm.</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="advantage-item">
            <Compass :size="18" class="advantage-icon" />
            <div>
              <h3 class="advantage-title">No site hopping</h3>
              <p class="advantage-text">All your journals in one clean workspace instead of scattered tabs.</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="advantage-item">
            <Share2 :size="18" class="advantage-icon" />
            <div>
              <h3 class="advantage-title">Easy sharing</h3>
              <p class="advantage-text">Send briefs to friends, teams, or colleagues in a few clicks.</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="advantage-item">
            <Users :size="18" class="advantage-icon" />
            <div>
              <h3 class="advantage-title">Profile-driven feeds</h3>
              <p class="advantage-text">Separate specialties into focused views you can return to daily.</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="advantage-item">
            <SlidersHorizontal :size="18" class="advantage-icon" />
            <div>
              <h3 class="advantage-title">Smart filters</h3>
              <p class="advantage-text">Narrow by dates, journals, and abstract availability in seconds.</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="advantage-item">
            <Download :size="18" class="advantage-icon" />
            <div>
              <h3 class="advantage-title">Export-ready briefs</h3>
              <p class="advantage-text">PDF, RIS, and NBIB exports for sharing and citations.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  UserPlus,
  LogIn,
  Users,
  Download,
  Smartphone,
  Calendar,
  Share2,
  Compass,
  SlidersHorizontal
} from 'lucide-vue-next'
</script>

<style scoped>
.hero-icon {
  display: inline-block;
}

.hero-kicker {
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.75rem;
  color: var(--warm-500);
  margin-bottom: 1rem;
}

.landing-advantages {
  background: var(--surface-elevated);
  border: 1px solid var(--warm-200);
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: var(--shadow-1);
}

.landing-advantages__header {
  max-width: 560px;
}

.advantage-item {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  padding: 1rem 1.1rem;
  border-radius: 16px;
  background: #FFFFFF;
  border: 1px solid var(--warm-200);
}

.advantage-icon {
  color: var(--terracotta-600);
  flex-shrink: 0;
  margin-top: 0.2rem;
}

.advantage-title {
  font-size: 0.98rem;
  font-weight: 600;
  color: var(--warm-900);
  margin-bottom: 0.2rem;
}

.advantage-text {
  color: var(--warm-600);
  margin: 0;
  font-size: 0.9rem;
}

.install-callout {
  padding: 0.6rem 1.1rem;
  border-radius: 999px;
  background: var(--surface-elevated);
  border: 1px solid var(--warm-200);
  color: var(--warm-600);
  font-size: 0.9rem;
  flex-wrap: wrap;
  justify-content: center;
  text-decoration: none;
}

.install-callout__cta {
  color: var(--terracotta-600);
  font-weight: 600;
}

.install-callout:hover {
  text-decoration: underline;
}

@media (max-width: 767.98px) {
  .landing-advantages {
    padding: 1.8rem;
  }
}
</style>
