<template>
  <div class="layout">
    <!-- Левая панель -->
    <div class="pane-left" :style="{ width: leftWidth + 'px' }">
      <LeftPanel />
    </div>

    <!-- Вертикальный разделитель -->
    <div class="divider-vertical" @mousedown="startResizeHorizontal"></div>

    <!-- Правая панель -->
    <div class="pane-right">
      <div
        class="pane-right-top"
        :style="{ height: rightTopHeight + 'px' }"
      ><RightTopPanel /></div>
      <div
        class="divider-horizontal"
        @mousedown="startResizeRightVertical"
      ></div>
      <div class="pane-right-bottom">
        <Task />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  const leftWidth = useCookie<number>('left_width', { sameSite: 'lax' });
  const rightTopHeight = useCookie<number>('right_top_height', {
    sameSite: 'lax',
  });

  // Устанавливаем значения по умолчанию
  if (!leftWidth.value) leftWidth.value = 400;
  if (!rightTopHeight.value) rightTopHeight.value = 300;

  let isResizingHorizontal = false;
  let isResizingRightVertical = false;

  function startResizeHorizontal() {
    isResizingHorizontal = true;
    document.addEventListener('mousemove', handleMouseMoveHorizontal);
    document.addEventListener('mouseup', stopResize);
  }

  function handleMouseMoveHorizontal(e: MouseEvent) {
    if (!isResizingHorizontal) return;
    leftWidth.value = Math.max(200, e.clientX);
  }

  function startResizeRightVertical() {
    isResizingRightVertical = true;
    document.addEventListener('mousemove', handleMouseMoveRightVertical);
    document.addEventListener('mouseup', stopResize);
  }

  function handleMouseMoveRightVertical(e: MouseEvent) {
    if (!isResizingRightVertical) return;
    const y = e.clientY;
    const headerOffset = 0; // если есть хедер — установи нужную высоту
    rightTopHeight.value = Math.max(100, y - headerOffset);
  }

  function stopResize() {
    isResizingHorizontal = false;
    isResizingRightVertical = false;
    document.removeEventListener('mousemove', handleMouseMoveHorizontal);
    document.removeEventListener('mousemove', handleMouseMoveRightVertical);
    document.removeEventListener('mouseup', stopResize);
  }
</script>

<style scoped>
  .layout {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }

  .pane-left {
    background-color: #f9f6fb;
    min-width: 200px;
    display: flex;
    flex-direction: column;
  }

  .pane-right {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .pane-right-top {
    padding: 10px;
    background-color: #f9f6fb;
    min-height: 100px;
  }

  .pane-right-bottom {
    padding: 10px;
    background-color: #f9f6fb;
    flex: 1;
  }

  .divider-vertical {
    width: 16px;
    background: linear-gradient(to right, #ccc, #eee, #ccc);
    cursor: col-resize;
    border-left: 1px solid #aaa;
    border-right: 1px solid #aaa;
  }

  .divider-horizontal {
    height: 16px;
    background: linear-gradient(to bottom, #ccc, #eee, #ccc);
    cursor: row-resize;
    border-top: 1px solid #aaa;
    border-bottom: 1px solid #aaa;
  }
</style>
