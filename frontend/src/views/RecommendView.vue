<template>
  <main class="page">
    <section class="container">
      <h1 class="title">추천</h1>

      <div class="tabs">
        <button class="tab" :class="{ active: tab === 'chat' }" @click="tab = 'chat'">AI 맞춤</button>
        <button class="tab" :class="{ active: tab === 'genre' }" @click="tab = 'genre'">장르</button>
        <button class="tab" :class="{ active: tab === 'person' }" @click="tab = 'person'">인물</button>
        <button class="tab" :class="{ active: tab === 'user' }" @click="tab = 'user'">유저</button>
      </div>

      <RecommendAi v-if="tab === 'chat'" />
      <RecommendGenre v-else-if="tab === 'genre'" />
      <RecommendPerson v-else-if="tab === 'person'" />
      <RecommendUser v-else />
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import RecommendAi from '@/components/recommend/RecommendAi.vue'
import RecommendGenre from '@/components/recommend/RecommendGenre.vue'
import RecommendPerson from '@/components/recommend/RecommendPerson.vue'
import RecommendUser from '@/components/recommend/RecommendUser.vue'

const tab = ref('chat')
</script>

<style scoped>

/* ✅ 배경색과 글자색을 테마 변수로 교체 */
.page { 
  min-height: calc(100vh - 60px); 
  background: var(--bg); /* #fff 대신 변수 사용 */
  color: var(--text);   /* 글자색 명시 */
  transition: background-color 0.3s, color 0.3s;
}

.container { width: min(1000px, 92vw); margin: 0 auto; padding: 22px 0 60px; }

/* ✅ 제목 색상도 변수 적용 */
.title { 
  margin: 0 0 14px; 
  font-size: 26px; 
  font-weight: 900; 
  color: var(--text); 
}

.tabs { display: flex; gap: 8px; margin-bottom: 14px; }

/* ✅ 탭 스타일에도 변수 적용 */
.tab {
  height: 38px; padding: 0 12px; border-radius: 12px;
  border: 1px solid var(--border); /* 변수 사용 */
  background: var(--card);        /* 변수 사용 */
  color: var(--text);             /* 변수 사용 */
  font-weight: 900; cursor: pointer;
  transition: all 0.2s;
}

.tab.active { 
  border-color: var(--primary); 
  background: var(--primary); 
  color: #fff; /* 활성화된 탭은 가독성을 위해 흰색 고정 가능 */
}
</style>
