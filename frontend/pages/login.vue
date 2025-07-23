<template>
  <div class="login-page">
    <div class="login-card">
      <template v-if="!isAuthenticated">
        <Input v-model="inputLogin" label="Логин" placeholder="Введите логин" :error="errors.login" />
        <Input v-model="inputPassword" label="Пароль" placeholder="Введите пароль" :error="errors.password" />
        <Button @click="handleLogin" label="Войти" class="full-width" />
      </template>

      <template v-else>
        <p>Вы уже вошли в систему как {{ userName }}</p>
        <Button @click="logout" label="Выйти" class="full-width" />
      </template>

      <p v-if="errors.general" class="error-message">{{ errors.general }}</p>
    </div>
  </div>
</template>


<script setup lang="ts">
definePageMeta({
  layout: 'blank'
})
const { login: authLogin, logout, getUser, isAuthenticated, userName } = useAuth();

const inputLogin = ref('');
const inputPassword = ref('');

const errors = reactive({
  login: '',
  password: '',
  general: '',
});

async function handleLogin() {
  // Сброс ошибок
  errors.login = '';
  errors.password = '';
  errors.general = '';

  if (!inputLogin.value) {
    errors.login = 'Поле логин обязательно';
  }
  if (!inputPassword.value) {
    errors.password = 'Поле пароль обязательно';
  }

  if (errors.login || errors.password) return;

  const success = await authLogin(inputLogin.value, inputPassword.value);

  if (!success) {
    errors.general = 'Неверный логин или пароль';
  } else {
    await getUser();
    navigateTo('/');
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f5f7fa;
}

.login-card {
  background: white;
  border: 1px solid #ddd;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 320px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.error-message {
  color: #d93025;
  font-size: 13px;
  margin-top: 4px;
  text-align: center;
}
</style>
