<template>
  <div class="page">
    <div class="backdrop"></div>

    <div class="card">
      <h1 class="title">혜성</h1>
      <p class="muted">회원가입</p>

      <form class="form" @submit.prevent="onSubmit">
        <label class="label">이름</label>
        <input class="input" v-model.trim="form.name" placeholder="이름" />

        <label class="label">이메일</label>
        <input class="input" v-model.trim="form.email" placeholder="email@example.com" />

        <label class="label">생년월일</label>
        <input class="input" type="date" v-model="form.birth_date" />

        <label class="label">성별</label>
        <select class="input" v-model="form.gender">
          <option disabled value="">선택</option>
          <option value="M">남</option>
          <option value="F">여</option>
        </select>

        <label class="label">아이디(username)</label>
        <input class="input" v-model.trim="form.username" placeholder="username" />

        <label class="label">비밀번호</label>
        <input class="input" type="password" v-model="form.password" placeholder="********" />

        <label class="label">비밀번호 확인</label>
        <input class="input" type="password" v-model="form.password2" placeholder="********" />

        <p v-if="error" class="error">{{ error }}</p>

        <button class="btn primary" type="submit">회원가입</button>
        <button class="btn" type="button" @click="$router.push('/login')">이미 계정이 있어요</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signup as signupApi } from '@/api/comet'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const error = ref('')

const form = reactive({
  name: '',
  email: '',
  birth_date: '',
  gender: '',
  username: '',
  password: '',
  password2: '',
})

function validate() {
  if (!form.name || !form.email || !form.birth_date || !form.gender || !form.username) {
    return '필수 항목을 모두 입력해줘.'
  }
  if (form.password.length < 8) return '비밀번호는 8자 이상이어야 해.'
  if (form.password !== form.password2) return '비밀번호 확인이 일치하지 않아.'
  return ''
}

async function onSubmit() {
  error.value = ''
  const msg = validate()
  if (msg) {
    error.value = msg
    return
  }

  try {
    const data = await signupApi({ ...form })

    // ✅ 백엔드에서 tokens를 같이 주는 방식(추천)이라면 자동 로그인
    if (data.tokens?.access) {
      auth.setTokens(data.tokens)
      auth.user = data.user
      router.push('/')
      return
    }

    // 토큰을 안 주는 방식이면 회원가입 후 로그인으로
    router.push('/login')
  } catch (e) {
    // DRF ValidationError는 보통 객체 형태로 옴
    const d = e?.response?.data
    if (typeof d === 'string') error.value = d
    else if (d?.detail) error.value = d.detail
    else error.value = '회원가입 실패 (입력값을 확인해줘)'
  }
}
</script>

<style scoped>
.page{
  min-height: 100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  padding: 20px;
  position: relative;
}
.backdrop{
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,.6);
}
.card{
  position: relative;
  width: 460px;
  max-width: 100%;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--card);
  box-shadow: var(--shadow);
  padding: 16px;
}
.title{ margin: 0; font-weight: 1000; font-size: 28px; }
.muted{ margin: 6px 0 14px; color: var(--muted); }
.form{ display:flex; flex-direction:column; gap: 8px; }
.label{ font-weight: 900; font-size: 13px; margin-top: 6px; }
.input{
  border: 1px solid var(--border);
  background: var(--input-bg);
  border-radius: 12px;
  padding: 10px 12px;
}
.btn{
  margin-top: 10px;
  border: 1px solid var(--border);
  background: var(--card);
  border-radius: 12px;
  padding: 10px 12px;
  cursor:pointer;
  font-weight: 1000;
}
.btn:hover{ background: var(--primary-weak); }
.btn.primary{
  border-color: transparent;
  background: var(--primary);
  color: #fff;
}
.error{ color: #ef4444; font-weight: 900; margin: 6px 0 0; }
</style>
