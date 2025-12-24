<template>
  <div class="page">
    <section class="hero">
      <h1 class="hero-title">지금 뭐 볼까?</h1>
      <p class="hero-sub">인기 / 최신 / 극찬작을 한 번에 둘러보자.</p>
    </section>

    <section class="banner-section" v-if="banners.length > 0">
      <div 
        class="banner-container"
        @mouseenter="stopAutoSlide"
        @mouseleave="startAutoSlide"
      >
        <div 
          class="banner-slide" 
          @click="goBannerLink(banners[currentIndex].link)"
        >
          <img :src="banners[currentIndex].image" class="banner-img" alt="메인 배너" />
          <div class="banner-overlay">
            <span class="banner-label">{{ banners[currentIndex].label }}</span>
            <h2 class="banner-title">{{ banners[currentIndex].title }}</h2>
            <p class="banner-desc">{{ banners[currentIndex].desc }}</p>
          </div>
        </div>

        <button class="banner-nav-btn prev" @click="prevBanner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
        <button class="banner-nav-btn next" @click="nextBanner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>

        <div class="dots-container">
          <span 
            v-for="(banner, index) in banners" 
            :key="index" 
            class="dot" 
            :class="{ active: index === currentIndex }"
            @click="setBanner(index)"
          ></span>
        </div>
      </div>
    </section>

    <hr class="divider" />

    <section class="sec">
      <div class="sec-head">
        <h2 class="sec-title">지금 뜨는 인기 영화</h2>
        <button class="more" @click="goMovies('popular')">더보기</button>
      </div>
      <MovieRow v-if="!loading" title="인기 영화" :movies="popular" @click-movie="goDetail" />
    </section>

    <section class="sec">
      <div class="sec-head">
        <h2 class="sec-title">최신 개봉 작품</h2>
        <button class="more" @click="goMovies('latest')">더보기</button>
      </div>
      <MovieRow v-if="!loading" title="최신 개봉작" :movies="nowPlaying" @click-movie="goDetail" />
    </section>

    <section class="sec">
      <div class="sec-head">
        <h2 class="sec-title">평론가가 극찬한 영화</h2>
        <button class="more" @click="goMovies('rating')">더보기</button>
      </div>
      <MovieRow v-if="!loading" title="평론가 극찬작" :movies="topRated" @click-movie="goDetail" />
    </section>

    <section class="sec">
      <div class="sec-head">
        <h2 class="sec-title">최근 코멘트</h2>
        <button class="more" @click="go('/mypage')">더보기</button>
      </div>
      <p v-if="reviewsLoading" class="muted">불러오는 중...</p>
      
      <div v-else class="review-slider-wrapper">
        <button class="slider-nav-btn left" @click="scrollPrev">‹</button>
        <div class="review-scroll-container" ref="scrollContainer">
          <ReviewCard
            v-for="r in recentReviews"
            :key="r.id"
            :review="r"
            class="slider-item"
            @click="openReviewModal(r)"
          />
        </div>
        <button class="slider-nav-btn right" @click="scrollNext">›</button>
      </div>
    </section>

    <ReviewDetailModal
      v-if="showDetailModal && selectedReview"
      :review="selectedReview"
      :replies="reviewComments"
      :movie="selectedReview.movie" 
      @close="closeDetailModal"
      @submit-reply="handleReplySubmit"
      @toggle-like="handleReviewLike"
      @delete-reply="handleReplyDelete"
      @delete-review="handleReviewDeleteLocal"
      @update-review="handleReviewUpdateLocal"
    />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  fetchHomeSections, 
  fetchRecentReviews, 
  fetchReviewComments, 
  createReviewComment, 
  toggleReviewLike 
} from '@/api/comet.js'

import MovieRow from '@/components/movie/MovieRow.vue'
import ReviewCard from '@/components/review/ReviewCard.vue'
import ReviewDetailModal from '@/components/review/ReviewDetailModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/original'

/* --- [배너 로직: 동적 데이터 & 자동 슬라이드] --- */
const currentIndex = ref(0)
const banners = ref([])
const slideTimer = ref(null)

// 배너 배열 구성 함수
function setupBanners() {
  const list = []

  // 1. 최신 개봉작 랜덤 배너
  if (nowPlaying.value.length > 0) {
    const randomIdx = Math.floor(Math.random() * nowPlaying.value.length)
    const movie = nowPlaying.value[randomIdx]
    list.push({
      image: movie.backdrop_path ? `${TMDB_IMAGE_BASE}${movie.backdrop_path}` : 'https://via.placeholder.com/1600x685?text=Comet+Movie',
      link: `/movies/${movie.tmdb_id || movie.id}`,
      label: '최신 개봉작',
      title: movie.title,
      desc: '지금 바로 혜성에서 상세 정보를 확인하세요.'
    })
  }

  // 2. 최근 리뷰 배너
  if (recentReviews.value.length > 0) {
    const review = recentReviews.value[0]
    list.push({
      image: review.movie?.backdrop_path ? `${TMDB_IMAGE_BASE}${review.movie.backdrop_path}` : 'https://via.placeholder.com/1600x685?text=User+Review',
      link: `/movies/${review.movie?.tmdb_id}`,
      label: '베스트 코멘트',
      title: review.content.length > 25 ? review.content.substring(0, 25) + '...' : review.content,
      desc: `${review.user?.nickname || '익명'}님의 솔직한 리뷰`
    })
  }

  // 3. 가이드 페이지 배너
  list.push({
    image: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2000&auto=format&fit=crop',
    link: '/guide',
    label: '이용 가이드',
    title: '혜성, 어떻게 이용하나요?',
    desc: '서비스 사용법과 꿀팁을 확인해보세요.'
  })

  banners.value = list
}

// 자동 슬라이드 시작
function startAutoSlide() {
  stopAutoSlide() // 중복 방지
  slideTimer.value = setInterval(() => {
    nextBanner()
  }, 5000) // 5초마다 전환
}

// 자동 슬라이드 정지
function stopAutoSlide() {
  if (slideTimer.value) clearInterval(slideTimer.value)
}

function nextBanner() {
  currentIndex.value = (currentIndex.value + 1) % banners.value.length
}
function prevBanner() {
  currentIndex.value = (currentIndex.value - 1 + banners.value.length) % banners.value.length
}
function setBanner(index) {
  currentIndex.value = index
  startAutoSlide() // 클릭 시 타이머 리셋
}
function goBannerLink(link) {
  if (link && link !== '#') router.push(link)
}

/* --- [기존 데이터 로딩 및 리뷰 로직] --- */
const loading = ref(false)
const popular = ref([])
const nowPlaying = ref([])
const topRated = ref([])
const reviewsLoading = ref(false)
const recentReviews = ref([])
const scrollContainer = ref(null)

const showDetailModal = ref(false)
const selectedReview = ref(null)
const reviewComments = ref([])

async function loadHome() {
  loading.value = true
  try {
    const data = await fetchHomeSections(1)
    popular.value = data?.popular ?? []
    nowPlaying.value = data?.now_playing ?? []
    topRated.value = data?.top_rated ?? []
    setupBanners() // 데이터 로드 후 배너 설정
  } finally {
    loading.value = false
  }
}

async function loadRecentReviews() {
  reviewsLoading.value = true
  try {
    const data = await fetchRecentReviews(12)
    recentReviews.value = Array.isArray(data) ? data : (data?.results || [])
    setupBanners() // 리뷰 로드 후 배너 다시 설정
  } finally {
    reviewsLoading.value = false
  }
}

// 슬라이더 이동
const scrollPrev = () => scrollContainer.value?.scrollBy({ left: -scrollContainer.value.clientWidth, behavior: 'smooth' })
const scrollNext = () => scrollContainer.value?.scrollBy({ left: scrollContainer.value.clientWidth, behavior: 'smooth' })

// 모달/액션 함수 (기존과 동일)
async function openReviewModal(review) {
  selectedReview.value = review
  try { reviewComments.value = await fetchReviewComments(review.id) || [] } catch (e) { reviewComments.value = [] }
  showDetailModal.value = true
}
function closeDetailModal() { showDetailModal.value = false; selectedReview.value = null; }
function handleReviewDeleteLocal(id) { recentReviews.value = recentReviews.value.filter(r => r.id !== id); closeDetailModal(); }
function handleReviewUpdateLocal(updated) {
  const idx = recentReviews.value.findIndex(r => r.id === updated.id)
  if (idx !== -1) recentReviews.value[idx] = { ...recentReviews.value[idx], ...updated }
  if (selectedReview.value?.id === updated.id) selectedReview.value = { ...selectedReview.value, ...updated }
}
async function handleReplySubmit(content) {
  if (!authStore.isLoggedIn) return alert('로그인 후 이용해주세요.')
  try {
    await createReviewComment(selectedReview.value.id, content)
    reviewComments.value = await fetchReviewComments(selectedReview.value.id)
  } catch (e) { alert('댓글 작성 실패') }
}
function handleReplyDelete(id) { reviewComments.value = reviewComments.value.filter(c => c.id !== id) }
async function handleReviewLike(id) {
  if (!authStore.isLoggedIn) return alert('로그인 후 이용해주세요.')
  try {
    const res = await toggleReviewLike(id)
    if (selectedReview.value) { selectedReview.value.is_liked = res.liked; selectedReview.value.likes_count = res.like_count; }
    const target = recentReviews.value.find(r => r.id === id)
    if (target) { target.is_liked = res.liked; target.likes_count = res.like_count; }
  } catch (e) { alert('오류 발생') }
}

function goDetail(movie) {
  const tmdbId = movie?.tmdb_id ?? movie?.id
  if (tmdbId) router.push(`/movies/${tmdbId}`)
}
function goMovies(sort) { router.push({ path: '/movies', query: { sort } }) }
function go(path) { router.push(path) }

onMounted(() => {
  loadHome()
  loadRecentReviews()
  startAutoSlide()
})

onUnmounted(() => {
  stopAutoSlide()
})
</script>

<style scoped>
/* 공통 */
.page { max-width: 1100px; margin: 0 auto; padding: 20px 14px 60px; color: var(--text); }
.hero { padding: 26px 0 18px; }
.hero-title { margin: 0; font-size: 44px; font-weight: 900; letter-spacing: -0.02em; }
.hero-sub { margin: 10px 0 0; color: #666; font-weight: 700; }
.divider { border: none; border-top: 1px solid #eee; margin: 18px 0 22px; }
.sec { margin-top: 18px; }
.sec-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.sec-title { margin: 0; font-size: 18px; font-weight: 900; }
.more { border: none; background: transparent; cursor: pointer; color: #666; font-weight: 900; }
.more:hover { text-decoration: underline; color: var(--primary); }

/* 배너 스타일 */
.banner-section { margin-top: 10px; margin-bottom: 30px; }
.banner-container { 
  position: relative; 
  width: 100%; 
  aspect-ratio: 21 / 9; 
  border-radius: 12px; 
  overflow: hidden; 
  background: #000;
}
.banner-slide { width: 100%; height: 100%; cursor: pointer; position: relative; }
.banner-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.banner-slide:hover .banner-img { transform: scale(1.02); }

/* 배너 텍스트 오버레이 */
.banner-overlay {
  position: absolute;
  left: 40px; bottom: 40px;
  color: white;
  z-index: 2;
  text-shadow: 0 2px 10px rgba(0,0,0,0.7);
  max-width: 70%;
  pointer-events: none;
}
.banner-label {
  display: inline-block;
  background: var(--primary, #ff2f6e);
  color: #fff;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 800;
  margin-bottom: 10px;
}
.banner-title { font-size: 32px; font-weight: 900; margin: 0; line-height: 1.2; word-break: keep-all; }
.banner-desc { font-size: 16px; margin: 8px 0 0; opacity: 0.9; }

.banner-nav-btn {
  position: absolute; top: 0; bottom: 0; width: 8%;
  background: transparent; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: rgba(255, 255, 255, 0.4); transition: color 0.3s; z-index: 5;
}
.banner-nav-btn:hover { color: #fff; }
.banner-nav-btn.prev { left: 0; }
.banner-nav-btn.next { right: 0; }
.banner-nav-btn svg { width: 34px; height: 34px; }

.dots-container {
  position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 8px; z-index: 10;
}
.dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: rgba(255, 255, 255, 0.4); cursor: pointer; transition: all 0.2s;
}
.dot.active { background: #fff; transform: scale(1.2); }

/* 리뷰 슬라이더 */
.review-slider-wrapper { position: relative; display: flex; align-items: center; width: 100%; }
.review-scroll-container {
  display: grid; grid-template-rows: repeat(2, 1fr); grid-auto-flow: column;
  grid-auto-columns: calc(33.333% - 10.7px); gap: 16px;
  overflow-x: auto; scroll-behavior: smooth; scroll-snap-type: x mandatory;
  padding: 10px 0; scrollbar-width: none;
}
.review-scroll-container::-webkit-scrollbar { display: none; }
.slider-item { width: 100%; scroll-snap-align: start; cursor: pointer; }

.slider-nav-btn {
  position: absolute; top: 50%; transform: translateY(-50%);
  width: 40px; height: 40px; border-radius: 50%;
  background: #fff; border: 1px solid #eee; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer; z-index: 10; display: flex; align-items: center; justify-content: center;
  font-size: 20px; transition: all 0.2s;
}
.slider-nav-btn:hover { background: var(--primary, #ff2f6e); color: #fff; }
.slider-nav-btn.left { left: -20px; }
.slider-nav-btn.right { right: -20px; }

@media (max-width: 768px) {
  .banner-title { font-size: 24px; }
  .banner-overlay { left: 20px; bottom: 20px; }
  .review-scroll-container { grid-auto-columns: calc(50% - 8px); }
}
</style>