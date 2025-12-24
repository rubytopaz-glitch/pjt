<template>
  <section class="panel">
    <div class="head">
      <div>
        <h2 class="h2">[유저 추천]</h2>
        <p class="sub">취향이 비슷한 유저를 찾아 팔로우해보세요.</p>
      </div>

      <button class="ghost" type="button" @click="load" :disabled="loading">
        새로고침
      </button>
    </div>

    <div v-if="loading" class="loading">로딩중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-if="spotlight" class="spotlight">
        <div class="avatar">👤</div>

        <div class="info">
          <p class="name">@{{ spotlight.username }}</p>
          <p class="desc">
            {{ spotlightDesc }}
          </p>

          <div class="stats">
            <span v-if="spotlight.reviews_count != null" class="pill"
              >리뷰 {{ spotlight.reviews_count }}</span
            >
            <span v-if="spotlight.received_likes != null" class="pill"
              >받은 좋아요 {{ spotlight.received_likes }}</span
            >
          </div>

          <div class="cta">
            <button class="btn" type="button" @click="goProfile(spotlight.username)">
              프로필 보기
            </button>

            <button
              v-if="spotlightSource === 'suggested'"
              class="btnOutline"
              type="button"
              :disabled="followLoadingMap[spotlight.username]"
              @click="follow(spotlight.username)"
            >
              {{ followLoadingMap[spotlight.username] ? '처리중...' : '팔로우' }}
            </button>
          </div>
        </div>
      </div>

      <div class="section" v-if="topReviewers.length">
        <div class="sectionHead">
          <h3 class="h3">실시간 유저 활동 TOP</h3>
          <p class="hint">리뷰 작성이 많은 유저</p>
        </div>

        <div class="rankRow">
          <button
            v-for="(u, idx) in topReviewers"
            :key="u.id || u.username || idx"
            class="rankCard"
            type="button"
            @click="goProfile(u.username)"
          >
            <span class="rank">{{ idx + 1 }}</span>
            <div class="rankBody">
              <p class="rankName">@{{ u.username }}</p>
              <p class="rankMeta">리뷰 {{ u.reviews_count ?? 0 }}</p>
            </div>
          </button>
        </div>
      </div>

      <div class="section" v-if="topLiked.length">
        <div class="sectionHead">
          <h3 class="h3">인기 유저 TOP</h3>
          <p class="hint">리뷰 좋아요를 많이 받은 유저</p>
        </div>

        <div class="rankRow">
          <button
            v-for="(u, idx) in topLiked"
            :key="u.id || u.username || idx"
            class="rankCard"
            type="button"
            @click="goProfile(u.username)"
          >
            <span class="rank">{{ idx + 1 }}</span>
            <div class="rankBody">
              <p class="rankName">@{{ u.username }}</p>
              <p class="rankMeta">받은 좋아요 {{ u.received_likes ?? 0 }}</p>
            </div>
          </button>
        </div>
      </div>

      <div class="section" v-if="suggested.length">
        <div class="sectionHead">
          <h3 class="h3">팔로우 추천</h3>
          <p class="hint">아직 팔로우하지 않은 유저</p>
        </div>

        <div class="grid">
          <div v-for="u in suggested" :key="u.id || u.username" class="userCard">
            <div class="uTop">
              <div class="uAvatar">👤</div>
              <div class="uInfo">
                <p class="uName">@{{ u.username }}</p>
                <p class="uMeta">리뷰 {{ u.reviews_count ?? 0 }}</p>
              </div>
            </div>

            <div class="uActions">
              <button class="btnSmall" type="button" @click="goProfile(u.username)">
                프로필
              </button>
              <button
                class="btnSmallOutline"
                type="button"
                :disabled="followLoadingMap[u.username]"
                @click="follow(u.username)"
              >
                {{ followLoadingMap[u.username] ? '처리중...' : '팔로우' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <p v-if="!spotlight && !topReviewers.length && !topLiked.length && !suggested.length" class="empty">
        추천 유저가 아직 없어요.
      </p>
    </div>
  </section>
</template>

<script setup>
/* ✅ 로직은 원본 그대로 100% 유지합니다. */
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchUserRecommends, toggleFollow } from '@/api/comet'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const error = ref('')
const payload = ref({
  top_reviewers: [],
  top_liked: [],
  suggested: [],
})

const followLoadingMap = ref({})

const myName = computed(() => auth.user?.username)

const topReviewers = computed(() => 
  (payload.value?.top_reviewers ?? []).filter(u => u.username !== myName.value)
)
const topLiked = computed(() => 
  (payload.value?.top_liked ?? []).filter(u => u.username !== myName.value)
)
const suggested = computed(() => 
  (payload.value?.suggested ?? []).filter(u => u.username !== myName.value)
)

const spotlightSource = computed(() => {
  if (topLiked.value.length) return 'top_liked'
  if (topReviewers.value.length) return 'top_reviewers'
  if (suggested.value.length) return 'suggested'
  return ''
})

const spotlight = computed(() => {
  if (spotlightSource.value === 'top_liked') return topLiked.value[0]
  if (spotlightSource.value === 'top_reviewers') return topReviewers.value[0]
  if (spotlightSource.value === 'suggested') return suggested.value[0]
  return null
})

const spotlightDesc = computed(() => {
  if (!spotlight.value) return ''
  if (spotlightSource.value === 'top_liked') return '요즘 가장 인기 많은 유저예요. 리뷰 좋아요 반응이 좋아요.'
  if (spotlightSource.value === 'top_reviewers') return '리뷰 활동이 활발한 유저예요. 취향 참고하기 좋아요.'
  return '활동 유저 중 취향이 맞을 확률이 높은 유저를 추천했어요.'
})

function goProfile(username) {
  if (!username) return
  router.push(`/users/${encodeURIComponent(username)}`)
}

async function follow(username) {
  if (!username) return
  followLoadingMap.value = { ...followLoadingMap.value, [username]: true }
  try {
    await toggleFollow(username)
    payload.value.suggested = (payload.value.suggested || []).filter((u) => u.username !== username)
  } catch (e) {
    console.error(e)
    alert('팔로우 처리 중 오류가 발생했어요.')
  } finally {
    followLoadingMap.value = { ...followLoadingMap.value, [username]: false }
  }
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    const res = await fetchUserRecommends()
    payload.value = res || { top_reviewers: [], top_liked: [], suggested: [] }
  } catch (e) {
    console.error(e)
    error.value = '유저 추천을 불러오지 못했어요.'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
/* 🎨 구조와 틀은 그대로 두고, 색상 코드만 변수로 교체했습니다. */

.panel {
  border: 1px solid var(--border); /* #eee -> 변수 */
  border-radius: 16px;
  padding: 16px;
  background: var(--card); /* #fff -> 변수 */
  color: var(--text);      /* 글자색 대응 추가 */
}

.head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}
.h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 900;
  color: var(--text);
}
.sub {
  margin: 6px 0 0;
  color: var(--muted); /* #666 -> 변수 */
  font-weight: 700;
}

.ghost {
  height: 34px;
  padding: 0 10px;
  border-radius: 12px;
  border: 1px solid var(--border); /* #ddd -> 변수 */
  background: var(--bg);          /* #fff -> 변수 */
  color: var(--text);             /* 변수 추가 */
  font-weight: 900;
  cursor: pointer;
}
.ghost:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading,
.error,
.empty {
  padding: 10px 0;
  font-weight: 800;
  color: var(--muted); /* #666 -> 변수 */
}
.error {
  color: var(--primary); /* 에러 강조를 위해 테마색 사용 */
}

/* spotlight */
.spotlight {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 14px;
  border: 1px solid var(--border); /* #eee -> 변수 */
  border-radius: 18px;
  padding: 14px;
  background: var(--bg);           /* #fafafa -> 변수 */
  margin-bottom: 16px;
}
.avatar {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  background: var(--card);       /* #fff -> 변수 */
  border: 1px solid var(--border); /* #eee -> 변수 */
  display: grid;
  place-items: center;
  font-size: 28px;
  color: var(--text);
}
.info .name {
  margin: 0;
  font-weight: 900;
  font-size: 16px;
  color: var(--text);
}
.info .desc {
  margin: 6px 0 0;
  color: var(--text); /* #333 -> 변수 */
  font-weight: 700;
  line-height: 1.45;
}
.stats {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.pill {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid var(--border); /* #e6e6e6 -> 변수 */
  background: var(--card);        /* #fff -> 변수 */
  font-weight: 900;
  color: var(--text);             /* #111 -> 변수 */
  font-size: 12px;
}
.cta {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}
.btn {
  height: 36px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid var(--primary); /* #111 -> 변수 */
  background: var(--primary);      /* #111 -> 변수 */
  color: #fff;                     /* 강조 버튼 글씨는 흰색 유지 */
  font-weight: 900;
  cursor: pointer;
}
.btnOutline {
  height: 36px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid var(--primary); /* #111 -> 변수 */
  background: transparent;          /* #fff -> 투명하게 변경하여 배경 상속 */
  color: var(--primary);           /* #111 -> 변수 */
  font-weight: 900;
  cursor: pointer;
}
.btnOutline:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* sections */
.section {
  margin-top: 18px;
}
.sectionHead {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}
.h3 {
  margin: 0;
  font-weight: 900;
  font-size: 14px;
  color: var(--text);
}
.hint {
  margin: 0;
  color: var(--muted); /* #888 -> 변수 */
  font-weight: 800;
  font-size: 12px;
}

/* horizontal rank row */
.rankRow {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(160px, 200px);
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 6px;
}
.rankRow::-webkit-scrollbar {
  height: 8px;
}
.rankRow::-webkit-scrollbar-thumb {
  background: var(--border); /* #e5e5e5 -> 변수 */
  border-radius: 999px;
}

.rankCard {
  border: 1px solid var(--border); /* #eee -> 변수 */
  background: var(--card);        /* #fff -> 변수 */
  border-radius: 16px;
  padding: 12px;
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 10px;
  text-align: left;
  cursor: pointer;
}
.rank {
  width: 28px;
  height: 28px;
  border-radius: 10px;
  background: var(--primary); /* #111 -> 테마 강조색 사용 */
  color: #fff;
  display: grid;
  place-items: center;
  font-weight: 900;
  font-size: 12px;
}
.rankName {
  margin: 0;
  font-weight: 900;
  color: var(--text);
}
.rankMeta {
  margin: 6px 0 0;
  color: var(--muted); /* #666 -> 변수 */
  font-weight: 800;
  font-size: 12px;
}

/* suggested grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
@media (max-width: 900px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 560px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

.userCard {
  border: 1px solid var(--border); /* #eee -> 변수 */
  border-radius: 16px;
  padding: 12px;
  background: var(--bg);           /* #fafafa -> 변수 */
}
.uTop {
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 10px;
  align-items: center;
}
.uAvatar {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: var(--card);       /* #fff -> 변수 */
  border: 1px solid var(--border); /* #eee -> 변수 */
  display: grid;
  place-items: center;
  color: var(--text);
}
.uName {
  margin: 0;
  font-weight: 900;
  color: var(--text);
}
.uMeta {
  margin: 6px 0 0;
  color: var(--muted); /* #666 -> 변수 */
  font-weight: 800;
  font-size: 12px;
}
.uActions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}
.btnSmall {
  height: 32px;
  padding: 0 10px;
  border-radius: 12px;
  border: 1px solid var(--primary); /* #111 -> 변수 */
  background: var(--primary);      /* #111 -> 변수 */
  color: #fff;
  font-weight: 900;
  cursor: pointer;
}
.btnSmallOutline {
  height: 32px;
  padding: 0 10px;
  border-radius: 12px;
  border: 1px solid var(--primary); /* #111 -> 변수 */
  background: transparent;          /* #fff -> 투명하게 */
  color: var(--primary);           /* #111 -> 변수 */
  font-weight: 900;
  cursor: pointer;
}
.btnSmallOutline:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>