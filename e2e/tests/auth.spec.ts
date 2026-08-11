import { expect, test } from "@playwright/test";
import { authBlockReason, loginAs } from "../fixtures/auth";

test("@ci unauthenticated users are redirected from protected routes", async ({ page }) => {
  await page.goto("/patient/appointments");
  await expect(page).toHaveURL(/\/login$/);
  await expect(page.getByRole("button", { name: "Sign in with WSO2" })).toBeVisible();
});

for (const value of [
  { role: "patientOne" as const, heading: "Patient dashboard" },
  { role: "doctorOne" as const, heading: "Doctor dashboard" },
  { role: "admin" as const, heading: "Administrator dashboard" },
]) {
  test(`@wso2 ${value.role} authenticates with WSO2 and reaches its dashboard`, async ({ page }) => {
    test.skip(Boolean(authBlockReason(value.role)), authBlockReason(value.role));
    await loginAs(page, value.role);
    await expect(page.getByRole("heading", { name: value.heading })).toBeVisible();
  });
}

test("@wso2 patient cannot open the administrator route", async ({ page }) => {
  test.skip(Boolean(authBlockReason("patientOne")), authBlockReason("patientOne"));
  await loginAs(page, "patientOne");
  await page.goto("/admin/dashboard");
  await expect(page).toHaveURL(/\/unauthorized$/);
});
