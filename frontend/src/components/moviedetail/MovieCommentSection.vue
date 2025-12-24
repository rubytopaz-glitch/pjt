<template>
  <section class="sub-section">
    <div class="head-row">
      <h3 class="sub-title">코멘트 <span class="cnt">{{ reviews.length }}+</span></h3>
      <span class="more-link" @click="$emit('open-list-modal')">더보기 ></span>
    </div>

    <div v-if="reviews.length === 0" class="no-data">아직 코멘트가 없습니다.</div>
    
    <div v-else class="comment-grid">
      <ReviewCard
        v-for="review in reviews.slice(0, 6)" 
        :key="review.id" 
        :review="review"
        @click="$emit('open-detail-modal', review)"
      />
    </div>
  </section>
</template>

<script setup>
import ReviewCard from '@/components/review/ReviewCard.vue'

// 부모(MovieDetailView)로부터 전달받는 데이터
defineProps({
  reviews: {
    type: Array,
    required: true
  }
})

// 부모에게 전달할 이벤트 정의
defineEmits(['open-list-modal', 'open-detail-modal'])
</script>
<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.head-row { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 20px; 
}

.sub-title { 
  font-size: 20px; 
  font-weight: 800; 
  color: var(--text); /* #000 -> var(--text) */
}

.cnt { 
  color: var(--primary); /* #ff2f6e -> var(--primary) 포인트 컬러 */
  margin-left: 4px; 
}

.more-link { 
  font-size: 14px; 
  color: var(--primary); /* #ff2f6e -> var(--primary) 포인트 컬러 */
  cursor: pointer; 
  font-weight: 700; 
  transition: opacity 0.2s;
}

.more-link:hover {
  opacity: 0.7;
  text-decoration: underline;
}

.no-data { 
  color: var(--muted); /* #999 -> var(--muted) */
  font-size: 14px; 
  padding: 40px 0; 
  text-align: center; 
}

/* 홈 화면의 review-grid와 동일한 레이아웃 유지 */
.comment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2열 구조 유지 */
  gap: 16px;
}

@media (max-width: 640px) {
  .comment-grid { 
    grid-template-columns: 1fr; /* 모바일 1열 유지 */
  }
}
</style>