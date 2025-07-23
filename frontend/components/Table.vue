<template>
  <div class="table-container">
    <input v-model="globalSearch" class="search-input-global" placeholder="Поиск по таблице" />

    <table class="gui-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" @click="sortBy(col)">
            <div class="header-cell">
              {{ col.label }}
              <span v-if="sort.key === col.key">
                {{ sort.order === 'asc' ? '▲' : '▼' }}
              </span>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, idx) in filteredRows" :key="idx" @click="rowClick(row)" class="row">
          <td v-for="col in columns" :key="col.key" :class="getCellClass(row[col.key], col)">
            {{ formatValue(row[col.key], col.type) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  columns: Array,
  rows: Array,
});

const globalSearch = ref('');
const sort = ref({ key: '', order: 'asc' });

const emit = defineEmits(['row-click']);

function sortBy(col) {
  if (sort.value.key === col.key) {
    sort.value.order = sort.value.order === 'asc' ? 'desc' : 'asc';
  } else {
    sort.value.key = col.key;
    sort.value.order = 'asc';
  }
}

function formatValue(val, type) {
  if (type === 'boolean') return val ? '✔' : '✘';
  if (type === 'date') return new Date(val).toLocaleDateString();
  return val;
}

function getCellClass(value, col) {
  if (!col.colorize) return '';
  if (col.type === 'number') {
    return value > 1000 ? 'highlight-green' : 'highlight-red';
  }
  if (col.type === 'string' && value?.toLowerCase().includes('ошибка')) {
    return 'highlight-red';
  }
  return '';
}

const filteredRows = computed(() => {
  let result = [...props.rows];

  if (globalSearch.value.trim()) {
    const term = globalSearch.value.toLowerCase();
    result = result.filter((row) => {
      return props.columns.some((col) => {
        const value = String(row[col.key] ?? '').toLowerCase();
        return value.includes(term);
      });
    });
  }

  if (sort.value.key) {
    result.sort((a, b) => {
      const valA = a[sort.value.key];
      const valB = b[sort.value.key];
      if (valA === valB) return 0;
      return sort.value.order === 'asc'
        ? valA > valB
          ? 1
          : -1
        : valA < valB
          ? 1
          : -1;
    });
  }

  return result;
});

function rowClick(row) {
  emit('row-click', row);
}
</script>

<style scoped>
.table-container {
  overflow: auto;
}

.search-input-global {
  margin-bottom: 8px;
  padding: 4px;
  font-size: 12px;
  min-width: 120px;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, sans-serif;
}

.gui-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Segoe UI', Tahoma, sans-serif;
  font-size: 12px;
  background: white;
}

th,
td {
  border: 1px solid #ccc;
  padding: 4px;
  text-align: left;
}

th {
  background: #e0e0e0;
  user-select: none;
}

.header-cell {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.row:hover {
  background-color: #f0f0f0;
  cursor: pointer;
}

.highlight-green {
  background-color: #e0ffe0;
}

.highlight-red {
  background-color: #ffe0e0;
}
</style>