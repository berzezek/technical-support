<template>
  <div
    class="dashboard-card"
    :style="{ backgroundColor: item.color || '#f0f0f0' }"
  >
    <div class="card-content">
      <div class="card-label">{{ item.label }}</div>
      <div class="card-value">{{ item.value }}</div>
    </div>
  </div>
</template>

<script setup>
  const props = defineProps({
    item: Object,
  });
</script>

<style scoped>
.dashboard-card {
  width: 160px; /* шире */
  height: 80px; /* выше */
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #ccc;
  border-radius: 6px;
  box-sizing: border-box;
  background-color: white;
  font-family: 'Segoe UI', Tahoma, sans-serif;
  text-align: center;
  cursor: pointer;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-label {
  font-size: 13px;
  color: black;
  line-height: 1.2;
  text-align: center;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: black;
}
</style>
