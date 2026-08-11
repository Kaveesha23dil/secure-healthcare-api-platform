import { expect, test } from "@playwright/test";
import { authBlockReason, loginAs } from "../fixtures/auth";
import { fictionalReason } from "../fixtures/test-data";
import { cancelAppointmentIfPresent } from "../helpers/cleanup";
import { observeGatewayOnly } from "../helpers/assertions";

test.describe("@wso2 patient workflow", () => {
  test.beforeEach(async ({ page }) => {
    test.skip(Boolean(authBlockReason("patientOne")), authBlockReason("patientOne"));
    await loginAs(page, "patientOne");
  });

  test("browses doctors and all API traffic uses the WSO2 gateway", async ({ page }) => {
    const directBackendRequests = observeGatewayOnly(page);
    await page.goto("/patient/doctors");
    await expect(page.getByRole("heading", { name: "Doctors" })).toBeVisible();
    await expect(page.getByRole("link", { name: /View details and availability/ }).first()).toBeVisible();
    expect(directBackendRequests).toEqual([]);
  });

  test("books and cancels an appointment without supplying a patient ID", async ({ page }) => {
    const reason = fictionalReason();
    await page.goto("/patient/doctors");
    await page.getByRole("link", { name: /View details and availability/ }).first().click();
    await page.getByLabel("Appointment time").selectOption({ index: 1 });
    await page.getByLabel("Reason").fill(reason);
    const booking = page.waitForRequest((request) => request.method() === "POST" && request.url().includes("/api/v1/appointments"));
    await page.getByRole("button", { name: "Book appointment" }).click();
    expect((await booking).postDataJSON()).not.toHaveProperty("patientId");
    await expect(page.getByText("Appointment booked successfully.")).toBeVisible();
    await page.goto("/patient/appointments");
    await expect(page.getByRole("row").filter({ hasText: reason })).toBeVisible();
    await cancelAppointmentIfPresent(page, reason);
  });
});
