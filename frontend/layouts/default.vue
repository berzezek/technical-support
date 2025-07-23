<template>
  <div class="layout">
    <!-- Header -->
    <Header />

    <!-- Main Content Area -->
    <div class="main-wrapper" v-if="isAuthenticated">
      <slot />
    </div>
    <!-- Footer -->
    <!-- <footer class="footer">Футер</footer> -->
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f2f2f2;
}

.footer {
  height: 40px;
  background-color: #444;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>

<script setup lang="ts">
const { isAuthenticated } = useAuth();
</script>
