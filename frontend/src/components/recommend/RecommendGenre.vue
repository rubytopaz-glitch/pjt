<template>
  <div class="wrap">
    <h2 class="h2">[장르 추천]</h2>

    <div class="chips" v-if="genres.length">
      <button
        v-for="g in genres"
        :key="g.tmdb_id"
        class="chip"
        :class="{ active: String(g.tmdb_id) === String(selectedGenreId) }"
        type="button"
        @click="selectGenre(g.tmdb_id)"
      >
        {{ g.name }}
      </button>

      <button class="chip arrow" type="button" @click="scrollChips('right')">›</button>
    </div>

    <div v-else class="chips-skeleton">
      <div class="chip sk" v-for="n in 5" :key="n"></div>
    </div>

    <div v-if="loadingMovies" class="loading">로딩중...</div>

    <div v-else-if="movies.length" class="grid">
      <button
        v-for="m in movies"
        :key="m.tmdb_id"
        class="card"
        type="button"
        @click="goMovie(m.tmdb_id)"
        :title="m.title"
      >
        <div class="poster">
          <img v-if="m.poster_path" :src="posterUrl(m.poster_path)" alt="" />
          <div v-else class="noimg">No Image</div>
        </div>

        <div class="meta">
          <p class="title">{{ m.title }}</p>
          <div class="stars">
            <span class="star" v-for="i in 5" :key="i" :class="{ on: i <= starCount(m.vote_average) }">★</span>
          </div>
        </div>
      </button>
    </div>

    <div v-else class="empty">해당 장르 추천 영화가 아직 없어요.</div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchGenreRecommends } from '@/api/comet'

const router = useRouter()

const genres = ref([])
const selectedGenreId = ref(null)

const movies = ref([])
const loadingGenres = ref(false)
const loadingMovies = ref(false)

function posterUrl(path) {
  return path ? `https://image.tmdb.org/t/p/w342${path}` : ''
}

// TMDB vote_average(0~10) -> 0~5 별로 변환
function starCount(voteAvg) {
  const v = Number(voteAvg || 0)
  return Math.max(0, Math.min(5, Math.round(v / 2)))
}

function goMovie(tmdbId) {
  router.push({ name: 'movie-detail', params: { tmdbId } })
}

async function loadGenres() {
  loadingGenres.value = true
  try {
    const res = await fetchGenreRecommends() // genre 없이 호출 => 장르 목록
    genres.value = Array.isArray(res?.genres) ? res.genres : []
    if (genres.value.length && !selectedGenreId.value) {
      selectedGenreId.value = genres.value[0].tmdb_id
    }
  } finally {
    loadingGenres.value = false
  }
}

async function loadMoviesByGenre(genreId) {
  if (!genreId) return
  loadingMovies.value = true
  try {
    const res = await fetchGenreRecommends({ genre: genreId }) // genre 파라미터 => 영화 리스트
    movies.value = Array.isArray(res?.results) ? res.results : []
  } finally {
    loadingMovies.value = false
  }
}

async function selectGenre(genreId) {
  selectedGenreId.value = genreId
  await loadMoviesByGenre(genreId)
}

function scrollChips() {
  // 스크롤 로직 필요시 추가
}

onMounted(async () => {
  await loadGenres()
  await loadMoviesByGenre(selectedGenreId.value)
})
</script>

<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.wrap {
  border: 1px solid var(--border); /* #eee -> var(--border) */
  border-radius: 16px;
  padding: 16px;
  background: var(--card); /* #fff -> var(--card) */
  color: var(--text);      /* 글자색 대응 추가 */
}

.h2 {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 900;
  color: var(--text);
}

/* chips */
.chips {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 14px;
  flex-wrap: nowrap;
  overflow-x: auto;
  padding-bottom: 4px;
}
.chips::-webkit-scrollbar { height: 6px; }
.chips::-webkit-scrollbar-thumb { background: var(--border); border-radius: 999px; }

.chip {
  height: 34px;
  padding: 0 14px;
  border-radius: 12px;
  border: 1px solid var(--border); /* #e6e6e6 -> var(--border) */
  background: var(--bg);          /* #f2f2f2 -> var(--bg) */
  color: var(--text);             /* 글자색 추가 */
  font-weight: 900;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}
.chip.active {
  background: var(--primary);    /* #111 -> var(--primary) */
  border-color: var(--primary);
  color: #fff;                   /* 활성화 시 글자색 흰색 유지 */
}
.chip.arrow {
  margin-left: auto;
  width: 34px;
  padding: 0;
  border-radius: 10px;
}

/* skeleton */
.chips-skeleton {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
}
.chip.sk {
  width: 80px;
  background: var(--bg);         /* #f2f2f2 -> var(--bg) */
  border-color: var(--border);    /* #f2f2f2 -> var(--border) */
}

/* grid */
.grid {
  margin-top: 14px;
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(auto-fill, minmax(160px, 190px));
  justify-content: center;
}
@media (max-width: 900px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 560px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

.card {
  width: 100%;
  max-width: 190px;
  border: 0;
  padding: 0;
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.poster {
  width: 100%;
  aspect-ratio: 2 / 3;
  border-radius: 10px;
  overflow: hidden;
  background: #111; /* 포스터 로딩 전 배경은 어둡게 유지 */
  display: grid;
  place-items: center;
}

.poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.noimg { color: #fff; font-weight: 900; font-size: 12px; opacity: 0.8; }

.meta { padding-top: 8px; }
.title {
  margin: 0 0 6px;
  font-weight: 900;
  font-size: 13px;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text); /* 고정 색상 제거 -> var(--text) */
}

.stars { display: flex; gap: 2px; }
.star { font-size: 12px; color: var(--muted); } /* #d9d9d9 -> var(--muted) */
.star.on { color: #f5c518; } /* 별 점등 색상은 테마 무관 고정 */

.loading, .empty {
  padding: 14px 0;
  font-weight: 800;
  color: var(--muted); /* #666 -> var(--muted) */
}
</style>