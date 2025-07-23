<script setup lang="ts">
const { isAuthenticated } = useAuth();
const {
  connect,
  disconnect,
  process_instances,
  process_definitions,
} = useTasksSocket();
const route = useRoute();

onMounted(() => {
  if (isAuthenticated.value && route.path !== '/login') {
    connect();
  }
});

onUnmounted(() => {
  disconnect();
});

// 🔽 Фильтрация — можно расширить по state, версии и т.д.
const filterMode = ref<'all'>('all');

const filteredProcessDefinitions = computed(() => {
  return process_definitions.value;
});

const filteredProcessInstances = computed(() => {
  return process_instances.value;
});

// 📘 Колонки под process_definitions
const definitionColumns = [
  { key: 'key', label: 'Key', type: 'string' },
  { key: 'name', label: 'Название', type: 'string' },
  { key: 'version', label: 'Версия', type: 'number' },
  { key: 'bpmnProcessId', label: 'ID процесса', type: 'string' },
  { key: 'tenantId', label: 'Тенант', type: 'string' },
];

// 🔁 Колонки под process_instances
const instanceColumns = [
  { key: 'key', label: 'Key', type: 'string' },
  { key: 'bpmnProcessId', label: 'ID процесса', type: 'string' },
  { key: 'processVersion', label: 'Версия', type: 'number' },
  { key: 'state', label: 'Состояние', type: 'string' },
  { key: 'startDate', label: 'Старт', type: 'date' },
  { key: 'endDate', label: 'Завершение', type: 'date' },
  { key: 'incident', label: 'Инцидент', type: 'boolean' },
];

function handleRowClick(row: any) {
  console.log('Клик по строке:', row);
}
</script>



<template>
  <div>
    <h2>💡 Определения процессов (Definitions)</h2>
    <Table :columns="definitionColumns" :rows="filteredProcessDefinitions" @row-click="handleRowClick" />

    <div style="margin-top: 2rem;"></div>

    <h2>🌀 Запущенные процессы (Instances)</h2>
    <Table :columns="instanceColumns" :rows="filteredProcessInstances" @row-click="handleRowClick" />
  </div>
</template>
