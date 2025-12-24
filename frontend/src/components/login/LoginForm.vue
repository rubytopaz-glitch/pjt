<template>
  <form class="form" @submit.prevent="handleSubmit">
    <label class="label">아이디 또는 이메일</label>
    <input
      v-model.trim="identifier"
      class="input"
      type="text"
      name="identifier"
      autocomplete="username"
      placeholder="user1 또는 user1@email.com"
      :disabled="loading"
    />

    <label class="label">비밀번호</label>
    <input
      v-model="password"
      class="input"
      type="password"
      name="password"
      autocomplete="current-password"
      placeholder="••••••••"
      :disabled="loading"
    />

    <button class="btn" type="submit" :disabled="loading || !identifier || !password">
      {{ loading ? '로그인 중...' : '로그인' }}
    </button>

    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const emit = defineEmits(['submit'])

const identifier = ref('')
const password = ref('')

function handleSubmit() {
  // ✅ 백엔드 login이 username/email 둘 다 받게 되어있으니
  // 프론트는 username 키로 보내도 됨(내용이 email이어도 처리됨)
  emit('submit', {
    username: identifier.value,
    password: password.value,
  })
}
</script>

<style>
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
