<template>
  <div class="tabs">
    <button 
      v-for="t in tabs" 
      :key="t.value"
      :class="['tab', { active: modelValue === t.value }]" 
      @click="$emit('update:modelValue', t.value)"
    >
      {{ t.label }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String
})
defineEmits(['update:modelValue'])

const tabs = [
  { label: '보관함', value: 'vault' },
  { label: '좋아요', value: 'likes' }
]
</script>

<style scoped>
.tabs { display: flex; border-bottom: 2px solid var(--border); margin-bottom: 30px; }
.tab { flex: 1; padding: 14px; font-size: 16px; font-weight: 700; background: none; border: none; cursor: pointer; color: var(--muted); transition: 0.2s; }
.tab.active { color: var(--text); border-bottom: 2px solid var(--text); margin-bottom: -2px; }
</style>