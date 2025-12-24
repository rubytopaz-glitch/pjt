<template>
  <section class="row-section">
    <div class="head">
      <h3>{{ title }}</h3>
      <router-link v-if="moreLink" :to="moreLink" class="more">더보기 ></router-link>
    </div>
    <div class="row-list">
      <slot></slot>
      <div v-if="isEmpty" class="empty-msg">{{ emptyMsg }}</div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: String,
  moreLink: [Object, String],
  isEmpty: Boolean,
  emptyMsg: String
})
</script>

<style scoped>

.row-section { margin-bottom: 40px; }

.head { 
  display: flex; 
  justify-content: space-between; 
  align-items: flex-end; 
  margin-bottom: 14px; 
  border-bottom: 1px solid var(--border); 
  padding-bottom: 10px; 
}

.head h3 { 
  font-size: 20px; 
  font-weight: 800; 
  margin: 0; 
  color: var(--text); 
}

.more { 
  font-size: 13px; 
  color: var(--muted); 
  text-decoration: none; 
  transition: color 0.2s;
}
.more:hover {
  color: var(--primary); 
}

.row-list { 
  display: flex; 
  gap: 14px; 
  overflow-x: auto; 
  padding-bottom: 10px; 
  scroll-behavior: smooth; 
}


.row-list::-webkit-scrollbar { height: 6px; }
.row-list::-webkit-scrollbar-thumb { 
  background: var(--border); /* #ccc -> var(--border)로 교체하여 테마에 반응 */
  border-radius: 3px; 
}
.row-list::-webkit-scrollbar-thumb:hover {
  background: var(--muted); /* 마우스 올릴 때만 살짝 더 진하게 */
}

.empty-msg { 
  width: 100%; 
  padding: 20px 0; 
  color: var(--muted); 
  font-size: 14px; 
}
</style>