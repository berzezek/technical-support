<template>
    <div>
        <Table :rows="leads" :columns="columns" @row-click="handleRowClick" />
    </div>
</template>

<script setup lang="ts">
const { leads, fetchLeads } = useLead();

const columns = [
    { key: 'id', label: 'ID', type: 'number' },
    { key: 'first_name', label: 'Имя', type: 'string' },
    { key: 'last_name', label: 'Фамилия', type: 'string' },
    { key: 'phone', label: 'Телефон', type: 'string' },
    { key: 'email', label: 'Email', type: 'string' },
    { key: 'status', label: 'Статус', type: 'string' },
    { key: 'created_at', label: 'Создано', type: 'date' },
    { key: 'updated_at', label: 'Обновлено', type: 'date' },
];

function handleRowClick(row: any) {
    console.log('Клик по строке:', row);
}

onMounted(() => {
    fetchLeads();
});
</script>
