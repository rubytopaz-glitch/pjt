<template>
  <main class="page">
    <div class="container">
      <div v-if="loading">로딩중...</div>
      <div v-else-if="!person">인물 정보를 불러오지 못했습니다.</div>

      <div v-else>
        <section class="hero">
          <img v-if="profileSrc" class="avatar" :src="profileSrc" />
          <div v-else class="avatar fallback">No Image</div>

          <div class="meta">
            <div class="name-row">
              <h1 class="name">{{ person.name }}</h1>
              
              <button class="heart-btn" type="button" @click.stop="onToggleLike">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="28" height="28" 
                  viewBox="0 0 24 24" 
                  :class="['heart-icon', { active: isLiked }]"
                >
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
              </button>
            </div>

            <p class="dept">{{ person.known_for_department || 'Person' }}</p>

            <div class="tabs">
              <button :class="{active: tab==='cast'}" @click="tab='cast'">출연</button>
              <button :class="{active: tab==='directors'}" @click="tab='directors'">감독</button>
            </div>
          </div>
        </section>

        <section v-if="tab==='cast'">
          <h2 class="h2">출연작</h2>
          <div class="grid">
            <div v-for="m in person.cast" :key="m.movie_tmdb_id" class="card" @click="goMovie(m.movie_tmdb_id)">
              <img v-if="m.poster_path" class="poster" :src="poster(m.poster_path)" />
              <div v-else class="poster fallback">No</div>
              <div class="title">{{ m.movie_title }}</div>
              <div class="sub" v-if="m.character_name">{{ m.character_name }}</div>
            </div>
          </div>
        </section>

        <section v-else>
          <h2 class="h2">감독작</h2>
          <div class="grid">
            <div v-for="m in person.directors" :key="m.movie_tmdb_id" class="card" @click="goMovie(m.movie_tmdb_id)">
              <img v-if="m.poster_path" class="poster" :src="poster(m.poster_path)" />
              <div v-else class="poster fallback">No</div>
              <div class="title">{{ m.movie_title }}</div>
              <div class="sub" v-if="m.job">{{ m.job }}</div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// ✅ [추가] Auth 스토어 및 API 함수 임포트
import { useAuthStore } from '@/stores/auth'
import { fetchPersonDetail, togglePersonLike, fetchMyLikedPeople } from '@/api/comet'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const tmdbId = computed(() => Number(route.params.tmdbId))
const loading = ref(true)
const person = ref(null)
const tab = ref('cast')

// ✅ [추가] 좋아요 상태 관리
const likedIds = ref(new Set())
const isLiked = computed(() => person.value && likedIds.value.has(person.value.id || person.value.tmdb_id))

const profileSrc = computed(() => {
  const p = person.value?.profile_path
  return p ? `https://image.tmdb.org/t/p/w300${p}` : ''
})

const poster = (path) => `https://image.tmdb.org/t/p/w342${path}`

async function load() {
  loading.value = true
  try {
    person.value = await fetchPersonDetail(tmdbId.value)
    tab.value = (person.value?.cast?.length ?? 0) > 0 ? 'cast' : 'directors'
    
    // ✅ [추가] 로그인 상태라면 좋아요 목록 업데이트
    if (authStore.isLoggedIn) {
      await updateLikedList()
    }
  } catch (e) {
    console.error(e)
    person.value = null
  } finally {
    loading.value = false
  }
}

// ✅ [추가] 좋아요 목록 가져오기 함수
async function updateLikedList() {
  try {
    const list = await fetchMyLikedPeople()
    likedIds.value = new Set(list.map(x => x.tmdb_id))
  } catch (e) {
    console.log('좋아요 목록 로드 실패')
  }
}

// ✅ [추가] 좋아요 토글 핸들러
async function onToggleLike() {
  if (!authStore.isLoggedIn) return alert('로그인이 필요합니다.')
  if (!person.value) return

  const p = person.value
  const pId = p.id || p.tmdb_id

  try {
    // UI 선반영 (낙관적 업데이트)
    const next = new Set(likedIds.value)
    if (next.has(pId)) next.delete(pId)
    else next.add(pId)
    likedIds.value = next

    // API 호출
    const res = await togglePersonLike(pId, {
      name: p.name,
      profile_path: p.profile_path,
      known_for_department: p.known_for_department
    })
    
    // 서버 응답으로 최종 확인 (혹시 다르면 보정)
    if (res.liked) next.add(pId)
    else next.delete(pId)
    likedIds.value = new Set(next)

  } catch (error) {
    console.error("좋아요 토글 실패:", error)
    alert("오류가 발생했습니다.")
    await updateLikedList() // 에러 시 원래 상태 복구
  }
}

function goMovie(id) {
  router.push({ name: 'movie-detail', params: { tmdbId: id } })
}

onMounted(load)
watch(tmdbId, load)
</script>

<style scoped>
/* ✅ 배경색을 테마 변수로 변경 */
.page { background: var(--bg, #fff); min-height:calc(100vh - 60px); }
.container { width:min(1100px, 92vw); margin:0 auto; padding:22px 0 60px; }

.hero { display:flex; gap:16px; align-items:center; margin-bottom:18px; }

/* ✅ 아바타 배경색 변경 */
.avatar { width:88px; height:88px; border-radius:18px; object-fit:cover; background: var(--input-bg, #f2f2f2); }
/* ✅ fallback 텍스트 색상 변경 */
.fallback { display:grid; place-items:center; color: var(--muted, #777); }

.meta { display: flex; flex-direction: column; justify-content: center; }

.name-row { display: flex; align-items: center; gap: 8px; }

/* ✅ 이름 텍스트 색상 명시적 지정 */
.name { margin:0; font-size:28px; font-weight:900; color: var(--text, #111); }
/* ✅ 부서 텍스트 색상 변경 */
.dept { margin:6px 0 0; color: var(--muted, #666); font-weight:700; }

.heart-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}
.heart-btn:hover { transform: scale(1.1); }

/* ✅ 하트 아이콘 (비활성 상태) 테마 적용 */
/* fill은 좀 더 밝은 회색 변수, stroke는 일반 테두리 변수 사용 */
.heart-icon {
  fill: var(--heart-inactive, #e0e0e0); 
  stroke: var(--border, #ccc);
  stroke-width: 1;
  transition: all 0.3s ease;
}
/* ✅ 하트 아이콘 (활성 상태) 테마 적용 - 프라이머리 컬러 사용 */
.heart-icon.active {
  fill: var(--primary, #ff2f6e);
  stroke: var(--primary, #ff2f6e);
}

.tabs { display:flex; gap:10px; margin-top:12px; }
/* ✅ 탭 버튼 테마 적용 (테두리, 배경, 글자색) */
.tabs button { 
  height:36px; 
  padding:0 14px; 
  border-radius:999px; 
  border:1px solid var(--border, #ddd); 
  background: var(--card, #fff); 
  color: var(--muted, #666); /* 기본은 회색 */
  font-weight:800; 
  cursor:pointer; 
  transition: all 0.2s; /* 부드러운 전환 추가 */
}
/* ✅ 활성화된 탭 버튼 테마 적용 */
.tabs button.active { 
  border-color: var(--text, #111); 
  color: var(--text, #111); /* 활성화 시 진한 글자색 */
}

/* ✅ 소제목 텍스트 색상 */
.h2 { margin:16px 0 10px; font-size:18px; font-weight:900; color: var(--text, #111); }
.grid { display:grid; grid-template-columns:repeat(6, 1fr); gap:12px; }

/* ✅ 카드 테마 적용 (테두리, 배경) */
.card { cursor:pointer; border:1px solid var(--border, #eee); border-radius:14px; overflow:hidden; background: var(--card, #fff); }
/* ✅ 포스터 스켈레톤 배경색 */
.poster { width:100%; aspect-ratio:2/3; object-fit:cover; background: var(--input-bg, #f2f2f2); }
/* ✅ 카드 제목 색상 */
.title { padding:10px 10px 0; font-weight:900; font-size:13px; color: var(--text, #111); }
/* ✅ 카드 서브 텍스트 색상 */
.sub { padding:6px 10px 10px; color: var(--muted, #666); font-weight:700; font-size:12px; }

@media (max-width: 980px){ .grid{ grid-template-columns:repeat(4, 1fr);} }
@media (max-width: 640px){ .grid{ grid-template-columns:repeat(2, 1fr);} }
</style>