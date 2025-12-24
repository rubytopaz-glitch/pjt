<template>
  <div class="review-card" @click="$emit('click', review)">
    <div class="card-header">
      <div class="user-info">
        <img 
          v-if="review.user && review.user.profile_image" 
          :src="review.user.profile_image" 
          class="profile-img" 
          alt="profile"
        >
        <div v-else class="profile-icon">👤</div>
        <span class="username">{{ review.user?.username || '익명' }}</span>
      </div>
      <div class="rating">★ {{ review.rating }}</div>
    </div>

    <div class="card-body">
      <div v-if="review.movie" class="movie-layout">
        <div class="poster-box">
          <img 
            v-if="review.movie.poster_path"
            :src="`https://image.tmdb.org/t/p/w200${review.movie.poster_path}`" 
            class="poster-img"
            alt="poster"
          />
          <div v-else class="no-poster">No Image</div>
        </div>
        
        <div class="text-box">
          <h4 class="movie-title">{{ review.movie.title }}</h4>
          <p class="content-text">{{ review.content }}</p>
        </div>
      </div>

      <div v-else class="text-only">
        <p class="content-text">{{ review.content }}</p>
      </div>
    </div>

    <div class="card-footer">
      <div class="footer-item">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon-gray">
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
        <span class="count-text">{{ review.likes_count || 0 }}</span>
      </div>
      <div class="footer-item">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon-gray">
          <path fill-rule="evenodd" d="M4.804 21.644A6.707 6.707 0 006 21.75a6.721 6.721 0 003.583-1.029c.774.182 1.584.279 2.417.279 5.322 0 9.75-3.97 9.75-9 0-5.03-4.428-9-9.75-9s-9.75 3.97-9.75 9c0 2.409 1.025 4.562 2.632 6.19l-2.484 3.032.006.003zM12 12.75a.75.75 0 01-.75-.75V9a.75.75 0 011.5 0v3a.75.75 0 01-.75.75zm0-6a.75.75 0 01.75-.75h.008a.75.75 0 01.75.75v.008a.75.75 0 01-.75.75H12a.75.75 0 01-.75-.75V6.75z" clip-rule="evenodd" />
        </svg>
        <span class="count-text">{{ review.comments_count || 0 }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  review: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>

.review-card {
  background: var(--card); /* #fff -> var(--card) */
  border: 1px solid var(--border); /* #e3e3e3 -> var(--border) */
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 190px; /* 카드 높이 고정 유지 */
  box-sizing: border-box;
  color: var(--text); /* 기본 텍스트 색상 대응 */
}

.review-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow); /* 고정값 -> var(--shadow) 테마 대응 */
}

/* 1. 헤더 스타일 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}
.profile-img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--border); /* #eee -> var(--border) */
}
.profile-icon {
  font-size: 22px;
  color: var(--muted); /* #ccc -> var(--muted) */
}
.username {
  font-weight: 700;
  font-size: 13px;
  color: var(--text); /* #333 -> var(--text) */
}
.rating {
  font-size: 12px;
  font-weight: 700;
  background: var(--bg); /* #fff -> var(--bg) */
  border: 1px solid var(--border); /* #eee -> var(--border) */
  padding: 2px 8px;
  border-radius: 4px;
  color: var(--text); /* #333 -> var(--text) */
}

/* 2. 바디 스타일 (포스터 레이아웃) */
.card-body {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.movie-layout {
  display: flex;
  gap: 12px;
  height: 100%;
  align-items: flex-start;
}

.poster-box {
  flex-shrink: 0;
  width: 45px;
  height: 68px;
  border-radius: 4px;
  overflow: hidden;
  background: var(--bg); /* #f0f0f0 -> var(--bg) */
  border: 1px solid var(--border); /* #eee -> var(--border) */
}
.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.no-poster {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  color: var(--muted); /* #999 -> var(--muted) */
}

.text-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.movie-title {
  margin: 0 0 6px 0;
  font-size: 14px;
  font-weight: 800;
  color: var(--text); /* #222 -> var(--text) */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.content-text {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text); /* #666 -> var(--text) */
  opacity: 0.85; /* 본문 텍스트는 가독성을 위해 살짝 불투명도 조절 */
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.text-only .content-text {
  -webkit-line-clamp: 4;
}

/* 3. 푸터 스타일 (회색 아이콘) */
.card-footer {
  display: flex;
  gap: 12px;
  border-top: 1px solid var(--border); /* #f5f5f5 -> var(--border) */
  padding-top: 10px;
  margin-top: auto;
}
.footer-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--muted); /* #888 -> var(--muted) */
}
.icon-gray {
  width: 16px;
  height: 16px;
  color: var(--muted); /* #999 -> var(--muted) */
}
.count-text {
  font-weight: 500;
  color: var(--muted);
}
</style>