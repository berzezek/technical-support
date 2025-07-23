// server/utils/getCamundaToken.ts
let token: string | null = null;
let tokenExpiresAt = 0;

// Define the RuntimeConfig type if not already imported
type RuntimeConfig = {
  zeebeAuthorizationServerUrl: string;
  zeebeClientId: string;
  zeebeClientSecret: string;
};

export async function getCamundaToken(runtimeConfig: RuntimeConfig) {
  const now = Date.now();
  if (token && tokenExpiresAt > now) {
    return token;
  }

  const { access_token, expires_in } = await $fetch<{ access_token: string, expires_in: number }>(
    runtimeConfig.zeebeAuthorizationServerUrl,
    {
      method: 'POST',
      body: new URLSearchParams({
        client_id: runtimeConfig.zeebeClientId,
        client_secret: runtimeConfig.zeebeClientSecret,
        grant_type: 'client_credentials',
        audience: 'tasklist.camunda.io',
      }),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  );

  token = access_token;
  tokenExpiresAt = now + expires_in * 1000 - 5000;
  return token;
}
