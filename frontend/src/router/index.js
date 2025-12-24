// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes.js'
import { requiresAuthGuard } from '@/utils/guards'

const router = createRouter({
  history: createWebHistory(),
  routes, 
  scrollBehavior(to, from, savedPosition) {
    // 사용자가 '뒤로가기'를 눌렀을 때는 이전 위치를 유지해주고,
    if (savedPosition) {
      return savedPosition
    } else {
      // 그 외 일반적인 이동(클릭 등)은 무조건 맨 위로 보냅니다.
      return { top: 0, behavior: 'smooth' } // 'smooth'를 넣으면 부드럽게 올라갑니다.
    }
  },
})

router.beforeEach(requiresAuthGuard)

export default router
