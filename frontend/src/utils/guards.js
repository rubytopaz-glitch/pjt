// frontend/src/utils/guards.js
import { useAuthStore } from '@/stores/auth'

let bootstrapped = false

export async function requiresAuthGuard(to) {
  const auth = useAuthStore()

  // ✅ 가드에서 먼저 토큰/유저 복구(1회만)
  if (!bootstrapped) {
    bootstrapped = true
    if (typeof auth.bootstrap === 'function') {
      try {
        await auth.bootstrap()
      } catch (e) {
        console.warn('bootstrap failed:', e)
      }
    }
  }

  const requiresAuth = to.matched.some((r) => r.meta?.requiresAuth)

  // ✅ 인증 필요한데 비로그인이면 로그인으로
  if (requiresAuth && !auth.isLoggedIn) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // ✅ 이미 로그인인데 /login 들어오면 redirect 처리
  if (to.name === 'login' && auth.isLoggedIn) {
    const redirect = to.query?.redirect
    return redirect ? redirect : { name: 'home' }
  }

  return true
}
