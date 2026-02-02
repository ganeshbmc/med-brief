<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-9 text-center">
        <div class="hero-icon mb-4">
          <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 80px;" />
        </div>
        <p class="hero-kicker">Medical research, distilled</p>
        <h1 class="display-3 fw-bold mb-4 text-warm-dark">Build a reading habit across the journals you trust.</h1>
        <p class="lead mb-4 text-muted">
          MedBrief keeps new issues in one calm dashboard, so you avoid hopping across publisher sites and share key
          reads with friends and colleagues in seconds.
        </p>
        <div class="row g-3 justify-content-center advantage-strip">
          <div class="col-md-4">
            <div class="advantage-card h-100">
              <div class="advantage-icon">
                <Calendar :size="20" />
              </div>
              <div>
                <h3 class="advantage-title">Habit-friendly cadence</h3>
                <p class="advantage-text">Stay consistent with focused, scheduled reading windows.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="advantage-card h-100">
              <div class="advantage-icon">
                <Globe :size="20" />
              </div>
              <div>
                <h3 class="advantage-title">No site hopping</h3>
                <p class="advantage-text">Everything you follow lives in one streamlined workspace.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="advantage-card h-100">
              <div class="advantage-icon">
                <Share2 :size="20" />
              </div>
              <div>
                <h3 class="advantage-title">Easy sharing</h3>
                <p class="advantage-text">Send briefs to teams or peers without extra steps.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="d-flex gap-3 justify-content-center flex-wrap mt-4">
          <router-link to="/register" class="btn btn-primary btn-lg px-4 fw-semibold d-flex align-items-center gap-2">
            <UserPlus :size="20" />
            Get Started
          </router-link>
          <router-link to="/login" class="btn btn-outline-primary btn-lg px-4 d-flex align-items-center gap-2">
            <LogIn :size="20" />
            Sign In
          </router-link>
        </div>
        <div class="install-callout d-inline-flex align-items-center gap-2 mt-4">
          <Smartphone :size="18" />
          <span>Install on iOS/Android for one-tap access (mobile only).</span>
          <router-link to="/install" class="text-terracotta fw-semibold">Learn how</router-link>
        </div>
      </div>
    </div>

    <div class="editorial-panel mt-5">
      <div class="row align-items-center gy-4">
        <div class="col-lg-6">
          <h3 class="fw-bold text-warm-dark mb-3">A focused ritual, without the overhead.</h3>
          <p class="text-muted mb-0">
            Track the journals that matter, apply your reading preferences, and export what you need from one place.
          </p>
        </div>
        <div class="col-lg-6">
          <div class="hero-metrics">
            <div class="metric-tile">
              <span class="metric-label">Profiles</span>
              <span class="metric-value">Tailored feeds by specialty</span>
            </div>
            <div class="metric-tile">
              <span class="metric-label">Filters</span>
              <span class="metric-value">Dates, journals, abstracts</span>
            </div>
            <div class="metric-tile">
              <span class="metric-label">Exports</span>
              <span class="metric-value">PDF, RIS, NBIB in one click</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-5 pt-3 g-4">
      <div class="col-md-4">
        <div class="card feature-card feature-card--accent h-100">
          <div class="feature-icon mb-3">
            <Microscope :size="34" />
          </div>
          <h5 class="fw-bold text-warm-dark">Journal signal</h5>
          <p class="text-muted">Stay ahead with focused coverage from the journals you already trust.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card feature-card h-100">
          <div class="feature-icon mb-3">
            <Users :size="34" />
          </div>
          <h5 class="fw-bold text-warm-dark">Profile-driven</h5>
          <p class="text-muted">Separate surgery, cardiology, or trials into clean, navigable feeds.</p>
        </div>
      </div>
      <div class="col-md-4">
          <div class="card feature-card h-100">
            <div class="feature-icon mb-3">
              <Download :size="34" />
            </div>
            <h5 class="fw-bold text-warm-dark">Export-ready briefs</h5>
            <p class="text-muted">Shareable PDF, RIS, and NBIB exports for teams and citations.</p>
          </div>
        </div>
      </div>
  </div>
</template>

<script setup>
import { UserPlus, LogIn, Microscope, Users, Download, Smartphone, Calendar, Globe, Share2 } from 'lucide-vue-next'
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

.editorial-panel {
  background: var(--surface-elevated);
  border: 1px solid var(--warm-200);
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: var(--shadow-1);
}

.advantage-strip {
  max-width: 960px;
  margin: 0 auto 2.5rem;
}

.advantage-card {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 1.2rem 1.4rem;
  border-radius: 18px;
  background: #FFFFFF;
  border: 1px solid var(--warm-200);
  box-shadow: var(--shadow-1);
  text-align: left;
}

.advantage-icon {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--terracotta-100);
  color: var(--terracotta-600);
  flex-shrink: 0;
}

.advantage-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--warm-900);
  margin-bottom: 0.3rem;
}

.advantage-text {
  color: var(--warm-600);
  margin: 0;
  font-size: 0.9rem;
}

.hero-metrics {
  display: grid;
  gap: 1rem;
}

.metric-tile {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 1rem 1.25rem;
  border: 1px solid rgba(231, 226, 220, 0.9);
}

.metric-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--warm-500);
  margin-bottom: 0.35rem;
}

.metric-value {
  font-weight: 600;
  color: var(--warm-900);
}

.feature-card {
  padding: 2rem 1.75rem;
  border-radius: 20px;
  border: 1px solid var(--warm-200);
  transition: transform var(--duration-medium) var(--ease-standard),
    box-shadow var(--duration-medium) var(--ease-standard);
}

.feature-card--accent {
  background: linear-gradient(140deg, rgba(224, 122, 95, 0.15), rgba(255, 255, 255, 0.9));
  border-color: rgba(224, 122, 95, 0.25);
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-2);
}

.feature-icon {
  display: inline-flex;
  padding: 0.9rem;
  background: var(--terracotta-100);
  border-radius: 999px;
  color: var(--terracotta-600);
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
}

.install-callout a {
  text-decoration: none;
}

.install-callout a:hover {
  text-decoration: underline;
}

@media (max-width: 767.98px) {
  .editorial-panel {
    padding: 2rem;
  }
}
</style>
