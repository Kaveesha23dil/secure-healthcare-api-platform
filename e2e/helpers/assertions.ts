import { expect, type APIResponse, type Page } from "@playwright/test";
import { gatewayBase } from "./api";

export async function expectProblem(response: APIResponse, status: number): Promise<void> {
  expect(response.status()).toBe(status);
  expect(response.headers()["content-type"] || "").toContain("application/problem+json");
  const body = await response.json();
  expect(body).toMatchObject({ status });
  expect(JSON.stringify(body)).not.toMatch(/traceback|stack trace|password|bearer /i);
}

export function observeGatewayOnly(page: Page): string[] {
  const violations: string[] = [];
  page.on("request", (request) => {
    if (request.url().includes("/api/v1/") && !request.url().startsWith(gatewayBase)) violations.push(request.url());
  });
  return violations;
}
