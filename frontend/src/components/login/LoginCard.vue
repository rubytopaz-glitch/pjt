<template>
  <div class="auth-card">
    <div class="brand">
      <img class="logo" :src="logoSrc" alt="혜성 로고" />
      <h1>혜성</h1>
    </div>

    <LoginForm
      :loading="loading"
      :error="error"
      @submit="$emit('submit', $event)"
    />

    <div class="footer">
      <p>
        아직 계정이 없나요?
        <router-link class="link" to="/signup">회원가입</router-link>
      </p>

      <!-- ✅ 추가: 아이디/비번 찾기 링크 -->
      <p class="helper-links">
        <router-link class="link" to="/find-username">아이디 찾기</router-link>
        <span class="divider">·</span>
        <router-link class="link" to="/reset-password">비밀번호 재설정</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import LoginForm from './LoginForm.vue'

defineProps({
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

defineEmits(['submit'])

const logoSrc = computed(() => new URL('@/assets/comet_logo.png', import.meta.url).href)
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
