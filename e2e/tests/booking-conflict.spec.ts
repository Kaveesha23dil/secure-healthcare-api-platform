import { expect, test } from "@playwright/test";
import { authBlockReason, loginAs } from "../fixtures/auth";
import { gatewayRequest } from "../helpers/api";
import { expectProblem } from "../helpers/assertions";

test("@wso2 duplicate booking is rejected without exposing raw gateway details", async ({ page, request }) => {
  test.skip(Boolean(authBlockReason("patientOne")), authBlockReason("patientOne"));
  await loginAs(page, "patientOne");
  await page.goto("/patient/doctors");
  await page.getByRole("link", { name: /View details and availability/ }).first().click();
  const option = page.getByLabel("Appointment time").locator("option").nth(1);
  test.skip(!(await option.count()), "No fictional available slot exists in this environment.");
  await page.getByLabel("Appointment time").selectOption(await option.getAttribute("value") || "");
  await page.getByLabel("Reason").fill(`E2E duplicate ${Date.now()}`);
  const firstPromise = page.waitForResponse((r) => r.url().endsWith("/api/v1/appointments") && r.request().method() === "POST");
  await page.getByRole("button", { name: "Book appointment" }).click();
  const first = await firstPromise;
  expect(first.status()).toBe(201);
  const authorization = first.request().headers()["authorization"];
  const duplicate = await gatewayRequest(request, "POST", "/api/v1/appointments", {
    token: authorization.slice(7),
    data: first.request().postDataJSON(),
  });
  await expectProblem(duplicate, 409);
  await expect(page.getByText("Appointment booked successfully.")).toBeVisible();
});

test.skip("@wso2 concurrent two-patient booking", async () => {
  // Requires a deterministic shared-slot seed/orchestration hook; database concurrency is covered by Pytest.
});
