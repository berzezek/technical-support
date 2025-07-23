export default defineNuxtRouteMiddleware(async (to) => {
  const publicPages = ['/login', '/register'];
  if (publicPages.includes(to.path) || to.path.startsWith('/.well-known')) return;

  const accessToken = useCookie<string | null>('auth_token');
  const refreshToken = useCookie<string | null>('refresh_token');

  if (accessToken.value) return;

  if (refreshToken.value) {
    try {
      const config = useRuntimeConfig();
      const res = await $fetch<{ access_token: string; refresh_token?: string }>(
        `${config.public.apiBaseUrl}/api/auth/keycloak/refresh`,
        {
          method: 'POST',
          body: new URLSearchParams({ refresh_token: refreshToken.value }),
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }
      );

      accessToken.value = res.access_token;
      if (res.refresh_token) {
        refreshToken.value = res.refresh_token;
      }

      return;
    } catch (e) {
      console.warn('[Middleware] Не удалось обновить токен');
    }
  }

  // Просто редиректим без очистки
  return navigateTo('/login');
});
