<template>
  <div class="guide-page">
    <div class="comet-loader-layer">
      <div class="comet-container">
        <div class="comet"></div>
        <div class="star-particle p1"></div>
        <div class="star-particle p2"></div>
        <div class="star-particle p3"></div>
        <div class="star-particle p4"></div>
        <div class="star-particle p5"></div>
      </div>
    </div>

    <div class="guide-content-wrapper delayed-fade-up">
      <div class="guide-container">
        <header class="guide-header">
          <h1 class="guide-title">서비스 가이드</h1>
          <p class="guide-sub">혜성과 함께 당신의 숨겨진 영화 DNA를 찾아보세요.</p>
        </header>

        <section class="guide-section">
          <h2 class="sec-title">📊 취향 분석 차트 보는 법</h2>
          <div class="guide-card">
            <p>여기에 차트 설명 콘텐츠가 들어갑니다.</p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* --- 기본 스타일 유지 --- */
.guide-page { background: var(--bg); color: var(--text); min-height: 100vh; position: relative; overflow-x: hidden; }
.guide-content-wrapper { padding: 120px 20px; }
.guide-container { max-width: 900px; margin: 0 auto; }
/* ... (기존 헤더, 섹션 스타일 생략 - 그대로 사용하시면 됩니다) ... */

/* ----------------------------------------------------
   🌠 혜성 애니메이션 스타일 (와구와구 버전)
---------------------------------------------------- */

/* 로더 레이어: 화면을 덮고 클릭 방지 */
.comet-loader-layer {
  position: fixed; inset: 0; z-index: 9999;
  pointer-events: none; /* 클릭 통과 */
  overflow: hidden;
}

/* 혜성 컨테이너: 대각선 이동 애니메이션 */
.comet-container {
  position: absolute;
  top: -10%; left: -10%;
  width: 200px; height: 200px;
  transform: rotate(-45deg); /* 혜성 각도 조절 */
  animation: cometPass 1.8s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
}

/* 혜성 본체 (머리와 꼬리) */
.comet {
  position: absolute;
  top: 50%; right: 0;
  width: 12px; height: 12px;
  background: #fff;
  border-radius: 50%;
  transform: translateY(-50%);
  /* 핵심! 테마별 포인트 컬러로 빛나는 꼬리 표현 */
  box-shadow: 
    0 0 15px 5px #fff,
    0 0 30px 10px var(--primary), /* 테마 하이라이트 */
    -20px 0 40px 15px var(--primary),
    -50px 0 60px 20px var(--primary-weak),
    -100px 0 80px 30px transparent;
}

/* 주변 별 파티클 (반짝임 효과) */
.star-particle {
  position: absolute;
  background: #fff;
  border-radius: 50%;
  opacity: 0;
  animation: twinkle 1.8s ease-in-out infinite;
}
/* 파티클 랜덤 배치 및 타이밍 */
.p1 { width: 4px; height: 4px; top: 20%; left: 30%; animation-delay: 0.2s; }
.p2 { width: 6px; height: 6px; top: 60%; left: 10%; animation-delay: 0.5s; }
.p3 { width: 3px; height: 3px; top: 40%; left: 80%; animation-delay: 0.8s; }
.p4 { width: 5px; height: 5px; top: 80%; left: 50%; animation-delay: 1.1s; }
.p5 { width: 4px; height: 4px; top: 10%; left: 70%; animation-delay: 0.3s; }

/* 콘텐츠 등장 애니메이션 (혜성 통과 후) */
.delayed-fade-up {
  opacity: 0;
  transform: translateY(30px);
  animation: contentAppear 0.8s ease-out 0.8s forwards; /* 0.8초 딜레이 후 실행 */
}

/* === 키프레임 정의 === */

/* 혜성이 화면을 가로지르는 움직임 */
@keyframes cometPass {
  0% { transform: rotate(-45deg) translateX(0) scale(0.8); opacity: 0; }
  20% { opacity: 1; }
  100% { transform: rotate(-45deg) translateX(200vw) scale(1.2); opacity: 0; }
}

/* 별 파티클 반짝임 */
@keyframes twinkle {
  0%, 100% { opacity: 0; transform: scale(0.5); }
  50% { opacity: 0.8; transform: scale(1); box-shadow: 0 0 10px #fff; }
}

/* 콘텐츠 부드럽게 떠오르기 */
@keyframes contentAppear {
  to { opacity: 1; transform: translateY(0); }
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 22px;
  box-shadow: var(--shadow);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}

.logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.brand h1 {
  margin: 0;
  font-size: 20px;
  color: var(--text);
  font-weight: 900;
}

.form {
  display: grid;
  gap: 10px;
}

.label {
  font-size: 12px;
  color: var(--muted);
  font-weight: 700;
}

.input {
  border: 1px solid var(--border);
  background: var(--input-bg);
  color: var(--text);
  border-radius: 10px;
  padding: 12px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-weak);
}

.btn {
  margin-top: 6px;
  padding: 12px;
  border-radius: 10px;
  border: 0;
  background: var(--primary);
  color: #fff;
  cursor: pointer;
  font-weight: 800;
  transition: opacity 0.2s;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
  filter: brightness(1.1);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.error {
  margin: 8px 0 0;
  color: #ff4d4f;
  font-size: 13px;
  font-weight: 700;
}

.footer {
  margin-top: 16px;
  font-size: 13px;
  color: var(--muted);
  text-align: center;
}

.link {
  color: var(--primary);
  font-weight: 800;
  cursor: pointer;
  margin-left: 6px;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.helper-links {
  margin-top: 8px;
}

.divider {
  margin: 0 8px;
  opacity: 0.6;
}


</style>

