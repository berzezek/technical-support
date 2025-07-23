<template>
  <div class="dashboard-grid">
    <div v-for="item in items" :key="item.label" @click="() => onClick(item)">
      <Card :item="item" />
    </div>
  </div>
</template>

<script setup>
  const props = defineProps({
    items: Array,
    onClick: Function,
  });
</script>

<style scoped>
  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* по 3 в ряд */
    gap: 12px;
    justify-items: center;
    align-items: center;
    max-width: 600px; /* ограничим ширину, чтобы выглядело ровно */
    margin: 0 auto; /* по центру */
  }
</style>
