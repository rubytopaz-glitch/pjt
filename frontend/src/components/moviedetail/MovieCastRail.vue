<template>
  <section class="sub-section">
    <h3 class="sub-title">출연/제작</h3>
    <div class="scroll-wrapper">
      <button class="circle-arrow-btn left" @click="scrollCast(-1)">‹</button>
      <div ref="castRail" class="horizontal-scroll">
        <div v-for="p in allCast" :key="p.tmdb_id" class="cast-card" @click="$emit('go-person', p.tmdb_id)">
          <div class="cast-img-box">
            <img v-if="p.profile_path" :src="`https://image.tmdb.org/t/p/w200${p.profile_path}`" />
            <div v-else class="no-img">👤</div>
          </div>
          <div class="cast-text">
            <div class="c-name">{{ p.name }}</div>
            <div class="c-role">{{ p.role_desc }}</div>
          </div>
        </div>
      </div>
      <button class="circle-arrow-btn right" @click="scrollCast(1)">›</button>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
defineProps(['allCast'])
defineEmits(['go-person'])

const castRail = ref(null)
function scrollCast(dir) {
  if (castRail.value) castRail.value.scrollBy({ left: dir * 300, behavior: 'smooth' })
}
</script>

<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.sub-title { 
  font-size: 20px; 
  font-weight: 800; 
  margin-bottom: 20px; 
  color: var(--text); /* 글자색 대응 */
}

.scroll-wrapper { position: relative; }

.horizontal-scroll { 
  display: flex; 
  gap: 14px; 
  overflow-x: auto; 
  scrollbar-width: none; /* 파이어폭스 대응 */
}
.horizontal-scroll::-webkit-scrollbar { display: none; } /* 크롬/사파리 스크롤바 숨김 유지 */

.cast-card { 
  width: 110px; 
  flex-shrink: 0; 
  cursor: pointer; 
  transition: transform 0.2s; 
}
.cast-card:hover { transform: scale(1.05); }

.cast-img-box { 
  width: 110px; 
  height: 110px; 
  border-radius: 6px; 
  overflow: hidden; 
  background: var(--bg); /* #f8f8f8 -> var(--bg) */
  border: 1px solid var(--border); /* #eee -> var(--border) */
  margin-bottom: 8px; 
}

.cast-img-box img { 
  width: 100%; 
  height: 100%; 
  object-fit: cover; 
}

.c-name { 
  font-size: 13px; 
  font-weight: 600; 
  color: var(--text); /* 기본 텍스트색 대응 */
}

.c-role { 
  font-size: 12px; 
  color: var(--muted); /* #888 -> var(--muted) */
}

/* 좌우 이동 버튼 테마 대응 */
.circle-arrow-btn { 
  position: absolute; 
  top: 35px; 
  width: 36px; 
  height: 36px; 
  border-radius: 50%; 
  background: var(--card); /* white -> var(--card) */
  border: 1px solid var(--border); /* #ddd -> var(--border) */
  color: var(--text); /* 화살표 색상 */
  z-index: 10; 
  cursor: pointer; 
  box-shadow: var(--shadow); /* 그림자 테마 대응 */
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.circle-arrow-btn:hover {
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff; /* 호버 시 화살표는 흰색 고정 */
}

.circle-arrow-btn.left { left: -15px; }
.circle-arrow-btn.right { right: -15px; }

/* 버튼 안의 화살표가 SVG일 경우를 대비 */
.circle-arrow-btn svg {
  fill: currentColor;
}
</style>