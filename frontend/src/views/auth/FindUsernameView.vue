<template>
  <div class="auth-backdrop">
    <AuthCardShell title="아이디 찾기">
      <FindUsernameForm />

      <template #footer>
        <router-link class="link" to="/login">로그인으로 돌아가기</router-link>
      </template>
    </AuthCardShell>
  </div>
</template>

<script setup>
import AuthCardShell from '@/components/login/AuthCardShell.vue'
import FindUsernameForm from '@/components/login/FindUsernameForm.vue'
</script>

<style scoped>
.auth-backdrop {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: var(--bg);
  padding: 24px;
  transition: background-color 0.3s;
}
</style>
