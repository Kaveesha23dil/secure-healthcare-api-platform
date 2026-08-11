import type { Page } from "@playwright/test";

export async function cancelAppointmentIfPresent(page: Page, reason: string): Promise<void> {
  await page.goto("/patient/appointments");
  const row = page.getByRole("row").filter({ hasText: reason });
  if (await row.count()) {
    page.once("dialog", (dialog) => dialog.accept());
    await row.getByRole("button", { name: "Cancel" }).click();
  }
}
