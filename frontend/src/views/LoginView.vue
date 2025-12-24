<template>
  <div class="auth-backdrop">
    <div class="auth-card">
      <!-- 타이틀 -->
      <div class="brand">
        <img class="logo" :src="logoSrc" alt="혜성 로고" />
        <h1>혜성</h1>
      </div>

      <!-- 로그인 폼 -->
      <form class="form" @submit.prevent="onSubmit">
        <label class="label">아이디 또는 이메일</label>
        <input
          v-model.trim="form.username"
          class="input"
          type="text"
          name="username"
          autocomplete="username"
          placeholder="user1 또는 user1@email.com"
        />

        <label class="label">비밀번호</label>
        <input
          v-model="form.password"
          class="input"
          type="password"
          name="password"
          autocomplete="current-password"
          placeholder="••••••••"
        />

        <button class="btn" type="submit" :disabled="loading">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>

      <div class="footer">
        <p>
          아직 계정이 없나요?
          <a class="link" @click.prevent="goSignup">회원가입</a>
        </p>
        <p class="helper">
          <a class="link" @click.prevent="goFindUsername">아이디 찾기</a>
          <span class="divider">·</span>
          <a class="link" @click.prevent="goResetPassword">비밀번호 재설정</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  username: '',
  password: '',
})

const loading = ref(false)
const error = ref('')

const logoSrc = computed(() => new URL('@/assets/comet_logo.png', import.meta.url).href)

async function onSubmit() {
  error.value = ''
  loading.value = true

  try {
    // ✅ 여기 payload는 “반드시” 이런 형태여야 함
    const payload = {
      username: form.username,
      password: form.password,
    }

    // 디버그용(원하면 지워도 됨)
    console.log('LOGIN payload =>', payload)

    await auth.login(payload) // store에서 API 호출
    router.push('/') // 홈으로
  } catch (e) {
    const msg =
      e?.response?.data?.detail ||
      e?.response?.data?.message ||
      '로그인에 실패했습니다.'
    error.value = msg
  } finally {
    loading.value = false
  }
}

function goSignup() {
  router.push('/signup')
}

function goFindUsername() {
  router.push('/find-username')
}

function goResetPassword() {
  router.push('/reset-password')
}


</script>

<style scoped>
/* 🎨 레이아웃 구조는 유지하고 색상만 테마 변수로 교체 */

.auth-backdrop {
  min-height: 100vh;
  display: grid;
  place-items: center;
  /* 백그라운드를 테마 배경색으로 대응하거나, 기존의 반투명 느낌을 유지 */
  background: var(--bg); 
  padding: 24px;
  transition: background-color 0.3s;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--card); /* #fff -> var(--card) */
  border: 1px solid var(--border); /* 테두리 추가로 다크모드 가시성 확보 */
  border-radius: 16px;
  padding: 22px;
  box-shadow: var(--shadow); /* 고정값 -> var(--shadow) */
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}

.logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.brand h1 {
  margin: 0;
  font-size: 20px;
  color: var(--text); /* 글자색 대응 */
  font-weight: 900;
}

.form {
  display: grid;
  gap: 10px;
}

.label {
  font-size: 12px;
  color: var(--muted); /* #555 -> var(--muted) */
  font-weight: 700;
}

.input {
  border: 1px solid var(--border); /* #ddd -> var(--border) */
  background: var(--input-bg);    /* 배경색 대응 */
  color: var(--text);             /* 입력 글자색 대응 */
  border-radius: 10px;
  padding: 12px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
  border-color: var(--primary); /* #aaa -> var(--primary) 포인트 컬러 */
  box-shadow: 0 0 0 3px var(--primary-weak);
}

.btn {
  margin-top: 6px;
  padding: 12px;
  border-radius: 10px;
  border: 0;
  background: var(--primary); /* #111 -> var(--primary) */
  color: #fff; /* 버튼 글자는 항상 흰색 유지 (가독성) */
  cursor: pointer;
  font-weight: 800;
  transition: opacity 0.2s;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
  filter: brightness(1.1);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.error {
  margin: 8px 0 0;
  color: #ff4d4f; /* 에러는 강렬한 레드 유지 혹은 var(--primary) 활용 */
  font-size: 13px;
  font-weight: 700;
}

.social {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 14px;
}

.social-btn {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid var(--border); /* #ddd -> var(--border) */
  background: var(--bg);           /* #fafafa -> var(--bg) */
  color: var(--text);              /* 글자색 대응 */
  cursor: pointer;
  font-weight: 700;
  transition: background 0.2s;
}

.social-btn:hover {
  background: var(--primary-weak);
}

.footer {
  margin-top: 16px;
  font-size: 13px;
  color: var(--muted); /* #666 -> var(--muted) */
  text-align: center;
}

.link {
  color: var(--primary); /* #111 -> var(--primary) 포인트 컬러 */
  font-weight: 800;
  cursor: pointer;
  margin-left: 6px;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.helper {
  margin-top: 8px;
}

.divider {
  margin: 0 8px;
  opacity: 0.6;
}

</style>
