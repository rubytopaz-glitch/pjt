import { defineStore } from 'pinia'
import { login as apiLogin, signup as apiSignup, fetchMe } from '@/api/comet'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: false,
  }),

  getters: {
    isLoggedIn: (state) => !!state.user,
  },

  actions: {
    async bootstrap() {
      // ✅ 로컬스토리지에 access 없으면 그냥 종료
      const access = localStorage.getItem('access')
      if (!access) {
        this.user = null
        return
      }

      // ✅ 토큰이 있으면 내 정보 조회로 로그인 상태 복구
      try {
        const me = await fetchMe()
        this.user = me
      } catch (e) {
        // 토큰이 깨졌거나 만료되면 정리
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        this.user = null
      }
    },
    async signup(payload) {
      // payload: { username, password, password2, name, email, birth_date, gender }
      this.loading = true
      try {
        const res = await apiSignup(payload)
        // signup은 "가입만" 해주고 로그인은 별도일 수도 있어서
        // 여기서는 res만 반환 (원하면 자동 로그인으로 바꿀 수 있음)
        return res
      } finally {
        this.loading = false
      }
    },

    async login(payload) {
      // payload: { username, password }
      this.loading = true
      try {
        const res = await apiLogin(payload)

        // ✅ 백엔드 응답 형식: { user: {...}, tokens: {access, refresh} }
        const { user, tokens } = res

        if (tokens?.access) localStorage.setItem('access', tokens.access)
        if (tokens?.refresh) localStorage.setItem('refresh', tokens.refresh)

        this.user = user
        return res
      } finally {
        this.loading = false
      }
    },

    async loadMe() {
      // ✅ 새로고침/앱 최초 진입 시 로그인 상태 복구
      const access = localStorage.getItem('access')
      if (!access) {
        this.user = null
        return null
      }

      try {
        const me = await fetchMe()
        this.user = me
        return me
      } catch (e) {
        // 토큰이 깨졌거나 만료된 경우
        this.logout()
        return null
      }
    },

    logout() {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      this.user = null
    },
  },
})
