import { expect, test } from "@playwright/test";
import { authBlockReason, loginAs } from "../fixtures/auth";
import { captureBearerToken, gatewayRequest } from "../helpers/api";
import { expectProblem } from "../helpers/assertions";

test("@wso2 missing token is rejected by the gateway", async ({ request }) => {
  test.skip(process.env.E2E_RUN_WSO2 !== "true", "Requires the real WSO2 gateway.");
  await expectProblem(await gatewayRequest(request, "GET", "/api/v1/patients/me/appointments"), 401);
});

test("@wso2 forged identity and role headers do not grant administrator access", async ({ request }) => {
  test.skip(process.env.E2E_RUN_WSO2 !== "true", "Requires the real WSO2 gateway.");
  const response = await gatewayRequest(request, "GET", "/api/v1/admin/appointments", {
    headers: { "X-User-Id": "forged-admin", "X-Roles": "administrator", "X-Scopes": "admin:manage appointment:read:all" },
  });
  expect([401, 403]).toContain(response.status());
});

test("@wso2 patient cannot read another patient's appointment", async ({ page, request }) => {
  test.skip(Boolean(authBlockReason("patientOne")), authBlockReason("patientOne"));
  const target = process.env.E2E_UNASSIGNED_APPOINTMENT_ID;
  test.skip(!target, "Set E2E_UNASSIGNED_APPOINTMENT_ID to fictional data owned by patient two.");
  await loginAs(page, "patientOne");
  const token = await captureBearerToken(page, () => page.goto("/patient/appointments").then(() => undefined));
  expect((await gatewayRequest(request, "GET", `/api/v1/appointments/${target}`, { token })).status()).toBe(404);
});

test("@wso2 doctor cannot read an unassigned appointment", async ({ page, request }) => {
  test.skip(Boolean(authBlockReason("doctorOne")), authBlockReason("doctorOne"));
  const target = process.env.E2E_UNASSIGNED_APPOINTMENT_ID;
  test.skip(!target, "Set E2E_UNASSIGNED_APPOINTMENT_ID to an appointment assigned to another doctor.");
  await loginAs(page, "doctorOne");
  const token = await captureBearerToken(page, () => page.goto("/doctor/appointments").then(async () => {
    const assigned = process.env.E2E_ASSIGNED_APPOINTMENT_ID;
    if (!assigned) throw new Error("E2E_ASSIGNED_APPOINTMENT_ID is required to capture a gateway bearer request");
    await page.getByLabel("Appointment reference").fill(assigned);
    await page.getByRole("button", { name: "Load" }).click();
  }));
  expect((await gatewayRequest(request, "GET", `/api/v1/appointments/${target}`, { token })).status()).toBe(404);
});

test("@wso2 response carries a non-secret request ID", async ({ page }) => {
  test.skip(Boolean(authBlockReason("patientOne")), authBlockReason("patientOne"));
  await loginAs(page, "patientOne");
  const responsePromise = page.waitForResponse((response) => response.url().includes("/api/v1/doctors"));
  await page.goto("/patient/doctors");
  const id = (await responsePromise).headers()["x-request-id"];
  expect(id).toMatch(/^[A-Za-z0-9._:-]{8,64}$/);
});

test.skip("@wso2 valid identity without required scope receives 403", async () => {
  // Execution awaits a WSO2 limited-scope identity whose claims still satisfy the backend identity contract.
});
