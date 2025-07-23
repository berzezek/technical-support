<template>
  <div class="left-panel">
    <!-- 🔹 Блок 1 -->
    <div class="block block-1">
      <!-- Ввод телефона и кнопки -->
      <div class="input-toolbar">
        <!-- Ввод -->
        <div class="input-phone">
          <Input v-model="phoneNumber" placeholder="Введите номер" />
        </div>

        <!-- Кнопки -->
        <div class="toolbar-buttons">
          <Button @click="searchByPhone" label="🔍" />
          <Button label="📄" />
          <Button @click="getLeads" label="👤" />
          <Button label="➕" />
        </div>

        <!-- Привязанный лид -->
        <div class="linked-lead-box">
          Привязанный Лид: <strong>{{ usedLead ? `${usedLead.last_name} ${usedLead.phone}` : " ПУСТО" }}</strong>
        </div>
      </div>
      <div class="info-title">
        <p>Информация</p>
        <hr />
      </div>
      <!-- Информация -->
      <div class="info-box">
        <Table :rows="categories" :columns="categoryColumns" @row-click="onCategoryClick" />
        <Table :rows="fetchedProducts" :columns="productColumns" />
      </div>
    </div>

    <!-- 🔹 Блок 2 -->
    <div class="block block-2">
      <p class="section-title">"Найденные ЛИДы</p>
      <table>
        <thead>
          <tr>
            <th>Статус</th>
            <th>Автор</th>
            <th>Создано</th>
            <th>ФИО</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lead in leads" :key="lead.id">
            <td class="blue" @click="getTasks(lead)">{{ lead.status }}</td>
            <td>{{ lead.email }}</td>
            <td>{{ formatDate(lead.created_at) }}</td>
            <td>{{ lead.first_name }} {{ lead.last_name }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 🔹 Блок 3 -->
    <div class="block block-3">
      <p class="section-title">Найденные заявки</p>
      <table v-if="tasks">
        <thead>
          <tr>
            <th>Не найдено</th>
          </tr>
        </thead>
      </table>
      <table v-else>
        <thead>
          <tr>
            <th>!!!</th>
            <th>Клиент ФИО</th>
            <th>Создано</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.id }}</td>
            <td>{{ task.description }}</td>
            <td>---</td>
            <td><span class="status-red">Согласовать</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const phoneNumber = ref('');
const { leads, fetchLeads, fetchLeadsByPhone } = useLead();
const { tasks, fetchTasks } = useTask();

const fetchedProducts = ref([]);

const {
  categories,
  category,
  products,
  product,
  fetchCategories,
  fetchProducts,
  fetchProductById,
  fetchCategoryById
} = useReference();


const usedLead = ref(null);

const searchByPhone = async () => {
  await fetchLeadsByPhone(phoneNumber.value);
};

const getTasks = async (lead) => {
  await fetchTasks(lead.id);
  usedLead.value = lead;
};

const onCategoryClick = async (category) => {
  await fetchCategoryById(category.id);
  console.log('Selected category:', category);
  fetchedProducts.value = category.products || [];
};

const getLeads = async () => {
  await fetchLeads();
};

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleString('ru-RU');
}

const categoryColumns = [
  { title: 'Название', key: 'name' },
  { title: 'Описание', key: 'description' }
];

const productColumns = [
  { title: 'Название', key: 'name' },
  { title: 'Описание', key: 'description' }
];

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.left-panel {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  font-size: 13px;
  background: white;
  color: black;
}

/* Общие блоки */
.block {
  flex: 1;
  min-height: 0;
  overflow: auto;
  padding: 8px;
  border-bottom: 1px solid #ccc;
}

.block:last-child {
  border-bottom: none;
}

/* Ввод */
.input-row {
  display: flex;
  gap: 4px;
  margin-bottom: 6px;
}

.input-row input {
  flex: 1;
  padding: 4px;
  border: 1px solid #999;
}

.input-row button {
  padding: 4px 6px;
  border: 1px solid #999;
  background: #f1f1f1;
  cursor: pointer;
}

/* Вкладки */
.tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
}

.tabs button {
  padding: 3px 8px;
  border: 1px solid #aaa;
  background: #eee;
  cursor: pointer;
}

/* Инфобокс */
.info-box {
  border: 1px solid #ddd;
  padding: 6px;
  height: 100%;
  overflow-y: auto;
}

/* Таблицы */
.section-title {
  font-weight: bold;
  margin-bottom: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

th,
td {
  border-bottom: 1px solid #ddd;
  padding: 4px;
  text-align: left;
}

th {
  background: #f9f9f9;
}

.blue {
  color: blue;
}

.status-red {
  background: red;
  color: white;
  padding: 2px 4px;
}

.tab-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.toolbar-buttons {
  display: flex;
  gap: 4px;
}

.linked-lead-line {
  display: flex;
  align-items: center;
  border: 1px solid #999;
  padding: 2px 6px;
  height: 28px;
  font-size: 12px;
  background: #f9f9f9;
  white-space: nowrap;
}

.linked-lead-line label {
  margin-right: 6px;
  color: #000;
}

.linked-lead-value {
  font-weight: bold;
  font-family: monospace;
  color: #333;
  background: #fff;
  padding: 2px 6px;
  border: 1px solid #ccc;
  min-width: 60px;
  display: inline-block;
}

.input-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 6px;
}

.input-phone {
  flex: 1;
  min-width: 150px;
}

.input-phone input {
  height: 28px;
  padding: 4px 8px;
  font-size: 13px;
  border: 1px solid #999;
  width: 100%;
  box-sizing: border-box;
}

.toolbar-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  flex: 1;
  min-width: 200px;
}


.toolbar-buttons button {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  font-size: 13px;
  border: 1px solid #aaa;
  background: #f2f2f2;
  height: 26px;
  cursor: pointer;
}

.icon {
  font-size: 14px;
}

.linked-lead-box {
  flex: 1 1 100%;
  font-size: 13px;
  padding: 4px 6px;
  border: 1px solid #aaa;
  background: #f4f4f4;
  white-space: nowrap;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

@media (max-width: 600px) {
  .input-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-buttons {
    justify-content: space-between;
  }

  .linked-lead-box {
    justify-content: flex-start;
  }
}

.info-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
}

.info-title p {
  margin: 0;
  font-size: 12px;
  color: #333;
  white-space: nowrap;
}

.info-title hr {
  flex-grow: 1;
  height: 1px;
  border: none;
  border-top: 1px solid #ccc;
}
</style>
