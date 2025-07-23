<template>
  <div>
    <FilterPanel />
    <div class="start-block">
      <Input v-model="phoneNumber" placeholder="Номер телефона" />
      <Button label="Начать" @click="startProcess" />
    </div>
    <LeadList />
  </div>
</template>

<script lang="ts" setup>
import FilterPanel from './FilterPanel.vue';

const phoneNumber = ref('');
const config = useRuntimeConfig();
const { accessToken } = useAuth();
const startProcess = () => {

  if (phoneNumber.value) {
    const url = `${config.public.apiBaseUrl}/services/process/start-main-process?phone=${phoneNumber.value}`;
    console.log(accessToken.value);
    fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${accessToken.value}`,
      }
    })
      .then(async (response) => {
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Ошибка: ${response.status} — ${errorText}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Процесс успешно запущен:', data);
        phoneNumber.value = '';
      })
      .catch(error => {
        console.error('Ошибка при запуске процесса:', error);
      });
  } else {
    console.error('Пожалуйста, введите номер телефона.');
  }
};
</script>

<style>
.start-block {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
