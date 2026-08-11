import type { APIRequestContext, APIResponse, Page } from "@playwright/test";

export const gatewayBase = `${process.env.E2E_GATEWAY_URL || "https://localhost:8243"}${process.env.E2E_API_CONTEXT || "/healthcare/1.0.0"}`;

export async function gatewayRequest(request: APIRequestContext, method: string, path: string, options: { token?: string; headers?: Record<string, string>; data?: unknown } = {}): Promise<APIResponse> {
  return request.fetch(`${gatewayBase}${path}`, {
    method,
    data: options.data,
    headers: { ...(options.token ? { Authorization: `Bearer ${options.token}` } : {}), ...options.headers },
    failOnStatusCode: false,
  });
}

export async function captureBearerToken(page: Page, trigger: () => Promise<void>): Promise<string> {
  const requestPromise = page.waitForRequest((request) => request.url().startsWith(gatewayBase) && request.headers()["authorization"]?.startsWith("Bearer "));
  await trigger();
  return (await requestPromise).headers()["authorization"].slice(7);
}
