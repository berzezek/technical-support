<template>
  <div class="gui-select-wrapper">
    <select class="gui-select" v-model="selected" @change="onChange">
      <option v-for="item in options" :key="item.value" :value="item.value">
        {{ item.label }}
      </option>
    </select>
    <div class="dropdown-arrow">▼</div>
  </div>
</template>

<script setup>
const props = defineProps({
  options: Array,
  modelValue: [String, Number],
});
const emit = defineEmits(['update:modelValue']);

const selected = ref(props.modelValue);
watch(
  () => props.modelValue,
  (val) => (selected.value = val)
);
watch(selected, (val) => emit('update:modelValue', val));

function onChange(e) {
  emit('update:modelValue', e.target.value);
}
</script>

<style scoped>
.gui-select-wrapper {
  position: relative;
  display: inline-block;
  min-width: 100px;
  font-family: 'Segoe UI', Tahoma, sans-serif;
}

.gui-select {
  min-width: 120px;
  width: 100%;
  padding: 6px 30px 4px 8px;
  font-size: 12px;
  border: 2px solid #aaa;
  box-shadow: inset 0 0 0 1px white, 1px 1px 0 #999;
  border-radius: 0;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  cursor: pointer;
}

.dropdown-arrow {
  position: absolute;
  background: linear-gradient(to bottom, #f4f4f4, #dcdcdc);
  top: 2px;
  bottom: 2px;
  right: 2px;
  width: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  color: #333;
  font-size: 12px;
}
</style>