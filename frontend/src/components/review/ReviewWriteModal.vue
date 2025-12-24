<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3>{{ movieTitle }}</h3>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>
      
      <div class="modal-body">
        <div class="rating-select-area">
          <span class="label">별점 선택</span>
          <div class="stars">
            <span 
              v-for="n in 5" 
              :key="n" 
              class="star-icon" 
              :class="{ active: n <= rating }"
              @click="rating = n"
            >★</span>
          </div>
          <span class="rating-text">{{ rating }}점</span>
        </div>

        <textarea 
          v-model="content" 
          placeholder="이 작품에 대한 생각을 자유롭게 표현해주세요." 
          class="review-input"
          maxlength="10000"
        ></textarea>
      </div>
      
      <div class="modal-footer">
        <button v-if="existingReview" class="delete-btn" @click="onDelete">삭제</button>

        <div class="right-group">
          <div class="text-counter">{{ content.length.toLocaleString() }}/10,000</div>
          <button 
            class="save-btn" 
            :disabled="content.trim().length === 0"
            @click="onSubmit"
          >
            저장
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  movieTitle: { type: String, default: '' },
  // ✅ [중요] 부모로부터 기존 리뷰 데이터 받기
  existingReview: { type: Object, default: null }
})
const emit = defineEmits(['close', 'submit', 'delete'])

const content = ref('')
const rating = ref(5)

// ✅ [중요] 모달 열릴 때 기존 데이터 채우기
onMounted(() => {
  if (props.existingReview) {
    content.value = props.existingReview.content || ''
    rating.value = props.existingReview.rating || 5
  }
})

function onSubmit() {
  if (content.value.trim().length > 0) {
    emit('submit', { content: content.value, rating: rating.value })
  }
}

// ✅ [추가] 삭제 핸들러
function onDelete() {
  if (confirm('정말 삭제하시겠습니까?')) {
    emit('delete', props.existingReview.id)
  }
}
</script>

<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.modal-overlay { 
  position: fixed; inset: 0; 
  background: rgba(0, 0, 0, 0.7); /* 오버레이는 가독성을 위해 어둡게 유지 */
  z-index: 2000; 
  display: flex; align-items: center; justify-content: center; 
  backdrop-filter: blur(4px); /* 배경 흐림으로 몰입감 유도 */
}

.modal-content { 
  background: var(--card); /* white -> var(--card) */
  width: 600px; height: 500px; 
  border-radius: 12px; 
  display: flex; flex-direction: column; overflow: hidden; 
  box-shadow: var(--shadow); /* rgba -> var(--shadow) */
  border: 1px solid var(--border); /* 다크 테마 경계선 확보 */
}

.modal-header { 
  padding: 16px 20px; 
  border-bottom: 1px solid var(--border); /* #eee -> var(--border) */
  display: flex; justify-content: space-between; align-items: center; 
}

.modal-header h3 { 
  margin: 0; font-size: 18px; font-weight: 700; 
  color: var(--text); /* #000 -> var(--text) */
}

.close-btn { 
  background: none; border: none; font-size: 24px; 
  cursor: pointer; color: var(--muted); /* #999 -> var(--muted) */
}

.modal-body { 
  flex: 1; padding: 20px; display: flex; flex-direction: column; 
  background: var(--card);
}

.rating-select-area { 
  display: flex; align-items: center; gap: 10px; 
  margin-bottom: 16px; padding-bottom: 16px; 
  border-bottom: 1px solid var(--border); /* #f5f5f5 -> var(--border) */
}

.label { 
  font-size: 14px; font-weight: 700; 
  color: var(--text); /* #333 -> var(--text) */
}

.stars { display: flex; cursor: pointer; }
.star-icon { 
  font-size: 24px; 
  color: var(--border); /* #e0e0e0 -> var(--border) */
  transition: color 0.2s; margin-right: 2px; 
}
.star-icon.active { color: #ffad1f; } /* 별점 금색은 시인성을 위해 유지 */
.rating-text { font-size: 14px; font-weight: 700; color: #ffad1f; margin-left: 4px; }

.review-input { 
  width: 100%; flex: 1; border: none; outline: none; resize: none; 
  font-size: 16px; line-height: 1.6; 
  background: transparent;
  color: var(--text); /* #333 -> var(--text) */
}
.review-input::placeholder { 
  color: var(--muted); /* #ccc -> var(--muted) */
}

/* 푸터 레이아웃 (양쪽 정렬 유지) */
.modal-footer { 
  padding: 12px 20px; 
  border-top: 1px solid var(--border); /* #eee -> var(--border) */
  display: flex; justify-content: space-between; align-items: center; 
}

.right-group { display: flex; align-items: center; gap: 12px; }

/* 삭제 버튼 스타일 */
.delete-btn { 
  background: none; border: none; 
  color: var(--muted); /* #999 -> var(--muted) */
  font-size: 14px; font-weight: 600; cursor: pointer; text-decoration: underline; 
}
.delete-btn:hover { 
  color: var(--primary); /* #ff2f6e -> var(--primary) 포인트 컬러 */
}

.text-counter { 
  font-size: 13px; 
  color: var(--muted); /* #aaa -> var(--muted) */
  opacity: 0.8;
}

.save-btn { 
  background: var(--primary); /* #ff2f6e -> var(--primary) */
  color: white; border: none; padding: 10px 24px; 
  border-radius: 6px; font-weight: 700; font-size: 15px; 
  cursor: pointer; transition: background 0.2s; 
}
.save-btn:disabled { 
  background: var(--border); /* #e0e0e0 -> var(--border) */
  color: var(--muted); /* #999 -> var(--muted) */
  cursor: not-allowed; 
}
.save-btn:hover:not(:disabled) { 
  opacity: 0.9; 
  filter: brightness(1.1);
}

@media (max-width: 768px) { 
  .modal-content { width: 95%; height: 80vh; } 
}
</style>