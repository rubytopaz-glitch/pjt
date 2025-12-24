<template>
  <article class="card" @click="goDetail" role="button" tabindex="0">
    <div class="poster-wrap">
      <img v-if="posterSrc" :src="posterSrc" :alt="movie?.title" class="poster" />
      <div v-else class="poster-fallback">No Image</div>
    </div>

    <div class="meta">
      <p class="title">{{ movie?.title }}</p>
      <p class="sub">
        <span v-if="movie?.release_date">{{ movie.release_date?.slice?.(0, 4) }}</span>
        <span v-if="movie?.vote_average"> · ★ {{ Number(movie.vote_average).toFixed(1) }}</span>
      </p>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  movie: { type: Object, required: true },
})

const router = useRouter()

const posterSrc = computed(() => {
  const p = props.movie?.poster_path
  if (!p) return ''
  return `https://image.tmdb.org/t/p/w500${p}`
})

function goDetail() {
  const tmdbId = props.movie?.tmdb_id
  if (!tmdbId) return
  router.push({ name: 'movie-detail', params: { tmdbId } })
}
</script>

<style scoped>
/* 🎨 레이아웃 구조(160px)는 유지하고 색상만 테마 변수로 교체 */

.card {
  width: 160px;
  cursor: pointer;
  user-select: none;
  transition: transform 0.2s ease; /* 호버 시 부드러운 움직임 추가 */
}

.card:hover {
  transform: translateY(-5px); /* 살짝 떠오르는 효과 */
}

.poster-wrap {
  width: 160px;
  height: 240px;
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg); /* #f2f2f2 -> var(--bg) */
  box-shadow: var(--shadow); /* 고정값 -> var(--shadow) */
  border: 1px solid var(--border); /* 다크 테마에서 경계 구분을 위해 추가 */
  transition: border-color 0.3s, box-shadow 0.3s;
}

.poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-fallback {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  color: var(--muted); /* #777 -> var(--muted) */
  font-size: 12px;
  background: var(--input-bg); /* 폴백 배경도 테마 대응 */
}

.meta {
  margin-top: 10px; /* 여백 살짝 조정 */
}

.title {
  font-size: 13px;
  font-weight: 700;
  margin: 0;
  line-height: 1.4;
  color: var(--text); /* #111 -> var(--text) */
  
  /* 기존 2줄 말줄임표 유지 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.3s;
}

.card:hover .title {
  color: var(--primary); /* 호버 시 제목에 테마 포인트 컬러 적용 */
}

.sub {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--muted); /* #666 -> var(--muted) */
  transition: color 0.3s;
}
</style>