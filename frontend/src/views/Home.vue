<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-8 text-center">
        <div class="hero-icon mb-4">
          <img src="@/assets/medbrief_icon.png" alt="MedBrief" style="height: 80px;" />
        </div>
        <h1 class="display-3 fw-bold mb-4 text-warm-dark">
          MedBrief
        </h1>
        <p class="lead mb-5 text-muted">
          Weekly signals from medical research.<br />
          Stay current without visiting multiple journal sites.
        </p>
        <div class="d-flex gap-3 justify-content-center">
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

    <!-- Features Section -->
    <div class="row mt-5 pt-5 g-4">
      <div class="col-md-4">
        <div class="card feature-card p-4 h-100 text-center">
          <div class="feature-icon mb-3">
            <Microscope :size="40" class="text-terracotta" />
          </div>
          <h5 class="fw-bold text-warm-dark">Top Journals</h5>
          <p class="text-muted">Access articles from NEJM, Lancet, Circulation, and more.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card feature-card p-4 h-100 text-center">
          <div class="feature-icon mb-3">
            <Users :size="40" class="text-terracotta" />
          </div>
          <h5 class="fw-bold text-warm-dark">Custom Profiles</h5>
          <p class="text-muted">Create feeds tailored to your specialty or research interests.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card feature-card p-4 h-100 text-center">
          <div class="feature-icon mb-3">
            <Clock :size="40" class="text-terracotta" />
          </div>
          <h5 class="fw-bold text-warm-dark">Weekly Briefs</h5>
          <p class="text-muted">Get a digest of the last 7 days' publications in seconds.</p>
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
  padding: 1.5rem;
  background: var(--terracotta-100);
  border-radius: 50%;
}

.feature-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-icon {
  display: inline-flex;
  padding: 1rem;
  background: var(--terracotta-100);
  border-radius: 50%;
}
</style>
