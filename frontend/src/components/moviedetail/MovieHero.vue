<template>
  <section class="hero-header">
    <div class="backdrop-bg" :style="{ backgroundImage: `url(https://image.tmdb.org/t/p/original${movie.backdrop_path})` }"></div>
    <div class="backdrop-overlay"></div>

    <div class="container hero-content">
      <div class="hero-text">
        <h1 class="title">{{ movie.title }}</h1>
        <p class="original-title">{{ movie.original_title }}</p>
        
        <div class="meta-info">
          <span>{{ movie.release_date?.slice(0, 4) }}</span>
          <span class="dot">・</span>
          <span>{{ movie.genres?.map(g => g.name).join('/') }}</span>
          <span class="dot">・</span>
          <span>{{ movie.runtime }}분</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  movie: { type: Object, required: true }
})
</script>
<style scoped>
/* 🎨 레이아웃은 유지하고 배경/텍스트를 테마에 완벽 대응 */

.hero-header { 
  position: relative; 
  width: 100%; 
  height: 400px; 
  background: var(--bg); /* #000 -> var(--bg) 테마 배경과 일치 */
  margin-top: -60px; 
  padding-top: 60px; 
  display: flex; 
  align-items: flex-end; 
  overflow: hidden; 
  transition: background-color 0.3s ease;
}

.backdrop-bg { 
  position: absolute; 
  inset: 0; 
  background-size: cover; 
  background-position: center 20%; 
  opacity: 0.5; /* 가독성을 위해 살짝 조절 */
  z-index: 1; 
}

/* ✅ 핵심 수정: 오버레이가 테마 배경색(var(--bg))으로 부드럽게 이어지게 설정 */
.backdrop-overlay { 
  position: absolute; 
  inset: 0; 
  background: linear-gradient(
    to right, 
    var(--bg) 0%, 
    transparent 100%
  ),
  linear-gradient(
    to top,
    var(--bg) 0%,
    transparent 40%
  );
  z-index: 2; 
}

.hero-content { 
  position: relative; 
  z-index: 3; 
  width: 100%; 
  padding-bottom: 30px; 
  margin: 0 auto; 
  max-width: 1100px; 
  padding-left: 20px; 
}

/* ✅ 텍스트 색상을 테마에 대응 (흰색 고정 -> var(--text)) */
.title { 
  font-size: 40px; 
  font-weight: 900; 
  margin: 0 0 6px; 
  color: var(--text); /* #fff -> var(--text) */
}

.original-title { 
  font-size: 14px; 
  opacity: 0.8; 
  margin-bottom: 12px; 
  color: var(--text); /* #fff -> var(--text) */
}

.meta-info { 
  font-size: 15px; 
  color: var(--text); /* #fff -> var(--text) */
  opacity: 0.9;
}

.dot { 
  margin: 0 6px; 
  opacity: 0.5; 
  color: var(--text);
}

.bottom-stats { 
  margin-top: 16px; 
  font-size: 13px; 
  color: var(--muted); /* #fff -> var(--muted) */
}

/* 모바일 대응 (기존 수치 유지) */
@media (max-width: 768px) {
  .hero-header { height: 300px; }
  .title { font-size: 28px; }
}
</style>
