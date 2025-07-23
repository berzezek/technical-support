<template>
  <!-- Верхняя часть с двумя панелями -->
  <div
    class="main-top"
    :class="{ column: isMobile }"
    :style="!isMobile ? { height: topHeight + 'px' } : {}"
  >
    <div class="main" :class="{ column: isMobile }">
      <div
        ref="leftPane"
        class="pane pane-left"
        :style="!isMobile ? { width: leftWidth + 'px' } : {}"
      >
        <div class="pane-content">
          <Button
            label="Нажми меня"
            icon="https://object.pscloud.io/darbiz/catalogs/ef5/72919243-ef52-11ef-889e-96c29f86e4bb.webp"
            @click="handleClick"
          />
          <SelectMain v-model="selectedOption" :options="optionData" />
          <p>Выбрано: {{ selectedOption }}</p>
        </div>
        <Input />
      </div>

      <div
        v-if="!isMobile"
        class="divider-vertical"
        @mousedown="startResizeHorizontal"
      ></div>

      <div class="pane pane-right">
        <div class="pane-content">
          <Table
            :columns="[
              {
                key: 'name',
                label: 'Имя',
                type: 'string',
                searchable: true,
              },
              {
                key: 'amount',
                label: 'Сумма',
                type: 'number',
                colorize: true,
              },
              { key: 'paid', label: 'Оплачено', type: 'boolean' },
              { key: 'date', label: 'Дата', type: 'date' },
            ]"
            :rows="[
              {
                name: 'Алексей',
                amount: 1500,
                paid: true,
                date: '2025-06-20',
              },
              {
                name: 'Ошибка платежа',
                amount: 0,
                paid: false,
                date: '2025-06-21',
              },
            ]"
            :onRowClick="handleClick"
          />
        </div>
      </div>
    </div>
  </div>

  <!-- Горизонтальная перемычка -->
  <div
    v-if="!isMobile"
    class="divider-horizontal"
    @mousedown="startResizeVertical"
  ></div>

  <!-- Нижняя панель -->
  <div class="bottom-pane">
    <div class="pane-content">
      <CardList :items="statusItems" :onClick="handleCardClick" />
    </div>
  </div>
</template>

<script setup>
  const selectedOption = ref('one');

  const leftWidth = ref(400);
  const topHeight = ref(300);
  const isMobile = ref(false);

  let isResizingHorizontal = false;
  let isResizingVertical = false;

  const optionData = [
    { label: 'Выбор 1', value: 'one' },
    { label: 'Выбор 2', value: 'two' },
    { label: 'Выбор 3', value: 'three' },
  ];

  function startResizeHorizontal(e) {
    isResizingHorizontal = true;
    document.addEventListener('mousemove', handleMouseMoveHorizontal);
    document.addEventListener('mouseup', stopResize);
  }

  function handleMouseMoveHorizontal(e) {
    if (!isResizingHorizontal) return;
    leftWidth.value = Math.max(
      200,
      Math.min(e.clientX, window.innerWidth - 200)
    );
  }

  function startResizeVertical(e) {
    isResizingVertical = true;
    document.addEventListener('mousemove', handleMouseMoveVertical);
    document.addEventListener('mouseup', stopResize);
  }

  function handleMouseMoveVertical(e) {
    if (!isResizingVertical) return;
    const footerHeight = 40;
    const headerHeight = 50;
    const maxHeight = window.innerHeight - footerHeight - headerHeight - 100;
    topHeight.value = Math.max(
      150,
      Math.min(e.clientY - headerHeight, maxHeight)
    );
  }

  function stopResize() {
    isResizingHorizontal = false;
    isResizingVertical = false;
    document.removeEventListener('mousemove', handleMouseMoveHorizontal);
    document.removeEventListener('mousemove', handleMouseMoveVertical);
    document.removeEventListener('mouseup', stopResize);
  }

  function checkMobile() {
    isMobile.value = window.innerWidth < 768;
  }

  function handleClick() {
    console.log('Нажато!');
  }

  const statusItems = [
    { label: 'Дозвонились', value: 7, color: '#cfcffe' },
    { label: 'Забрать забор', value: 12, color: '#9accfe' },
    { label: 'Спам', value: 92, color: '#cecdce' },
    { label: 'Полуцелевой', value: 4, color: '#ffd701' },
    { label: 'Целевой', value: 4, color: '#d8c566' },
    { label: 'Дожми или доведи', value: 11, color: '#fe424f' },
    // добавь остальные
  ];

  function handleCardClick(item) {
    console.log('Клик по карточке:', item);
  }

  onMounted(() => {
    checkMobile();
    window.addEventListener('resize', checkMobile);
  });

  onBeforeUnmount(() => {
    window.removeEventListener('resize', checkMobile);
  });
</script>

<style scoped>
  .main-top {
    display: flex;
    overflow: hidden;
  }

  .main-top.column {
    flex-direction: column;
    height: auto !important;
  }

  .main {
    flex: 1;
    display: flex;
    overflow: hidden;
  }

  .main.column {
    flex-direction: column;
  }

  .pane {
    overflow: auto;
    background-color: white;
  }

  .pane-left {
    min-width: 200px;
    max-width: 100%;
    border-right: 1px solid #ccc;
  }

  .pane-right {
    flex: 1;
  }

  .pane-content {
    padding: 16px;
  }

  .divider-vertical {
    width: 5px;
    background-color: #888;
    cursor: col-resize;
  }

  .divider-horizontal {
    height: 5px;
    background-color: #666;
    cursor: row-resize;
  }

  .bottom-pane {
    flex: 1;
    overflow: auto;
    background-color: #fff;
  }
</style>
