<template>
  <div class="terms-body">
    <p class="effective-date">본 약관은 2025년 12월 23일부터 적용됩니다.</p>

    <section>
      <h4>제1조 (목적)</h4>
      <p>본 약관은 주식회사 혜성(이하 "회사")이 운영하는 서비스 '혜성(The Comet)'에서 제공하는 영화 정보 제공, 리뷰 작성, 취향 분석 및 추천 서비스(이하 "서비스")를 이용함에 있어 회사와 이용자의 권리, 의무 및 책임 사항을 규정함을 목적으로 합니다.</p>
    </section>

    <section>
      <h4>제2조 (서비스의 내용)</h4>
      <p>회사는 이용자에게 다음과 같은 서비스를 제공합니다.</p>
      <ul>
        <li>TMDB(The Movie Database) API를 기반으로 한 영화 및 인물 정보 제공</li>
        <li>이용자의 영화 리뷰 작성 및 공유 기능</li>
        <li>사용자 데이터를 기반으로 한 개인별 맞춤 영화 추천</li>
        <li>기타 회사가 추가로 개발하거나 다른 회사와의 제휴를 통해 제공하는 서비스</li>
      </ul>
    </section>

    <section>
      <h4>제3조 (게시물의 저작권 및 관리)</h4>
      <ol>
        <li>이용자가 서비스 내에 게시한 리뷰 등 게시물의 저작권은 해당 게시물의 저작자에게 귀속됩니다.</li>
        <li>이용자는 회사가 서비스 홍보 및 운영 목적으로 게시물을 복제, 수정, 전시할 수 있음에 동의합니다.</li>
        <li>타인의 저작권을 침해하거나 명예를 훼손하는 게시물은 사전 통보 없이 삭제될 수 있습니다.</li>
      </ol>
    </section>

    <section>
      <h4>제4조 (책임의 제한)</h4>
      <p>회사는 TMDB 등 외부 API를 통해 제공받는 정보의 정확성이나 신뢰성에 대해 보증하지 않으며, 해당 정보로 인해 발생하는 손해에 대해 책임을 지지 않습니다.</p>
    </section>

    <section class="warning-section">
      <h4>🚫 이용 제한 사항</h4>
      <p>비정상적인 방법(크롤링, 해킹 등)으로 서비스에 접근하거나, 다른 사용자의 활동을 방해하는 경우 계정 이용이 즉시 제한될 수 있습니다.</p>
    </section>
  </div>
</template>

<style scoped>
.terms-body { font-size: 14px; line-height: 1.6; color: var(--text); text-align: left; }
.effective-date { font-weight: 800; color: var(--primary); margin-bottom: 20px; }
section { margin-bottom: 25px; }
h4 { font-size: 16px; font-weight: 900; margin-bottom: 10px; color: var(--text); }
ul, ol { padding-left: 20px; margin: 10px 0; }
li { margin-bottom: 6px; }

.warning-section {
  background: var(--primary-weak);
  padding: 15px;
  border-radius: 10px;
  border: 1px dashed var(--primary);
}
</style>