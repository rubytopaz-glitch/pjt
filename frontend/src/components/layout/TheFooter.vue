<template>
  <footer class="footer">
    <div class="inner">
      <div class="left">
        <div class="brand">혜성 (The Comet)</div>
        <p class="desc">
          영화 정보 · 리뷰 · 취향분석/추천 
        </p>
        
        <div class="legal-links">
          <button class="legal-btn bold" @click="isPrivacyOpen = true">개인정보처리방침</button>
          <span class="dot">·</span>
          <button class="legal-btn" @click="isTermsOpen = true">이용약관</button>
        </div>
      </div>

      <div class="right">
        <a class="link" href="#" @click.prevent="scrollTop">맨 위로</a>
        <span class="dot">·</span>
        <span class="copy">© {{ year }} The Comet. All rights reserved.</span>
      </div>
    </div>

    <BaseModal 
      :open="isPrivacyOpen" 
      title="개인정보처리방침" 
      @close="isPrivacyOpen = false"
    >
      <PrivacyPolicyContent />
    </BaseModal>

    <BaseModal 
      :open="isTermsOpen" 
      title="서비스 이용약관" 
      @close="isTermsOpen = false"
    >
      <TermsOfServiceContent />
    </BaseModal>
  </footer>
</template>

<script setup>
import { ref } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import PrivacyPolicyContent from '@/components/legal/PrivacyPolicyContent.vue'
import TermsOfServiceContent from '@/components/legal/TermsOfServiceContent.vue'

const year = new Date().getFullYear()

// 각 모달의 열림 상태 관리
const isPrivacyOpen = ref(false)
const isTermsOpen = ref(false)

// 최상단으로 스크롤
function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.footer {
  margin-top: 80px; /* 본문과 푸터 사이 여백 */
  border-top: 1px solid var(--border);
  background: var(--card);
  transition: background-color 0.3s, color 0.3s;
}

.inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 14px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.brand {
  font-weight: 1000;
  font-size: 18px;
  letter-spacing: -0.2px;
  color: var(--text);
}

.desc {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.6;
  max-width: 400px;
}

/* 법적 링크 스타일 */
.legal-links {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.legal-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 12px;
  color: var(--muted);
  cursor: pointer;
  font-family: inherit;
  transition: color 0.2s;
}

.legal-btn.bold {
  font-weight: 800;
  color: var(--text);
}

.legal-btn:hover {
  text-decoration: underline;
  color: var(--primary);
}

.right {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--muted);
  font-size: 13px;
  white-space: nowrap;
  margin-top: 5px;
}

.link {
  color: inherit;
  text-decoration: none;
  font-weight: 900;
  transition: color 0.2s;
}

.link:hover {
  text-decoration: underline;
  color: var(--primary);
}

.dot {
  opacity: 0.5;
  font-size: 12px;
}

.copy {
  font-weight: 500;
}

/* 모바일 대응 */
@media (max-width: 720px) {
  .inner {
    flex-direction: column;
    align-items: flex-start;
    padding: 30px 14px;
    gap: 30px;
  }
  
  .right {
    width: 100%;
    justify-content: flex-start;
    border-top: 1px solid var(--border);
    padding-top: 20px;
    white-space: normal;
  }
}
</style>