<template>
  <button class="gui-button" :class="{ active, selected }" @click="$emit('click')">
    <img v-if="icon" :src="icon" class="icon" alt="icon" />
    {{ label }}
  </button>
</template>

<script setup>
defineProps({
  label: String,
  icon: String,
  active: Boolean,
  selected: Boolean,
});
defineEmits(['click']);
</script>

<style scoped>
.gui-button {
  background: linear-gradient(to bottom, #e0e0e0, #c0c0c0);
  border: 1px solid #999;
  border-radius: 0;
  font-size: 12px;
  padding: 4px 12px;
  font-family: 'Segoe UI', Tahoma, sans-serif;
  box-shadow: inset 0 0 0 1px #fff, 1px 1px 0 #888;
  margin: 2px;
  cursor: pointer;
  min-width: 60px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  user-select: none;
  white-space: nowrap;
}

.gui-button:hover {
  background: linear-gradient(to bottom, #f0f0f0, #d0d0d0);
}

.gui-button:active {
  background: linear-gradient(to bottom, #cce0ff, #b0d0f0);
  box-shadow: inset 1px 1px 0 #3c6eb4;
  border-color: #5a90dc;
}

.gui-button.selected {
  background: #cce0ff;
  border-color: #5a90dc;
  box-shadow: inset 0 0 0 1px #fff, 1px 1px 0 #3c6eb4;
}

.gui-button.active {
  font-weight: bold;
  background: linear-gradient(to bottom, #d0e5ff, #b0d0f0);
}

.icon {
  width: 12px;
  height: 12px;
  object-fit: contain;
}
</style>
