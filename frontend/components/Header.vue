<template>
  <header class="header">
    <button class="menu-toggle" @click="isMenuOpen = !isMenuOpen">
      ☰ Меню
    </button>

    <div class="nav" :class="{ open: isMenuOpen }">
      <NuxtLink to="/">Главное</NuxtLink>
      <NuxtLink to="/">Контактные лица</NuxtLink>
      <NuxtLink to="/">Работа с заявками</NuxtLink>
      <NuxtLink to="/">Приемка</NuxtLink>
      <NuxtLink to="/">Администрация</NuxtLink>
      <NuxtLink to="/">Департамент снабжения</NuxtLink>
      <NuxtLink to="/">Отчеты</NuxtLink>
      <NuxtLink to="/">Параметры приложения</NuxtLink>
    </div>

    <div class="user" :class="{ open: isMenuOpen }">
      <span class="username"><span class="role-title">{{role}}</span> {{ userName }}</span>
    </div>
  </header>
</template>

<script setup lang="ts">
  const { userName, role } = useAuth();
  const isMenuOpen = ref(false);
</script>

<style scoped>
  .header {
    background-color: #f9f9f9;
    border-bottom: 1px solid #ddd;
    padding: 0 16px;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 8px;
    position: relative;
  }

  /* кнопка меню */
  .menu-toggle {
    display: none;
    background: none;
    border: none;
    font-size: 16px;
    cursor: pointer;
    padding: 8px 0;
  }

  .nav,
  .user {
    display: flex;
    align-items: flex-end;
    gap: 12px;
  }

  .nav a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.2s;
    padding-bottom: 4px;
  }

  .nav a:hover {
    color: #007bff;
  }

  .username {
    color: #333;
    padding-bottom: 4px;
  }

  .role-title {
    font-weight: bold;
    color: #555;
    margin-right: 4px;
  }

  /* адаптивное поведение */
  @media (max-width: 1080px) {
    .header {
      flex-direction: column;
      align-items: flex-start;
      height: auto;
      padding: 12px 16px;
    }

    .menu-toggle {
      display: block;
      margin-bottom: 8px;
    }

    .nav,
    .user {
      display: none;
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
      width: 100%;
    }

    .nav.open,
    .user.open {
      display: flex;
    }

    .nav a {
      width: 100%;
    }
  }
</style>
