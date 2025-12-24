<template>
  <form class="form" @submit.prevent="handleSubmit">
    <label class="label">새 비밀번호</label>
    <input
      v-model="pw1"
      class="input"
      type="password"
      autocomplete="new-password"
      placeholder="8자 이상"
      :disabled="loading"
    />

    <label class="label">새 비밀번호 확인</label>
    <input
      v-model="pw2"
      class="input"
      type="password"
      autocomplete="new-password"
      placeholder="한 번 더 입력"
      :disabled="loading"
    />

    <button class="btn" type="submit" :disabled="loading || !pw1 || !pw2">
      {{ loading ? '변경 중...' : '비밀번호 변경하기' }}
    </button>

    <p v-if="success" class="success">{{ success }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { passwordResetConfirmApi } from '@/api/comet'

const props = defineProps({
  uid: { type: String, required: true },
  token: { type: String, required: true },
})

const emit = defineEmits(['done'])

const loading = ref(false)
const error = ref('')
const success = ref('')

const pw1 = ref('')
const pw2 = ref('')

async function handleSubmit() {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    await passwordResetConfirmApi({
      uid: props.uid,
      token: props.token,
      new_password: pw1.value,
      new_password2: pw2.value,
    })
    success.value = '비밀번호가 변경되었습니다. 잠시 후 로그인 화면으로 이동합니다.'
    emit('done')
  } catch (e) {
    error.value =
      e?.response?.data?.detail ||
      e?.response?.data?.message ||
      '변경에 실패했습니다.'
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
