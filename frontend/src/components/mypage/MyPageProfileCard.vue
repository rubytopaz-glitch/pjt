<template>
  <section class="profile-card">
    <div class="avatar-area">
      <div class="avatar">
        <img v-if="user?.profile_image" :src="getProfileImageUrl(user.profile_image)" alt="profile" />
        <div v-else class="fallback">👤</div>
      </div>
      <div class="names">
        <h1 class="username">{{ user?.username || '사용자' }}</h1>
        <button class="btn-edit" @click="$emit('edit')">프로필 수정</button>
      </div>
    </div>
    
    <div class="stats">
      <div class="stat-item" @click="$emit('open-follow', 'following')">
        <span>팔로잉</span> <b>{{ user?.following_count || 0 }}</b>
      </div>
      
      <div class="stat-item" @click="$emit('open-follow', 'followers')">
        <span>팔로워</span> <b>{{ user?.followers_count || 0 }}</b>
      </div>
    </div>
  </section>
</template>

<script setup>
/** ✅ 이미지 URL 보정 함수 */
function getProfileImageUrl(path) {
  if (!path) return null
  if (path.startsWith('http')) return path 
  return `http://127.0.0.1:8000${path}` 
}

defineProps({
  user: Object
})

// ✅ [수정] 부모에게 보낼 이벤트 정의에 'open-follow' 추가
defineEmits(['edit', 'open-follow'])
</script>

<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.profile-card { text-align: center; margin-bottom: 30px; }
.avatar-area { margin-bottom: 20px; }

.avatar { 
  width: 100px; height: 100px; 
  background: var(--bg); /* #eee -> var(--bg) 테마 배경색 대응 */
  border-radius: 50%; 
  margin: 0 auto 10px; 
  overflow: hidden; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  border: 1px solid var(--border); 
}

.avatar img { width: 100%; height: 100%; object-fit: cover; }
.fallback { font-size: 40px; color: var(--muted); } /* 아이콘 색상 대응 */
.names { margin-top: 10px; }
.username { font-size: 24px; font-weight: 900; margin-bottom: 10px; color: var(--text); }

.btn-edit { 
  padding: 6px 12px; 
  border: 1px solid var(--border); 
  background: var(--card); 
  border-radius: 4px; 
  cursor: pointer; 
  font-size: 13px; 
  color: var(--text); 
  transition: background 0.2s;
}
.btn-edit:hover {
  background: var(--primary-weak); /* 호버 시 테마별 약한 강조색 */
}

.stats { display: flex; justify-content: center; gap: 20px; color: var(--muted); font-size: 14px; }
.stats b { color: var(--text); font-weight: 900; margin-left: 4px; }

/* ✅ 클릭 가능한 아이템 스타일 테마 대응 */
.stat-item {
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s, color 0.2s;
}

.stat-item:hover {
  opacity: 0.8;
  transform: scale(1.05);
  color: var(--primary); /* #ff2f6e -> var(--primary) 테마 포인트 컬러 대응 */
}
</style>