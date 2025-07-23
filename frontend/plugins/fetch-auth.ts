// plugins/fetch-auth.ts
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.hook('app:created', () => {
    const originalFetch = globalThis.$fetch;

    const customFetch = async (...args: Parameters<typeof globalThis.$fetch>) => {
      try {
        return await originalFetch(...args);
      } catch (err: any) {
        if (err?.response?.status === 401) {
          const { refresh, logout } = useAuth();

          const ok = await refresh();
          if (!ok) logout();
        }

        throw err; // пробрасываем ошибку дальше
      }
    };

    // Copy 'raw' and 'create' properties from originalFetch
    customFetch.raw = originalFetch.raw;
    customFetch.create = originalFetch.create;

    globalThis.$fetch = customFetch as typeof globalThis.$fetch;
  });
});
