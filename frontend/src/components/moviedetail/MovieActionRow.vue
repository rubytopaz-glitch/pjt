<template>
  <div class="info-area">
    <div class="rating-row">
      <div class="rating-stars">
        <div class="star-bg">★★★★★★★★★★</div>
        <div class="star-fill" :style="{ width: starWidth }">★★★★★★★★★★</div>
      </div>
      <div class="rating-score">
        <span class="score-num">{{ voteScore }}</span>
        <span class="score-label">평균 별점 ({{ voteCount }}명)</span>
      </div>
    </div>

    <div class="divider"></div>

    <div class="action-row">
      <button class="act-btn" :class="{ active: isLiked }" @click="$emit('toggle-like')">
        <div class="icon-box">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="svg-icon heart"><path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001z" /></svg>
        </div>
        <span class="act-label">좋아요</span>
      </button>

      <button class="act-btn" @click="$emit('open-write-modal')">
        <div class="icon-box">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="svg-icon"><path d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-12.15 12.15a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32L19.513 8.2z" /></svg>
        </div>
        <span class="act-label">코멘트</span>
      </button>

      <button class="act-btn" :class="{ active: isWished }" @click="$emit('toggle-wish')">
        <div class="icon-box">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="svg-icon"><path d="M12 15a3 3 0 100-6 3 3 0 000 6z" /><path fill-rule="evenodd" d="M1.323 11.447C2.811 6.976 7.028 3.75 12.001 3.75c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113-1.487 4.471-5.705 7.697-10.677 7.697-4.97 0-9.186-3.223-10.675-7.69a1.762 1.762 0 010-1.113zM17.25 12a5.25 5.25 0 11-10.5 0 5.25 5.25 0 0110.5 0z" clip-rule="evenodd" /></svg>
        </div>
        <span class="act-label">보고싶어요</span>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps(['isLiked', 'isWished', 'starWidth', 'voteScore', 'voteCount'])
defineEmits(['toggle-like', 'toggle-wish', 'open-write-modal'])
</script>

<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.rating-row { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 10px 0 20px; 
}

/* 별점 컨테이너 */
.rating-stars { 
  position: relative; 
  font-size: 32px; 
  color: var(--border); /* #eee -> var(--border) (비활성 별 색상) */
  line-height: 1; 
  letter-spacing: -2px; 
}

.star-bg { 
  color: var(--border); /* #e0e0e0 -> var(--border) */
}

.star-fill { 
  position: absolute; 
  top: 0; 
  left: 0; 
  color: #ffad1f; /* 별점 금색은 시각적 가독성을 위해 유지 */
  overflow: hidden; 
  white-space: nowrap; 
}

.score-num { 
  font-size: 32px; 
  font-weight: 700; 
  color: var(--text); /* #333 -> var(--text) */
  margin-right: 8px; 
}

.score-label { 
  font-size: 13px; 
  color: var(--muted); /* #888 -> var(--muted) */
}

.divider { 
  height: 1px; 
  background: var(--border); /* #ededed -> var(--border) */
  margin: 0; 
  width: 100%; 
}

/* 액션 바 (좋아요, 북마크 등) */
.action-row { 
  display: flex; 
  gap: 40px; 
  padding: 20px 0; 
}

.act-btn { 
  background: transparent; 
  border: none; 
  cursor: pointer; 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  gap: 6px; 
  color: var(--text); /* #292a32 -> var(--text) */
  transition: transform 0.2s, color 0.2s;
}

.act-btn:hover {
  transform: scale(1.05);
  color: var(--primary); /* 호버 시 테마 포인트 컬러 */
}

.act-btn.active { 
  color: var(--primary); /* #ff2f6e -> var(--primary) */
}

.act-btn.active .svg-icon { 
  fill: var(--primary); /* 아이콘 색상도 테마에 맞춰 변경 */
}

.svg-icon { 
  width: 24px; 
  height: 24px; 
  fill: currentColor; /* 부모인 .act-btn의 color를 따르도록 설정 */
  transition: fill 0.2s;
}
</style>