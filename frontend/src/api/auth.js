import { defineStore } from 'pinia'
import { login as apiLogin, fetchMe } from '@/api/comet'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
  }),
  getters: {
    isAuthed: (s) => !!s.user,
  },
  actions: {
    async bootstrap() {
      // 새로고침해도 토큰이 localStorage에 있으면 me로 유저 복구
      const access = localStorage.getItem('access')
      if (!access) return
      try {
        this.user = await fetchMe()
      } catch (e) {
        // 토큰이 깨졌거나 만료면 정리
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        this.user = null
      }
    },

    async login(payload) {
      const res = await apiLogin(payload)
      // res = { user, tokens:{access, refresh} }
      const { tokens, user } = res
      if (tokens?.access) localStorage.setItem('access', tokens.access)
      if (tokens?.refresh) localStorage.setItem('refresh', tokens.refresh)

      // ✅ 여기서 user를 바로 세팅하거나, fetchMe를 다시 호출해도 됨
      this.user = user || (await fetchMe())
      return res
    },

    logout() {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      this.user = null
    },
  },
})
