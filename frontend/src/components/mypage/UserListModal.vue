<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-window">
      <div class="header">
        <h3>{{ title }}</h3>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>
      
      <div class="user-list">
        <div v-if="users.length === 0" class="empty">목록이 비어있습니다.</div>
        
        <div v-for="user in users" :key="user.id" class="user-item">
          <div class="user-info" @click="goProfile(user.username)">
            <img v-if="user.profile_image" :src="fullUrl(user.profile_image)" class="avatar" />
            <div v-else class="avatar-fallback">👤</div>
            <span class="username">{{ user.username }}</span>
          </div>
          
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  title: String,
  users: Array
})
const emit = defineEmits(['close'])
const router = useRouter()

function fullUrl(path) {
  if (!path) return ''
  return path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`
}

function goProfile(username) {
  emit('close') // 이동 전 모달 닫기
  router.push(`/users/${username}`)
}
</script>
<style scoped>

.modal-overlay {
  position: fixed; 
  inset: 0; 
  background: rgba(0, 0, 0, 0.7); /* 오버레이는 가독성을 위해 어둡게 유지 */
  display: flex; 
  align-items: center; 
  justify-content: center; 
  z-index: 2000;
  backdrop-filter: blur(4px); /* 배경 흐림 효과 추가 */
}

.modal-window {
  background: var(--card); /* white -> var(--card) */
  width: 400px; 
  height: 500px; 
  border-radius: 12px;
  display: flex; 
  flex-direction: column; 
  overflow: hidden;
  border: 1px solid var(--border); /* 다크 테마 경계선 확보 */
  box-shadow: var(--shadow); /* rgba -> var(--shadow) */
}

.header {
  padding: 15px 20px; 
  border-bottom: 1px solid var(--border); /* #eee -> var(--border) */
  display: flex; 
  justify-content: space-between; 
  align-items: center;
  background: var(--card);
}

.header h3 { 
  margin: 0; 
  font-size: 18px; 
  font-weight: 800; 
  color: var(--text); /* 글자색 대응 */
}

.close-btn { 
  border: none; 
  background: none; 
  font-size: 20px; 
  cursor: pointer; 
  color: var(--muted); /* 고정색 -> var(--muted) */
}

.user-list { 
  flex: 1; 
  overflow-y: auto; 
  padding: 10px; 
  background: var(--card); /* 리스트 배경 대응 */
}

.empty { 
  text-align: center; 
  color: var(--muted); /* #999 -> var(--muted) */
  margin-top: 50px; 
}

.user-item {
  display: flex; 
  align-items: center; 
  justify-content: space-between;
  padding: 10px; 
  border-radius: 8px; 
  transition: all 0.2s;
  cursor: pointer;
}

/* ✅ 호버 시 테마별 포인트 컬러 적용 */
.user-item:hover { 
  background: var(--primary-weak); /* #f9f9f9 -> 테마별 강조색 */
}

.user-info { display: flex; align-items: center; gap: 12px; }

.avatar { 
  width: 40px; 
  height: 40px; 
  border-radius: 50%; 
  object-fit: cover; 
  border: 1px solid var(--border); /* #eee -> var(--border) */
}

.avatar-fallback { 
  width: 40px; 
  height: 40px; 
  border-radius: 50%; 
  background: var(--bg); /* #eee -> var(--bg) */
  color: var(--muted);
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-size: 20px; 
  border: 1px solid var(--border);
}

.username { 
  font-weight: 700; 
  font-size: 15px; 
  color: var(--text); /* 글자색 대응 */
}
</style>