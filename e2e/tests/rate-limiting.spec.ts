import { expect, test } from "@playwright/test";
import { authBlockReason, loginAs } from "../fixtures/auth";

test("@wso2 rate limiting returns safe frontend guidance", async ({ page }) => {
  test.skip(process.env.E2E_RUN_RATE_LIMIT !== "true", "Opt in with E2E_RUN_RATE_LIMIT=true only in an isolated throttling test environment.");
  test.skip(Boolean(authBlockReason("patientOne")), authBlockReason("patientOne"));
  await loginAs(page, "patientOne");
  let limited = false;
  for (let i = 0; i < 25 && !limited; i += 1) {
    const responsePromise = page.waitForResponse((response) => response.url().includes("/api/v1/doctors"));
    await page.goto("/patient/doctors");
    limited = (await responsePromise).status() === 429;
  }
  expect(limited, "Configured WSO2 policy did not throttle within the conservative 25-request ceiling").toBe(true);
  await expect(page.getByText(/too many requests|try again shortly/i)).toBeVisible();
});
