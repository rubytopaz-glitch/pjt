<template>
  <div class="auth-backdrop">
    <AuthCardShell :title="modeTitle">
      <PasswordResetConfirmForm
        v-if="isConfirmMode"
        :uid="uid"
        :token="token"
        @done="goLoginSoon"
      />
      <PasswordResetRequestForm v-else />

      <template #footer>
        <router-link class="link" to="/login">로그인으로 돌아가기</router-link>
      </template>
    </AuthCardShell>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AuthCardShell from '@/components/login/AuthCardShell.vue'
import PasswordResetRequestForm from '@/components/login/PasswordResetRequestForm.vue'
import PasswordResetConfirmForm from '@/components/login/PasswordResetConfirmForm.vue'

const route = useRoute()
const router = useRouter()

const uid = computed(() => String(route.query.uid || ''))
const token = computed(() => String(route.query.token || ''))

const isConfirmMode = computed(() => !!uid.value && !!token.value)

const modeTitle = computed(() => (isConfirmMode.value ? '새 비밀번호 설정' : '비밀번호 재설정 링크 받기'))

function goLoginSoon() {
  setTimeout(() => router.push('/login'), 1200)
}
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
