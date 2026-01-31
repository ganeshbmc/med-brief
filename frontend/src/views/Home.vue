<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-9 text-center">
        <div class="hero-icon mb-4">
          <img src="@/assets/medbrief_icon.png" alt="MedBrief" class="logo-icon" style="height: 80px;" />
        </div>
        <p class="hero-kicker">Medical research, distilled</p>
        <h1 class="display-3 fw-bold mb-4 text-warm-dark">Your research brief, on your schedule.</h1>
        <p class="lead mb-5 text-muted">
          A premium, calm reading experience that turns dense publication streams into a personalized dashboard.
        </p>
        <div class="d-flex gap-3 justify-content-center flex-wrap">
          <router-link to="/register" class="btn btn-primary btn-lg px-4 fw-semibold d-flex align-items-center gap-2">
            <UserPlus :size="20" />
            Get Started
          </router-link>
          <router-link to="/login" class="btn btn-outline-primary btn-lg px-4 d-flex align-items-center gap-2">
            <LogIn :size="20" />
            Sign In
          </router-link>
        </div>
      </div>
    </div>

    <div class="editorial-panel mt-5">
      <div class="row align-items-center gy-4">
        <div class="col-lg-6">
          <h3 class="fw-bold text-warm-dark mb-3">A research ritual, not a backlog.</h3>
          <p class="text-muted mb-0">
            Track the journals that matter to you, apply your reading preferences, and export what you need —
            without context switching across tabs.
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
            <Clock :size="34" />
          </div>
          <h5 class="fw-bold text-warm-dark">Flexible cadence</h5>
          <p class="text-muted">Catch up in minutes with curated windows and export-ready briefs.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { UserPlus, LogIn, Microscope, Users, Clock } from 'lucide-vue-next'
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

@media (max-width: 767.98px) {
  .editorial-panel {
    padding: 2rem;
  }
}
</style>
