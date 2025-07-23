<template>
  <label class="gui-radio">
    <input
      type="radio"
      :name="name"
      :value="value"
      :checked="modelValue === value"
      @change="$emit('update:modelValue', value)"
    />
    <span>{{ label }}</span>
  </label>
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  value: [String, Number],
  label: String,
  name: String,
});
defineEmits(['update:modelValue']);
</script>

<style scoped>
.gui-radio {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-family: 'Segoe UI', Tahoma, sans-serif;
  margin-right: 12px;
  white-space: nowrap;
}

.gui-radio input[type='radio'] {
  accent-color: #555;
  margin: 0;
  cursor: pointer;
}
</style>
