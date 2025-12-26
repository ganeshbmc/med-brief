<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-8 text-center text-white">
        <h1 class="display-3 fw-bold mb-4">
          <span class="me-3">📚</span>MedBrief
        </h1>
        <p class="lead mb-5 opacity-90">
          Weekly signals from medical research.<br />
          Stay current without visiting multiple journal sites.
        </p>
        <div class="d-flex gap-3 justify-content-center">
          <router-link to="/register" class="btn btn-light btn-lg px-4 fw-semibold">
            Get Started
          </router-link>
          <router-link to="/login" class="btn btn-outline-light btn-lg px-4">
            Sign In
          </router-link>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="row mt-5 pt-5 g-4">
      <div class="col-md-4">
        <div class="card card-glass text-white p-4 h-100">
          <div class="display-6 mb-3">🔬</div>
          <h5 class="fw-bold">Top Journals</h5>
          <p class="opacity-75">Access articles from NEJM, Lancet, Circulation, and more.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card card-glass text-white p-4 h-100">
          <div class="display-6 mb-3">📋</div>
          <h5 class="fw-bold">Custom Profiles</h5>
          <p class="opacity-75">Create feeds tailored to your specialty or research interests.</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card card-glass text-white p-4 h-100">
          <div class="display-6 mb-3">⏱️</div>
          <h5 class="fw-bold">Weekly Briefs</h5>
          <p class="opacity-75">Get a digest of the last 7 days' publications in seconds.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Home page - no logic needed
</script>
