<template>
  <section class="row">
    <div class="row-head">
      <h2 class="row-title">{{ title }}</h2>

      <div class="actions">
        <button class="nav-btn" @click="scrollLeft">‹</button>
        <button class="nav-btn" @click="scrollRight">›</button>
      </div>
    </div>

    <div ref="rail" class="rail">
      <MovieCard
        v-for="m in movies"
        :key="m.tmdb_id"
        :movie="m"
      />
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import MovieCard from './MovieCard.vue'

defineProps({
  title: { type: String, required: true },
  movies: { type: Array, default: () => [] },
})

const rail = ref(null)

function scrollLeft() {
  rail.value?.scrollBy({ left: -800, behavior: 'smooth' })
}
function scrollRight() {
  rail.value?.scrollBy({ left: 800, behavior: 'smooth' })
}
</script>

<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.row {
  margin: 26px 0;
}

.row-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.row-title {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: var(--text); /* #111 -> var(--text) */
}

.actions {
  display: flex;
  gap: 8px;
}

.nav-btn {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--card);
  cursor: pointer;
  font-size: 18px;
  color: var(--text);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ✅ 중복 코드를 정리하고 호버 효과 유지 */
.nav-btn:hover:not(:disabled) {
  background: var(--primary);     
  border-color: var(--primary);
  color: #ffffff;                  /* 호버 시 화살표는 흰색 고정 */
  transform: scale(1.1);           
}

.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* 더보기 버튼 스타일 */
.more { 
  border: none; 
  background: transparent; 
  cursor: pointer; 
  color: var(--muted); 
  font-weight: 900; 
  font-size: 13px;
  transition: color 0.2s;
}
.more:hover { 
  text-decoration: underline; 
  color: var(--primary); 
}

/* 영화들이 지나가는 레일 */
.rail {
  display: flex;
  gap: 14px;
  overflow-x: auto;
  padding: 4px 2px 12px;
  scroll-behavior: smooth;
}

/* ✅ 스크롤바 테마 대응 */
.rail::-webkit-scrollbar {
  height: 6px; /* 높이 살짝 최적화 */
}
.rail::-webkit-scrollbar-thumb {
  background: var(--border); /* rgba(0,0,0,0.12) -> var(--border) */
  border-radius: 999px;
}
.rail::-webkit-scrollbar-thumb:hover {
  background: var(--muted);
}
</style>