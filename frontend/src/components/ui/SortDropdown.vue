<template>
  <div class="sort-wrapper" v-if="options && options.length">
    <select :value="modelValue" @change="$emit('update:modelValue', $event.target.value)" class="sort-select">
      <option v-for="opt in options" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
    <div class="arrow">▼</div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, required: true },
  options: { 
    type: Array, 
    default: () => [
      { value: 'latest', label: '담은 순' },
      { value: 'oldest', label: '담은 역순' },
      { value: 'rating_high', label: '나의 별점 높은 순' },
      { value: 'rating_low', label: '나의 별점 낮은 순' },
      { value: 'new_release', label: '신작 순' },
      { value: 'old_release', label: '구작 순' },
    ]
  }
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.sort-wrapper {
  position: relative;
  display: inline-block;
}
.sort-select {
  appearance: none;
  padding: 8px 28px 8px 12px;
  font-size: 13px;
  font-weight: 700;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--card);
  color: var(--text);
  cursor: pointer;
  outline: none;
}
.sort-select:hover {
  background: var(--input-bg);
}
.arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 10px;
  color: var(--muted);
  pointer-events: none;
}
</style>