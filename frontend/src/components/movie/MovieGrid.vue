<template>
  <div class="grid">
    <MovieCard v-for="m in movies" :key="m.tmdb_id ?? m.id" :movie="m" />
  </div>
</template>

<script setup>
import MovieCard from './MovieCard.vue'

defineProps({
  movies: { type: Array, default: () => [] },
})
</script>

<style scoped>
.grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (min-width: 900px) {
  .grid { grid-template-columns: repeat(5, minmax(0, 1fr)); }
}
</style>
