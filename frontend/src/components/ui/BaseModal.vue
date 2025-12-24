<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click="$emit('close')">
      <div class="modal-content" @click.stop>
        <header class="modal-header">
          <h3>{{ title }}</h3>
          <button class="close-btn" @click="$emit('close')">X</button>
        </header>
        <div class="modal-body">
          <slot></slot>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  open: Boolean,
  title: String
})

/** ✅ [수정 핵심] emits 선언을 추가하여 경고를 제거합니다. */
defineEmits(['close'])
</script>

<style scoped>
/* 배경 레이어 */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6); /* 배경을 조금 더 어둡게 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px; /* 모바일에서 화면 끝에 붙지 않게 여백 */
  backdrop-filter: blur(2px); /* 배경 살짝 흐리게 (선택 사항) */
}

/* 모달 본체 */
.modal-content {
  background: var(--card, #ffffff);
  color: var(--text, #111111);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  
  /* [핵심] 유연한 크기 설정 */
  width: 100%;             /* 기본적으로 가득 채움 */
  max-width: 550px;        /* 하지만 최대 550px까지만 커짐 */
  max-height: 85vh;        /* 화면 높이의 85%까지만 커짐 */
  
  display: flex;
  flex-direction: column;  /* 헤더, 바디를 세로로 배치 */
  overflow: hidden;        /* 자식이 삐져나오지 않게 */
  position: relative;
}

/* 헤더 영역 */
.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border, #eee);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

/* [핵심] 스크롤 가능한 바디 영역 */
.modal-body {
  padding: 24px;
  overflow-y: auto;        /* 내용이 길어지면 내부에서 스크롤 생성 */
  flex: 1;                 /* 남은 공간을 모두 차지 */
}

/* 닫기 버튼 */
.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--muted, #6b7280);
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}

.close-btn:hover {
  color: var(--text);
}
</style>