// frontend/src/router/routes.js

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  { path: '/movies', name: 'movies', component: () => import('@/views/MoviesView.vue') },
  {
    path: '/movies/:tmdbId',
    name: 'movie-detail',
    component: () => import('@/views/MovieDetailView.vue'),
    props: true,
  },
  { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
  { path: '/find-username',  name: 'find-username', component: () => import('@/views/auth/FindUsernameView.vue')},
  { path: '/reset-password', name: 'reset-password', component: () => import('@/views/auth/ResetPasswordView.vue')},
  { path: '/signup', name: 'signup', component: () => import('@/views/SignupView.vue') },
  {
    path: '/taste',
    name: 'taste',
    component: () => import('@/views/TasteView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/recommend',
    name: 'recommend',
    component: () => import('@/views/RecommendView.vue'),
    meta: { requiresAuth: true },
  },
  { path: '/search', name: 'search', component: () => import('@/views/SearchView.vue') },

  // 마이페이지 관련
  {
    path: '/mypage',
    name: 'mypage',
    component: () => import('@/views/MyPageView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/mypage/grid/:type',
    name: 'mypage-grid',
    component: () => import('@/components/mypage/MyPageGridView.vue'),
    props: true
  },
  { path: '/me', redirect: { name: 'mypage' } }, // 기존 호환성 유지

  // 도움말 가이드
  {
    path: '/guide',
    name: 'guide',
    component: () => import('@/views/GuideView.vue'),
  },

  // 유저 및 인물 정보
  {
    path: '/users/:username',
    name: 'user-profile',
    component: () => import('@/views/UserProfileView.vue'),
    props: true,
  },
  { 
    path: '/people/:tmdbId', 
    name: 'person-detail', 
    component: () => import('@/views/PersonDetailView.vue'), 
    props: true 
  },

  // 404 페이지 (항상 맨 아래에 위치)
  { path: '/:pathMatch(.*)*', name: 'notfound', component: () => import('@/views/NotFoundView.vue') },
]

export default routes