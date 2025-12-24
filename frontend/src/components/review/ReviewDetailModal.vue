<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <div class="user-profile clickable" @click="goToUserProfile">
          <img v-if="review.user.profile_image" :src="review.user.profile_image" class="u-img">
          <div v-else class="u-icon">👤</div>
          <span class="u-name">{{ review.user.username }}</span>
        </div>

        <div class="header-right">
          <div v-if="isMyReview" class="my-actions">
            <button class="action-text" @click="openEditModal">수정</button>
            <span class="divider-bar">|</span>
            <button class="action-text" @click="onDeleteReview">삭제</button>
          </div>
          <button class="close-btn" @click="$emit('close')">✕</button>
        </div>
      </div>

      <div class="modal-body">
        <div class="review-meta-row">
          <div class="small-poster" v-if="posterUrl" @click="goToMovieDetail">
            <img :src="posterUrl" alt="Poster">
          </div>

          <div class="meta-info">
            <div class="movie-title" v-if="review.movie" @click="goToMovieDetail">
              {{ review.movie.title }}
            </div>
            <div class="rating-date">
              <span class="star">★ {{ review.rating }}</span>
              <span class="date">{{ formatDate(review.created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="review-content">
          {{ review.content }}
        </div>

        <div class="action-bar">
          <button
            class="action-btn"
            :class="{ active: review.is_liked }"
            @click="$emit('toggle-like', review.id)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
            좋아요 {{ review.likes_count }}
          </button>

          <div class="action-item">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path fill-rule="evenodd" d="M4.804 21.644A6.707 6.707 0 006 21.75a6.721 6.721 0 003.583-1.029c.774.182 1.584.279 2.417.279 5.322 0 9.75-3.97 9.75-9 0-5.03-4.428-9-9.75-9s-9.75 3.97-9.75 9c0 2.409 1.025 4.562 2.632 6.19l-2.484 3.032.006.003zM12 12.75a.75.75 0 01-.75-.75V9a.75.75 0 011.5 0v3a.75.75 0 01-.75.75zm0-6a.75.75 0 01.75-.75h.008a.75.75 0 01.75.75v.008a.75.75 0 01-.75.75H12a.75.75 0 01-.75-.75V6.75z" clip-rule="evenodd" />
            </svg>
            댓글 {{ replies.length }}
          </div>
        </div>

        <div class="divider"></div>

        <div class="replies-list">
          <div v-for="reply in replies" :key="reply.id" class="reply-item">
            <div class="r-head">
              <span class="r-user">{{ reply.user.username }}</span>
              <div class="r-right">
                <span class="r-date">{{ formatDate(reply.created_at) }}</span>
                <button
                  v-if="authStore.user?.id === reply.user.id"
                  class="del-reply-btn"
                  @click="onDeleteReply(reply.id)"
                >삭제</button>
              </div>
            </div>
            <div class="r-body">{{ reply.content }}</div>
          </div>
          <div v-if="replies.length === 0" class="no-replies">
            아직 댓글이 없습니다.
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <input
          type="text"
          v-model="replyText"
          class="reply-input"
          placeholder="댓글을 작성해주세요..."
          @keyup.enter="onSubmitReply"
        />
        <button class="submit-btn" :disabled="!replyText.trim()" @click="onSubmitReply">등록</button>
      </div>
    </div>

    <ReviewWriteModal 
      v-if="isEditModalOpen"
      :movieTitle="review.movie?.title || ''"
      :existingReview="review"
      @close="isEditModalOpen = false"
      @submit="handleEditSubmit"
      @delete="handleEditDelete" 
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { deleteReviewComment, deleteReview, updateReview } from '@/api/comet'
import ReviewWriteModal from '@/components/review/ReviewWriteModal.vue'

const props = defineProps({
  review: { type: Object, required: true },
  replies: { type: Array, default: () => [] },
  movie: { type: Object, default: null }
})

// 부모에게 보낼 이벤트 정의 (이게 있어야 새로고침 없이 반영됨)
const emit = defineEmits([
  'close', 
  'submit-reply', 
  'toggle-like', 
  'delete-reply', 
  'delete-review', 
  'update-review'
])

const router = useRouter()
const authStore = useAuthStore()
const replyText = ref('')
const isEditModalOpen = ref(false)

const posterUrl = computed(() => {
  const m = props.review.movie || props.movie
  if (m?.poster_path) return `https://image.tmdb.org/t/p/w200${m.poster_path}`
  return null
})

const isMyReview = computed(() => {
  if (!authStore.isLoggedIn || !props.review.user) return false
  return authStore.user?.id === props.review.user.id
})

/* --- 댓글 관련 --- */
function onSubmitReply() {
  if (replyText.value.trim()) {
    emit('submit-reply', replyText.value)
    replyText.value = ''
  }
}

async function onDeleteReply(commentId) {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  try {
    await deleteReviewComment(commentId)
    emit('delete-reply', commentId)
  } catch (e) {
    alert('댓글 삭제 실패')
  }
}

/* --- ✅ 리뷰 삭제 (정상 작동 중) --- */
async function onDeleteReview() {
  if (!confirm('정말 이 리뷰를 삭제하시겠습니까?')) return
  try {
    await deleteReview(props.review.id)
    emit('delete-review', props.review.id)
    emit('close')
  } catch (e) {
    console.error(e)
    alert('삭제 실패')
  }
}

/* --- ✅ 리뷰 수정 (400 에러 해결을 위한 수정) --- */
function openEditModal() {
  isEditModalOpen.value = true
}

async function handleEditSubmit(payload) {
  try {
    // 🔥 [핵심] 400 에러 해결: movie ID를 반드시 포함해야 합니다!
    // 백엔드가 PUT 요청 시 영화 정보 연결을 확인하려 하기 때문입니다.
    const updateData = {
      content: payload.content,
      rating: payload.rating,
      watched: props.review.watched ?? true, // 혹시 모르니 이것도 포함
      movie: props.review.movie.id // ✅ 영화 ID 추가 (필수)
    }
    
    // API 호출
    const updated = await updateReview(props.review.id, updateData)
    
    // 부모에게 알려서 화면 즉시 갱신
    emit('update-review', updated)
    isEditModalOpen.value = false
    alert('수정되었습니다.')
  } catch (e) {
    console.error('리뷰 수정 에러:', e)
    // 에러 내용을 구체적으로 확인 (디버깅용)
    if (e.response && e.response.data) {
        console.log('서버 에러 메시지:', e.response.data)
    }
    alert('수정에 실패했습니다.')
  }
}

function handleEditDelete() {
  onDeleteReview()
  isEditModalOpen.value = false
}

/* --- 이동/유틸 함수 --- */
function goToMovieDetail() {
  const m = props.review.movie || props.movie
  if (m) {
    router.push(`/movies/${m.tmdb_id || m.id}`)
    emit('close')
  }
}

function goToUserProfile() {
  const username = props.review?.user?.username
  if (!username) return
  router.push(`/users/${username}`)
  emit('close')
}

function formatDate(dateString) {
  if (!dateString) return ''
  const d = new Date(dateString)
  return `${d.getFullYear()}.${d.getMonth()+1}.${d.getDate()}`
}
</script>

<style scoped>
/* 기존 스타일 + 헤더 버튼 스타일 */
.modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.7); z-index: 9999; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
.modal-card { width: 600px; height: 700px; background: var(--card); border-radius: 12px; display: flex; flex-direction: column; overflow: hidden; box-shadow: var(--shadow); border: 1px solid var(--border); }

.modal-header { height: 60px; padding: 0 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-shrink: 0; background: var(--card); }
.user-profile { display: flex; align-items: center; gap: 10px; }
.user-profile.clickable { cursor: pointer; }
.u-img { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 1px solid var(--border); }
.u-icon { font-size: 28px; color: var(--muted); }
.u-name { font-weight: 700; font-size: 15px; color: var(--text); }

.header-right { display: flex; align-items: center; gap: 16px; }
.my-actions { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--muted); }
.action-text { background: none; border: none; cursor: pointer; color: var(--muted); padding: 0; font-size: 13px; transition: color 0.2s; }
.action-text:hover { color: var(--primary); text-decoration: underline; }
.divider-bar { color: var(--border); font-size: 10px; }
.close-btn { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--muted); padding: 0; line-height: 1; }

.modal-body { flex: 1; overflow-y: auto; padding: 20px; background: var(--card); }
.review-meta-row { display: flex; gap: 16px; margin-bottom: 16px; }
.small-poster { width: 60px; height: 90px; border-radius: 4px; overflow: hidden; flex-shrink: 0; cursor: pointer; background: var(--bg); border: 1px solid var(--border); }
.small-poster img { width: 100%; height: 100%; object-fit: cover; }
.meta-info { display: flex; flex-direction: column; justify-content: center; gap: 4px; }
.movie-title { font-weight: 700; font-size: 16px; color: var(--text); cursor: pointer; }
.rating-date { font-size: 13px; color: var(--muted); display: flex; gap: 8px; }
.star { color: #ffad1f; font-weight: 700; }
.review-content { font-size: 15px; line-height: 1.6; color: var(--text); margin-bottom: 20px; white-space: pre-wrap; }

.action-bar { display: flex; gap: 16px; align-items: center; padding-bottom: 16px; }
.action-btn, .action-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--muted); background: none; border: none; padding: 0; cursor: pointer; }
.action-btn:hover { color: var(--text); }
.action-btn.active { color: var(--primary); font-weight: 700; }

.divider { height: 1px; background: var(--border); margin-bottom: 16px; }
.replies-list { display: flex; flex-direction: column; gap: 16px; }
.no-replies { text-align: center; color: var(--muted); padding: 20px 0; font-size: 13px; }
.reply-item { background: var(--bg); padding: 12px; border-radius: 8px; border: 1px solid var(--border); }
.r-head { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 12px; }
.r-user { font-weight: 700; color: var(--text); }
.r-right { display: flex; align-items: center; gap: 8px; }
.r-date { color: var(--muted); }
.del-reply-btn { font-size: 11px; color: var(--muted); border: none; background: none; cursor: pointer; text-decoration: underline; padding: 0; }
.del-reply-btn:hover { color: var(--primary); }
.r-body { font-size: 14px; color: var(--text); line-height: 1.4; }

.modal-footer { height: 70px; padding: 0 20px; border-top: 1px solid var(--border); display: flex; align-items: center; gap: 10px; background: var(--card); flex-shrink: 0; }
.reply-input { flex: 1; padding: 12px 16px; border: 1px solid var(--border); background: var(--input-bg); color: var(--text); border-radius: 99px; outline: none; font-size: 14px; }
.reply-input:focus { background: var(--card); border-color: var(--primary); box-shadow: 0 0 0 2px var(--primary-weak); }
.submit-btn { background: var(--border); color: var(--muted); border: none; padding: 10px 20px; border-radius: 99px; font-weight: 700; cursor: default; }
.submit-btn:not(:disabled) { background: var(--primary); color: white; cursor: pointer; }

@media (max-width: 600px) { .modal-card { width: 95%; height: 80vh; } }
</style>