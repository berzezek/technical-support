// server/api/camunda/tasks.get.ts
import { getCamundaToken } from '~/server/utils/getCamundaToken';

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();

  const runtimeConfig = {
    zeebeAuthorizationServerUrl: config.zeebeAuthorizationServerUrl,
    zeebeClientId: config.zeebeClientId,
    zeebeClientSecret: config.zeebeClientSecret,
  };

  const tasklistBaseUrl = config.public.tasklistBaseUrl;

  let token = await getCamundaToken(runtimeConfig);

  try {
    const data = await $fetch(`${tasklistBaseUrl}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return data;
  } catch (err: any) {
    if (err?.response?.status === 401) {
      console.warn('[Tasklist] 401 — получаем новый токен и повторяем запрос');

      token = await getCamundaToken(runtimeConfig);

      return await $fetch(`${tasklistBaseUrl}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
    }

    console.error('[Tasklist] Ошибка:', err);
    throw createError({ statusCode: 500, statusMessage: 'Camunda Tasklist fetch error' });
  }
});
