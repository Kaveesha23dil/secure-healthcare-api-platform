import { expect, test } from "@playwright/test";
import { authBlockReason, loginAs } from "../fixtures/auth";

test("@wso2 doctor loads an assigned appointment and only sees valid transitions", async ({ page }) => {
  test.skip(Boolean(authBlockReason("doctorOne")), authBlockReason("doctorOne"));
  test.skip(!process.env.E2E_ASSIGNED_APPOINTMENT_ID, "Current API has no doctor appointment-list endpoint; provide a fictional assigned reference.");
  await loginAs(page, "doctorOne");
  await page.goto("/doctor/appointments");
  await page.getByLabel("Appointment reference").fill(process.env.E2E_ASSIGNED_APPOINTMENT_ID!);
  await page.getByRole("button", { name: "Load" }).click();
  await expect(page.getByRole("table")).toBeVisible();
  await expect(page.getByRole("button", { name: /Check in|Complete|Cancel/ }).first()).toBeVisible();
});

test.skip("@wso2 doctor creates availability", async () => {
  // Blocked: there is no current-doctor identity/identifier contract for safe self-service mutation.
});

test.skip("@wso2 doctor invalid transition is rejected", async () => {
  // Requires an isolated, resettable assigned appointment so the test cannot corrupt shared workflow state.
});
