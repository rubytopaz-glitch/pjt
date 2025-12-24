<template>
  <header :class="['nav-container', { transparent: isDetailPage }]">
    <div class="nav-inner">
      <div class="left">
        <RouterLink to="/" class="brand" @click="closeMobileIfOpen">
          <img :src="logoUrl" class="logo" alt="혜성 로고" />
          <span class="brand-text">혜성</span>
        </RouterLink>

        <!-- ✅ 데스크탑 메뉴 -->
        <nav v-if="!isMobile" class="menu">
          <RouterLink to="/" class="link">홈</RouterLink>
          <RouterLink :to="{ name: 'movies' }" class="link">영화</RouterLink>
          <RouterLink to="/taste" class="link">취향분석</RouterLink>
          <RouterLink to="/recommend" class="link">추천</RouterLink>
          <RouterLink to="/guide" class="link">도움말</RouterLink>
        </nav>
      </div>

      <div class="right">
        <!-- ✅ 데스크탑 검색 -->
        <input
          v-if="!isMobile"
          class="search"
          type="text"
          placeholder="검색"
          v-model="q"
          @keyup.enter="goSearch"
        />

        <!-- ✅ 모바일 햄버거 버튼 -->
        <button
          v-if="isMobile"
          class="icon-btn"
          type="button"
          @click="toggleMobileMenu"
          aria-label="메뉴 열기"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            class="hamburger-icon"
          >
            <path
              fill-rule="evenodd"
              d="M3.75 6.75A.75.75 0 0 1 4.5 6h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Zm0 5.25a.75.75 0 0 1 .75-.75h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Zm0 5.25A.75.75 0 0 1 4.5 16.5h15a.75.75 0 0 1 0 1.5h-15a.75.75 0 0 1-.75-.75Z"
              clip-rule="evenodd"
            />
          </svg>
        </button>

        <!-- ✅ 데스크탑 유저 메뉴 -->
        <div v-if="!isMobile && isLoggedIn" class="user-menu-wrapper">
          <div class="user-icon-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="user-icon">
              <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM3.751 20.105a8.25 8.25 0 0 1 16.498 0 .75.75 0 0 1-.437.695A18.683 18.683 0 0 1 12 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 0 1-.437-.695Z" clip-rule="evenodd" />
            </svg>
          </div>

          <div class="dropdown-menu">
            <RouterLink :to="{ name: 'mypage' }" class="dropdown-item">마이페이지</RouterLink>
            <div class="dropdown-item" @click="onLogout">로그아웃</div>

            <div class="dropdown-item theme-item">
              <span>테마변경</span>
              <span class="arrow"> > </span>

              <div class="sub-dropdown">
                <div class="dropdown-item" @click="changeTheme('light')">기본 (White)</div>
                <div class="dropdown-item" @click="changeTheme('blackred')">Black Red</div>
                <div class="dropdown-item" @click="changeTheme('blue')">Blue</div>
                <div class="dropdown-item" @click="changeTheme('midnight')">Midnight Gold</div>
                <div class="dropdown-item" @click="changeTheme('purple')">Cyber Purple</div>
                <div class="dropdown-item" @click="changeTheme('forest')">Forest Green</div>
                <div class="dropdown-item" @click="changeTheme('sunset')">Sunset Orange</div>
              </div>
            </div>
          </div>
        </div>

        <!-- ✅ 데스크탑 로그인 -->
        <template v-if="!isMobile && !isLoggedIn">
          <RouterLink to="/login" class="btn ghost">로그인</RouterLink>
        </template>
      </div>
    </div>

    <!-- ✅ 모바일 드로어(햄버거 메뉴) -->
    <Teleport to="body">
      <div v-show="mobileOpen" class="drawer-overlay" @click="closeMobile" />

      <aside v-show="mobileOpen" class="mobile-drawer" @click.stop>
        <div class="drawer-header">
          <div class="drawer-title">메뉴</div>
          <button class="icon-btn" type="button" @click="closeMobile" aria-label="메뉴 닫기">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="close-icon">
              <path d="M6.225 4.811a.75.75 0 0 1 1.06 0L12 9.525l4.715-4.714a.75.75 0 1 1 1.06 1.06L13.06 10.586l4.715 4.714a.75.75 0 1 1-1.06 1.06L12 11.646l-4.715 4.714a.75.75 0 1 1-1.06-1.06l4.715-4.714-4.715-4.714a.75.75 0 0 1 0-1.06Z"/>
            </svg>
          </button>
        </div>

        <div class="drawer-section">
          <input
            class="drawer-search"
            type="text"
            placeholder="검색"
            v-model="q"
            @keyup.enter="goSearchAndClose"
          />
        </div>

        <nav class="drawer-nav">
          <RouterLink to="/" class="drawer-link" @click="closeMobile">홈</RouterLink>
          <RouterLink :to="{ name: 'movies' }" class="drawer-link" @click="closeMobile">영화</RouterLink>
          <RouterLink to="/taste" class="drawer-link" @click="closeMobile">취향분석</RouterLink>
          <RouterLink to="/recommend" class="drawer-link" @click="closeMobile">추천</RouterLink>
          <RouterLink to="/guide" class="drawer-link" @click="closeMobile">도움말</RouterLink>
        </nav>

        <div class="drawer-divider" />

        <div v-if="isLoggedIn" class="drawer-nav">
          <RouterLink :to="{ name: 'mypage' }" class="drawer-link" @click="closeMobile">마이페이지</RouterLink>
          <button class="drawer-btn" type="button" @click="onLogoutAndClose">로그아웃</button>

          <button class="drawer-btn" type="button" @click="themeOpen = !themeOpen">
            테마변경 <span class="drawer-arrow">{{ themeOpen ? '▾' : '▸' }}</span>
          </button>

          <div v-show="themeOpen" class="drawer-sub">
            <button class="drawer-sub-btn" @click="changeThemeAndClose('light')">기본 (White)</button>
            <button class="drawer-sub-btn" @click="changeThemeAndClose('blackred')">Black Red</button>
            <button class="drawer-sub-btn" @click="changeThemeAndClose('blue')">Blue</button>
            <button class="drawer-sub-btn" @click="changeThemeAndClose('midnight')">Midnight Gold</button>
            <button class="drawer-sub-btn" @click="changeThemeAndClose('purple')">Cyber Purple</button>
            <button class="drawer-sub-btn" @click="changeThemeAndClose('forest')">Forest Green</button>
            <button class="drawer-sub-btn" @click="changeThemeAndClose('sunset')">Sunset Orange</button>
          </div>
        </div>

        <div v-else class="drawer-nav">
          <RouterLink to="/login" class="drawer-link" @click="closeMobile">로그인</RouterLink>
        </div>
      </aside>
    </Teleport>
  </header>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import logoUrl from '@/assets/comet_logo.png'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const themeStore = useThemeStore()

const q = ref('')

const isDetailPage = computed(() => route.name === 'movie-detail')
const isLoggedIn = computed(() => auth.isLoggedIn || auth.isAuthenticated)

/** ✅ 반응형 기준(원하면 숫자만 바꾸면 됨) */
const MOBILE_BP = 860
const isMobile = ref(false)
const mobileOpen = ref(false)
const themeOpen = ref(false)

function updateIsMobile() {
  isMobile.value = window.innerWidth <= MOBILE_BP
}

onMounted(() => {
  updateIsMobile()
  window.addEventListener('resize', updateIsMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateIsMobile)
})

watch(
  () => route.fullPath,
  () => {
    mobileOpen.value = false
    themeOpen.value = false
  }
)

watch(isMobile, (v) => {
  if (!v) {
    mobileOpen.value = false
    themeOpen.value = false
  }
})

function toggleMobileMenu() {
  mobileOpen.value = !mobileOpen.value
}

function closeMobile() {
  mobileOpen.value = false
  themeOpen.value = false
}

function closeMobileIfOpen() {
  if (mobileOpen.value) closeMobile()
}

function goSearch() {
  const keyword = q.value.trim()
  if (!keyword) return
  router.push({ name: 'search', query: { q: keyword } })
  q.value = ''
}

function goSearchAndClose() {
  goSearch()
  closeMobile()
}

function onLogout() {
  auth.logout()
  router.push('/')
}

function onLogoutAndClose() {
  onLogout()
  closeMobile()
}

function changeTheme(themeName) {
  themeStore.setTheme(themeName)
}

function changeThemeAndClose(themeName) {
  changeTheme(themeName)
  closeMobile()
}
</script>

<style scoped>
/* 네비게이션 컨테이너 - 전체 폰트 고정 */
.nav-container {
  position: fixed;
  top: 0; left: 0; right: 0;
  width: 100%; height: 60px;
  background: var(--nav-bg);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--nav-border);
  z-index: 9999;
  transition: all 0.3s ease;

  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.nav-inner {
  max-width: 1100px;
  margin: 0 auto;
  height: 100%;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand { display: flex; align-items: center; gap: 8px; text-decoration: none; }
.logo { width: 28px; height: 28px; object-fit: contain; }

.brand-text {
  font-family: inherit;
  font-weight: 800;
  font-size: 18px;
  letter-spacing: -0.03em;
  color: var(--nav-text);
}

.left { display: flex; align-items: center; gap: 20px; }
.menu { display: flex; gap: 16px; }
.right { display: flex; align-items: center; gap: 10px; }

/* 메뉴 링크 */
.link {
  font-family: inherit;
  color: var(--nav-text);
  transition: color 0.3s;
  text-decoration: none;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: -0.01em;
}
.link:hover, .link.router-link-active {
  color: var(--primary);
  font-weight: 800;
}

/* 검색창 */
.search {
  width: 200px; padding: 7px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--input-bg);
  color: var(--text);
  outline: none;
  transition: all 0.2s;
  font-size: 13px;
  font-family: inherit;
}

/* 유저 아이콘 */
.user-menu-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  height: 60px;
  cursor: pointer;
}
.user-icon {
  width: 28px; height: 28px;
  color: var(--nav-text);
  transition: color 0.3s;
}
.user-menu-wrapper:hover .dropdown-menu { display: block; }

/* 드롭다운 */
.dropdown-menu, .sub-dropdown {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: var(--shadow);
  z-index: 10000;
}
.dropdown-menu {
  display: none;
  position: absolute;
  top: 55px;
  right: 0;
  width: 160px;
  overflow: visible;
}
.dropdown-item {
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  text-decoration: none;
  transition: background 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-family: inherit;
}
.dropdown-item:hover {
  background: var(--primary-weak);
  color: var(--primary);
}
.theme-item { position: relative; }
.theme-item:hover .sub-dropdown { display: block; }
.sub-dropdown {
  display: none;
  position: absolute;
  top: 0;
  left: -160px;
  width: 160px;
}
.arrow { font-size: 10px; color: var(--muted); }

/* 투명 모드 */
.nav-container.transparent {
  background: transparent !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 버튼 */
.btn {
  padding: 7px 12px; border-radius: 6px;
  text-decoration: none; cursor: pointer; font-size: 13px; font-weight: 700;
  border: 1px solid var(--primary); background: var(--primary); color: #fff;
  font-family: inherit;
}
.btn.ghost {
  background: transparent; border: 1px solid transparent; color: var(--nav-text);
}

/* ✅ 모바일 햄버거/닫기 버튼 */
.icon-btn {
  background: transparent;
  border: none;
  padding: 6px;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--nav-text);
}
.icon-btn:hover { background: var(--primary-weak); }
.hamburger-icon { width: 26px; height: 26px; }
.close-icon { width: 22px; height: 22px; }

/* ✅ 모바일 드로어 */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  z-index: 20000;
}

.mobile-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: min(82vw, 320px);
  height: 100vh;
  background: var(--card);
  border-left: 1px solid var(--border);
  box-shadow: var(--shadow);
  z-index: 20001;
  padding-top: 12px;
  display: flex;
  flex-direction: column;
}

.drawer-header {
  height: 48px;
  padding: 0 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.drawer-title {
  font-weight: 800;
  color: var(--text);
}

.drawer-section {
  padding: 10px 14px 0 14px;
}

.drawer-search {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--input-bg);
  color: var(--text);
  outline: none;
  font-size: 14px;
  font-family: inherit;
}

.drawer-nav {
  display: flex;
  flex-direction: column;
  padding: 10px 6px;
}

.drawer-link {
  padding: 12px 12px;
  border-radius: 10px;
  text-decoration: none;
  color: var(--text);
  font-weight: 700;
}
.drawer-link:hover { background: var(--primary-weak); color: var(--primary); }

.drawer-btn {
  width: 100%;
  text-align: left;
  padding: 12px 12px;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: var(--text);
  font-weight: 800;
  cursor: pointer;
  font-family: inherit;
}
.drawer-btn:hover { background: var(--primary-weak); color: var(--primary); }

.drawer-divider {
  height: 1px;
  background: var(--border);
  margin: 6px 14px;
}

.drawer-sub {
  padding: 6px 14px 14px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.drawer-sub-btn {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  cursor: pointer;
  font-weight: 700;
  font-family: inherit;
}
.drawer-sub-btn:hover { background: var(--primary-weak); color: var(--primary); }

.drawer-arrow { float: right; opacity: 0.8; }

/* ✅ 아주 작은 화면에서 로고 텍스트 숨김(선택) */
@media (max-width: 420px) {
  .brand-text { display: none; }
  .nav-inner { padding: 0 12px; }
  .left { gap: 12px; }
  .right { gap: 6px; }
}
</style>
