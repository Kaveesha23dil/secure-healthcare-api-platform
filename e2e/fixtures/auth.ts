import { expect, type Page } from "@playwright/test";
import { credentialsFor, realWso2Enabled, type TestRole } from "./users";

const destinations: Record<Exclude<TestRole, "limited">, RegExp> = {
  patientOne: /\/patient\/dashboard/,
  patientTwo: /\/patient\/dashboard/,
  doctorOne: /\/doctor\/dashboard/,
  doctorTwo: /\/doctor\/dashboard/,
  admin: /\/admin\/dashboard/,
};

export function authBlockReason(role: TestRole): string | undefined {
  if (!realWso2Enabled) return "Set E2E_RUN_WSO2=true to run against an available WSO2 environment.";
  if (!credentialsFor(role)) return `Missing credentials for ${role}; configure the matching E2E_* environment variables.`;
}

export async function loginAs(page: Page, role: Exclude<TestRole, "limited">): Promise<void> {
  const credentials = credentialsFor(role);
  if (!credentials) throw new Error(`Missing credentials for ${role}`);
  await page.goto("/login");
  await page.getByRole("button", { name: "Sign in with WSO2" }).click();
  await page.locator('input[name="username"], input[id="username"]').first().fill(credentials.username);
  await page.locator('input[name="password"], input[id="password"]').first().fill(credentials.password);
  await page.locator('button[type="submit"], input[type="submit"]').first().click();
  await expect(page).toHaveURL(destinations[role]);
}
