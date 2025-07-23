import { useCookie, useRuntimeConfig, navigateTo, computed } from '#imports';
import type { Ref, ComputedRef } from '#imports';

export interface AuthContext {
  accessToken: Ref<string | null>;
  refreshToken: Ref<string | null>;
  userName: Ref<string | null>;
  groups: Ref<string[] | null>;
  isAuthenticated: ComputedRef<boolean>;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  getUser: () => Promise<void>;
  refresh: () => Promise<boolean>;
}

export const useAuth = (): AuthContext => {
  const accessToken = useCookie<string | null>('auth_token', {
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
  });

  const refreshToken = useCookie<string | null>('refresh_token', {
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
  });

  const userName = useCookie<string | null>('user_name', {
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
  });

  const groups = useCookie<string[] | null>('groups', {
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
  });

  const isAuthenticated = computed(() => !!accessToken.value);
  const config = useRuntimeConfig();

  async function login(email: string, password: string): Promise<boolean> {
    try {
      const { access_token, refresh_token } = await $fetch<{
        access_token: string;
        refresh_token: string;
      }>(`${config.public.apiBaseUrl}/services/auth/keycloak/login`, {
        method: 'POST',
        body: new URLSearchParams({ username: email, password }),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      accessToken.value = access_token;
      refreshToken.value = refresh_token;
      return true;
    } catch (error) {
      return false;
    }
  }

  async function getUser() {
    if (!accessToken.value) return;

    try {
      const user = await $fetch<{
        name: string;
        role: string;
        groups?: string[];
      }>(`${config.public.apiBaseUrl}/services/auth/keycloak/me`, {
        method: 'POST',
        body: new URLSearchParams({ access_token: accessToken.value }),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      userName.value = user.name;
      groups.value = user.groups || [];
    } catch (error) {
      console.error('Failed to fetch user data:', error);
    }
  }

  async function refresh(): Promise<boolean> {
    if (!refreshToken.value) return false;

    try {
      const { access_token, refresh_token } = await $fetch<{
        access_token: string;
        refresh_token: string;
      }>(`${config.public.apiBaseUrl}/services/auth/keycloak/refresh`, {
        method: 'POST',
        body: new URLSearchParams({ refresh_token: refreshToken.value }),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      accessToken.value = access_token;
      refreshToken.value = refresh_token;
      return true;
    } catch (e) {
      console.warn('[Auth] ❌ Ошибка обновления токена:', e);
      return false; // ❗ не вызываем logout()
    }
  }

  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    userName.value = null;
    groups.value = null;
    navigateTo('/login');
  }

  return {
    accessToken,
    refreshToken,
    userName,
    groups,
    isAuthenticated,
    login,
    logout,
    getUser,
    refresh,
  };
};
