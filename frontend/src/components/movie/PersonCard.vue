<template>
  <article class="card" @click="goDetail">
    <button class="heart-badge" @click.stop="onUnlike">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="#ff2f6e">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
      </svg>
    </button>

    <div class="poster-wrap">
      <img v-if="profileSrc" :src="profileSrc" class="poster" alt="profile" />
      <div v-else class="poster-fallback">No Image</div>
    </div>
    <div class="meta">
      <p class="name">{{ person.name }}</p>
      <p class="dept">{{ person.known_for_department }}</p>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  person: { type: Object, required: true }
})

const emit = defineEmits(['toggle-like']) // ✅ 이벤트 정의 추가
const router = useRouter()

const profileSrc = computed(() => {
  const p = props.person.profile_path
  if (!p) return ''
  return `https://image.tmdb.org/t/p/w500${p}` // w185 -> w500 (화질 개선)
})

function goDetail() {
  if (props.person.tmdb_id) {
    router.push({ name: 'person-detail', params: { tmdbId: props.person.tmdb_id } })
  }
}

// ✅ 좋아요 취소 핸들러
function onUnlike() {
  emit('toggle-like', props.person)
}
</script>

<style scoped>
/* 🎨 레이아웃 구조(120px)는 유지하고 색상만 테마 변수로 교체 */

.card { 
  width: 120px; 
  cursor: pointer; 
  user-select: none; 
  position: relative; /* ✅ 하트 버튼 기준점 유지 */
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
}

/* ✅ 하트 버튼 테마 대응 */
.heart-badge {
  position: absolute; 
  top: 6px; 
  right: 6px; 
  z-index: 5;
  width: 26px; 
  height: 26px;
  /* ✅ 흰색 고정 대신 테마 카드 배경 사용 */
  background: var(--card); 
  border: 1px solid var(--border); 
  border-radius: 50%;
  cursor: pointer; 
  display: flex; 
  align-items: center; 
  justify-content: center;
  box-shadow: var(--shadow);
  transition: all 0.2s;
  padding: 0;
}

.heart-badge:hover { 
  transform: scale(1.2); 
  border-color: var(--primary); /* 호버 시 포인트 컬러 테두리 */
}

/* 하트 아이콘 색상 (SVG나 폰트일 경우 대비) */
.heart-badge svg, .heart-badge i {
  color: var(--muted);
  transition: color 0.2s;
}

/* 활성화된 하트 상태 (필요 시) */
.heart-badge.active svg {
  color: var(--primary);
}

.poster-wrap {
  width: 120px; 
  height: 180px; /* 2:3 비율 유지 */
  border-radius: 12px; 
  overflow: hidden; 
  background: var(--bg); /* #f2f2f2 -> var(--bg) */
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  transition: border-color 0.3s;
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
  background: var(--input-bg);
}

.meta { 
  margin-top: 8px; 
  text-align: center; 
}

.name { 
  font-size: 13px; 
  font-weight: 700; 
  margin: 0; 
  color: var(--text); 
  overflow: hidden; 
  text-overflow: ellipsis; 
  white-space: nowrap; 
  transition: color 0.2s;
}

/* 카드 호버 시 이름 색상 강조 */
.card:hover .name {
  color: var(--primary);
}

.dept { 
  font-size: 11px; 
  color: var(--muted); 
  margin: 2px 0 0; 
}
</style>