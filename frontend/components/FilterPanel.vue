<template>
    <div class="erp-toolbar">
        <!-- 🔹 Строка с фильтрами кнопок -->
        <div class="toolbar-row filters-row">
            <Button label="👁️‍🗨️" @click="onViewClick" />
            <Button label="ℹ️" @click="onInfoClick" />
            <Button v-for="f in filterButtons" :key="f" :label="f" :selected="status === f" @click="status = f" />
            <Dropdown v-model="serviceCenter" :options="scOptions" />
        </div>

        <!-- 🔹 Первая строка -->
        <div class="toolbar-row">
            <Dropdown v-model="status" :options="statusOptions" />
            <Dropdown v-model="author" :options="authorOptions" />
            <Calendar v-model="dateFrom" />
            <Calendar v-model="dateTo" />
            <Dropdown v-model="relevance" :options="relevanceOptions" />
        </div>

        <!-- 🔹 Вторая строка -->
        <div class="toolbar-row split-row">
            <div class="toolbar-group">
                <Button v-for="item in periodOptions" :key="item" :label="item" :selected="period === item"
                    @click="period = item" />
            </div>

            <div class="radio-column">
                <RadioButton v-model="projectType" name="project" label="Все" value="all" />
                <RadioButton v-model="projectType" name="project" label="Проект Кофе" value="coffee" />
                <RadioButton v-model="projectType" name="project" label="Проект ТО" value="to" />
            </div>

            <div class="toolbar-group">
                <Button v-for="manager in managers" :key="manager" :label="manager" @click="selectManager(manager)" />
            </div>
        </div>
    </div>
</template>


<script setup lang="ts">
const status = ref('');
const author = ref('');
const dateFrom = ref('');
const dateTo = ref('');
const relevance = ref('');
const serviceCenter = ref('');
const period = ref('День');
const projectType = ref('all');

const statusOptions = ['Все', 'Мои', 'Команда', 'ОП1', 'ОП2'];
const authorOptions = ['Автор 1', 'Автор 2'];
const relevanceOptions = ['Актуальные', 'Все'];
const scOptions = ['СЦ 1', 'СЦ 2'];
const periodOptions = ['День', 'Неделя', 'Месяц'];
const managers = ['КМ ОР Джаббаров Зариф', 'КМ ОР Потапов Александр'];

const radioProjects = {
    all: 'Все',
    coffee: 'Проект Кофе',
    to: 'Проект ТО',
};

function selectManager(name: string) {
    console.log('Менеджер:', name);
}

const filterButtons = ['Все', 'Мои', 'Команда', 'ОП1', 'ОП2'];

function onViewClick() {
    console.log('👁️‍🗨️ Нажато');
}
function onInfoClick() {
    console.log('ℹ️ Нажато');
}
</script>

<style scoped>
.erp-toolbar {
    display: flex;
    flex-direction: column;
    gap: 6px;
    background: #fdfdfd;
    padding: 6px;
    font-family: 'Segoe UI', Tahoma, sans-serif;
    border-bottom: 1px solid #ccc;
}

/* общая строка */
.toolbar-row {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: nowrap;
}

/* для 2-й строки — несколько групп */
.split-row {
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

/* группа внутри строки */
.toolbar-group {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: nowrap;
}

/* радиокнопки */
.radio-row {
    gap: 16px;
}

.radio-label {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    user-select: none;
}

.radio-label input[type='radio'] {
    accent-color: #444;
    margin: 0;
    cursor: pointer;
}

.toolbar-row {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: nowrap;
}

.radio-column {
    display: flex;
    flex-direction: column;
    /* 💥 вот это ключ */
    gap: 4px;
}

.filters-row {
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 4px;
}

.erp-toolbar {
    display: flex;
    flex-direction: column;
    gap: 6px;
    background: #fdfdfd;
    padding: 6px;
    font-family: 'Segoe UI', Tahoma, sans-serif;
    border-bottom: 1px solid #ccc;
}

.toolbar-row {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: nowrap;
}

.split-row {
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

.toolbar-group {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: nowrap;
}

.radio-column {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
</style>
