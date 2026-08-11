import { expect, test } from "@playwright/test";
import { authBlockReason, loginAs } from "../fixtures/auth";
import { fictionalDoctor } from "../fixtures/test-data";

test("@wso2 administrator views summaries and manages a fictional doctor", async ({ page }) => {
  test.skip(Boolean(authBlockReason("admin")), authBlockReason("admin"));
  await loginAs(page, "admin");
  await page.goto("/admin/appointments");
  await expect(page.getByRole("heading", { name: "All appointments" })).toBeVisible();
  await page.goto("/admin/patients");
  await expect(page.getByRole("heading", { name: "Patient summaries" })).toBeVisible();
  const doctor = fictionalDoctor();
  await page.goto("/admin/doctors");
  await page.getByLabel("Name").fill(doctor.displayName);
  await page.getByLabel("Specialization").fill(doctor.specialization);
  await page.getByLabel("Clinic").fill(doctor.clinicName);
  await page.getByRole("button", { name: "Create doctor" }).click();
  await expect(page.getByRole("heading", { name: doctor.displayName })).toBeVisible();
  const card = page.locator("article").filter({ hasText: doctor.displayName });
  page.once("dialog", (dialog) => dialog.accept());
  await card.getByRole("button", { name: "Deactivate doctor" }).click();
});
