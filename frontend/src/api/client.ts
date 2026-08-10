import { gatewayConfig } from "../auth/authConfig";
import { tokenStorage } from "../auth/token-storage";
import type { ProblemDetails } from "./types";

let onUnauthorized: () => void = () => tokenStorage.clear();
export const setUnauthorizedHandler = (handler: () => void) => {
  onUnauthorized = handler;
};
export class ApiError extends Error {
  constructor(
    public problem: ProblemDetails,
    public retryAfter?: string,
  ) {
    super(problem.title);
  }
}
const safeMessage: Record<number, string> = {
  400: "The request could not be completed.",
  401: "Your session has expired. Please sign in again.",
  403: "You do not have permission to perform this action.",
  404: "The requested resource is unavailable.",
  409: "The request conflicts with the current resource state.",
  422: "Please review the submitted information.",
  429: "Too many requests. Please try again shortly.",
  500: "The service is temporarily unavailable.",
};
export const gatewayBaseUrl = `${gatewayConfig.url}${gatewayConfig.context}`;
export async function apiRequest<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  if (!path.startsWith("/")) throw new Error("API paths must be relative");
  const token = tokenStorage.token();
  if (!token) {
    onUnauthorized();
    throw new ApiError({ title: safeMessage[401], status: 401 });
  }
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  headers.set("Authorization", `Bearer ${token}`);
  if (init.body) headers.set("Content-Type", "application/json");
  const response = await fetch(`${gatewayBaseUrl}${path}`, {
    ...init,
    headers,
  });
  if (response.status === 401) onUnauthorized();
  if (!response.ok) {
    let body: Partial<ProblemDetails> = {};
    try {
      body = (await response.json()) as Partial<ProblemDetails>;
    } catch {
      /* safe fallback */
    }
    const status = response.status;
    throw new ApiError(
      {
        title: safeMessage[status] || "The request failed.",
        status,
        type: body.type,
        instance: body.instance,
        traceId: body.traceId,
      },
      response.headers.get("Retry-After") ?? undefined,
    );
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
