<template>
  <div class="privacy-body">
    <p class="effective-date">본 방침은 2025년 11월 14일부터 적용됩니다.</p>
    
    <p>주식회사 혜성(The Comet)은 회원의 개인정보 보호를 소중하게 생각하며, 관련 법령을 준수하기 위해 최선을 다하고 있습니다.</p>

    <section>
      <h4>제1조 개인정보의 수집 ∙ 이용 목적 및 항목</h4>
      <p>회사는 서비스 제공을 위해 필요한 최소한의 개인정보를 수집합니다.</p>
      
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>수집 목적</th>
              <th>수집 항목</th>
              <th>보유 기간</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>회원 가입 및 관리</td>
              <td>이메일주소, 비밀번호, 닉네임</td>
              <td>회원 탈퇴 시까지</td>
            </tr>
            <tr>
              <td>본인 및 연령 확인</td>
              <td>이름, 생년월일, 휴대전화번호, CI/DI</td>
              <td>회원 탈퇴 시까지</td>
            </tr>
            <tr>
              <td>상품 결제 및 환불</td>
              <td>카드정보, 계좌번호, 결제 기록</td>
              <td class="highlight">5년 (법정 보관)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section>
      <h4>제2조 개인정보의 보관 및 이용기간</h4>
      <ul>
        <li>계약 또는 청약철회 등에 관한 기록: 5년</li>
        <li>대금결제 및 재화의 공급에 관한 기록: 5년</li>
        <li>웹사이트 방문 기록(접속 로그): 3개월</li>
      </ul>
    </section>

    <section>
      <h4>제3조 개인정보의 처리 위탁</h4>
      <p>회사는 원활한 서비스 제공을 위해 아래와 같이 업무를 위택하고 있습니다.</p>
      <div class="table-wrapper">
        <table>
          <tbody>
            <tr>
              <th>결제 대행</th>
              <td>다날, KG이니시스, 네이버파이낸셜</td>
            </tr>
            <tr>
              <th>본인 인증</th>
              <td>KCB (코리아크레딧뷰로)</td>
            </tr>
            <tr>
              <th>서버 운영</th>
              <td>Amazon Web Services (AWS)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="kids-section">
      <h4>🧸 어린이를 위한 요약</h4>
      <p>부모님 동의 없이는 가입할 수 없으며, 여러분의 소중한 정보는 서비스 운영을 위해서만 사용되고 탈퇴하면 즉시 지워집니다.</p>
    </section>

    <div class="contact">
      <p><strong>개인정보보호책임자:</strong> 정인수 (cs@thecomet.com)</p>
    </div>
  </div>
</template>

<style scoped>
.privacy-body {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  text-align: left;
}

.effective-date {
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 20px;
}

section { margin-bottom: 25px; }

h4 {
  font-size: 16px;
  font-weight: 900;
  margin-bottom: 10px;
  color: var(--text);
}

ul { padding-left: 20px; margin: 10px 0; }
li { margin-bottom: 4px; }

/* 테이블 스타일 */
.table-wrapper {
  width: 100%;
  overflow-x: auto;
  margin: 10px 0;
  border: 1px solid var(--border);
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th, td {
  padding: 10px;
  border: 1px solid var(--border);
  text-align: left;
}

th { background: var(--primary-weak); font-weight: 800; }

.highlight { font-weight: 800; color: var(--primary); }

.kids-section {
  background: var(--primary-weak);
  padding: 15px;
  border-radius: 10px;
  margin-top: 30px;
}

.contact {
  margin-top: 30px;
  padding-top: 15px;
  border-top: 1px solid var(--border);
  font-size: 13px;
}
</style>