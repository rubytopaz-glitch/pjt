<template>
  <div class="app-wrapper">
    <TheNavbar />

    <div class="main-content">
      <RouterView />
    </div>

    <TheFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue' // 추가
import { RouterView } from 'vue-router'
import TheNavbar from '@/components/layout/TheNavbar.vue'
import TheFooter from '@/components/layout/TheFooter.vue'
import { useThemeStore } from '@/stores/theme' // 추가

const themeStore = useThemeStore()

// 앱이 실행될 때 테마 초기화
onMounted(() => {
  themeStore.initTheme()
})
</script>

<style>
/* 전역 스타일 리셋 */
* { box-sizing: border-box; }
body { 
  margin: 0; 
  padding: 0; 
  font-family: 'Pretendard', sans-serif;
  /* 테마 변경 시 배경색이 부드럽게 변하도록 추가 */
  transition: background-color 0.3s, color 0.3s; 
}

.main-content {
  padding-top: 60px; 
  min-height: calc(100vh - 60px); 
}
</style>