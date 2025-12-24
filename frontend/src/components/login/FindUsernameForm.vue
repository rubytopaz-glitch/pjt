<template>
  <form class="form" @submit.prevent="handleSubmit">
    <label class="label">가입 이메일</label>
    <input
      v-model.trim="email"
      class="input"
      type="email"
      autocomplete="email"
      placeholder="user@email.com"
      :disabled="loading"
    />

    <label class="label">생년월일 (선택)</label>
    <input
      v-model="birthDate"
      class="input"
      type="date"
      :disabled="loading"
    />

    <button class="btn" type="submit" :disabled="loading || !email">
      {{ loading ? '처리 중...' : '아이디 안내 메일 받기' }}
    </button>

    <p v-if="success" class="success">{{ success }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { findUsernameApi } from '@/api/comet'

const loading = ref(false)
const error = ref('')
const success = ref('')

const email = ref('')
const birthDate = ref('') // yyyy-mm-dd

async function handleSubmit() {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    const payload = { email: email.value }
    if (birthDate.value) payload.birth_date = birthDate.value

    await findUsernameApi(payload)
    success.value = '입력하신 정보와 일치하는 계정이 있으면 이메일로 아이디를 안내했어요.'
  } catch (e) {
    error.value =
      e?.response?.data?.detail ||
      e?.response?.data?.message ||
      '요청에 실패했습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.success {
  margin: 8px 0 0;
  color: #22c55e;
  font-size: 13px;
  font-weight: 800;
}
.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 22px;
  box-shadow: var(--shadow);
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
  color: var(--text);
  font-weight: 900;
}

.form {
  display: grid;
  gap: 10px;
}

.label {
  font-size: 12px;
  color: var(--muted);
  font-weight: 700;
}

.input {
  border: 1px solid var(--border);
  background: var(--input-bg);
  color: var(--text);
  border-radius: 10px;
  padding: 12px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-weak);
}

.btn {
  margin-top: 6px;
  padding: 12px;
  border-radius: 10px;
  border: 0;
  background: var(--primary);
  color: #fff;
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
  color: #ff4d4f;
  font-size: 13px;
  font-weight: 700;
}

.footer {
  margin-top: 16px;
  font-size: 13px;
  color: var(--muted);
  text-align: center;
}

.link {
  color: var(--primary);
  font-weight: 800;
  cursor: pointer;
  margin-left: 6px;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.helper-links {
  margin-top: 8px;
}

.divider {
  margin: 0 8px;
  opacity: 0.6;
}

</style>
