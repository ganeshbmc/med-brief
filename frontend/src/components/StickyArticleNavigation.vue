<template>
  <div class="sticky-article-nav" v-if="visible">
    <div class="nav-container">
      <button 
        v-if="hasPrev" 
        type="button"
        @click="navigateTo(-1)" 
        class="nav-button"
      >
        <ArrowLeft :size="16" />
        <span class="d-none d-sm-inline">Previous</span>
      </button>
      <div v-else class="spacer d-none d-sm-block"></div>
      
      <button 
        v-if="hasNext" 
        type="button"
        @click="navigateTo(1)" 
        class="nav-button"
      >
        <span class="d-none d-sm-inline">Next</span>
        <ArrowRight :size="16" />
      </button>
      <div v-else class="spacer d-none d-sm-block"></div>
    </div>
  </div>
</template>

<script setup>
import { ArrowLeft, ArrowRight } from 'lucide-vue-next';

// Props
const props = defineProps({
  hasPrev: Boolean,
  hasNext: Boolean,
  visible: { type: Boolean, default: true }
});

// Emits
const emit = defineEmits(['navigate']);

// Methods
const navigateTo = (offset) => {
  emit('navigate', offset);
};
</script>

<style scoped>
.sticky-article-nav {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1060;
  animation: slideUp 0.3s ease-out;
}

.nav-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 0.6rem 1.2rem;
  border-radius: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  border: 1px solid var(--warm-200);
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--terracotta-500);
  text-decoration: none;
  font-weight: 600;
  padding: 0.4rem 1rem;
  border-radius: 2rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-button:hover {
  background-color: var(--terracotta-100);
  text-decoration: none;
  color: var(--terracotta-600);
  transform: translateY(-1px);
}

.nav-button:active {
  transform: translateY(0);
}

.spacer {
  width: 80px; /* Approximate width of "Previous" or "Next" buttons */
}

@keyframes slideUp {
  from {
    transform: translate(-50%, 100px);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}

/* Mobile responsiveness */
@media (max-width: 576px) {
  .sticky-article-nav {
    bottom: 20px;
    width: auto;
  }
  
  .nav-container {
    gap: 0.5rem;
    padding: 0.5rem 0.8rem;
  }

  .nav-button {
    padding: 0.5rem;
  }
}
</style>
