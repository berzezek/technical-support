<template>
  <div class="gui-input-wrapper">
    <label v-if="label" class="input-label">{{ label }}</label>
    <input
      class="input-global"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :class="{ 'input-error': error }"
    />
    <p v-if="error" class="error-text">{{ error }}</p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  label: String,
  placeholder: String,
  error: String,
});
defineEmits(['update:modelValue']);
</script>

<style scoped>
.gui-input-wrapper {
  width: 100%;
}

.input-label {
  font-size: 12px;
  margin-bottom: 4px;
  display: block;
}

.input-global {
  width: 100%;
  padding: 4px;
  font-size: 12px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.input-error {
  border-color: #d93025;
  background: #fff6f6;
}

.error-text {
  color: #d93025;
  font-size: 11px;
  margin-top: 2px;
}
</style>
