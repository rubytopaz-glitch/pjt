import { defineStore } from 'pinia'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    themes: ['light', 'blackred', 'blue', 'midnight', 'purple', 'forest', 'sunset'],
    theme: localStorage.getItem('theme') || 'light' // 기본값을 light로 설정 가능
  }),

  actions: {
    applyTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme)
    },

    async setTheme(theme, { syncServer = true } = {}) {
      this.theme = theme
      localStorage.setItem('theme', theme)
      this.applyTheme(theme)

      // ✅ 로그인 상태면 서버에도 저장 (마이페이지/설정 연동)
      if (syncServer) {
        const auth = useAuthStore()
        if (auth.isAuthenticated) {
          try {
            await api.patch('/auth/me/theme/', { theme })
          } catch (e) {
            console.error("서버 테마 저장 실패:", e)
          }
        }
      }
    },

    /**
     * ✅ 테마 토글 로직 수정
     * 현재 테마의 인덱스를 찾아 다음 테마로 순환시킵니다.
     * (sunset 다음은 다시 blackred로 돌아감)
     */
    async toggleTheme() {
      const currentIndex = this.themes.indexOf(this.theme)
      const nextIndex = (currentIndex + 1) % this.themes.length
      const nextTheme = this.themes[nextIndex]
      await this.setTheme(nextTheme)
    },

    // 앱 시작 시 1번 호출 (로컬스토리지 값 적용)
    initTheme() {
      this.applyTheme(this.theme)
    },
  },
})