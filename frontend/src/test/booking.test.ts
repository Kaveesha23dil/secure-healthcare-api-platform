import { describe, expect, it, vi } from "vitest";
import { createAppointment } from "../api/appointments";
import { tokenStorage } from "../auth/token-storage";
describe("patient booking security", () => {
  it("never sends an editable patient identity", async () => {
    tokenStorage.set("token", {
      user: {
        subject: "patient",
        roles: ["patient"],
        scopes: ["appointment:create"],
      },
      expiresAt: Date.now() + 1000,
    });
    const mock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(
        new Response(JSON.stringify({ id: "a" }), { status: 201 }),
      );
    await createAppointment({
      doctorId: "doctor",
      slotId: "slot",
      reason: "Fictional consultation",
    });
    const body = JSON.parse(String(mock.mock.calls[0][1]?.body)) as Record<
      string,
      unknown
    >;
    expect(body).toEqual({
      doctorId: "doctor",
      slotId: "slot",
      reason: "Fictional consultation",
    });
    expect(body).not.toHaveProperty("patientId");
  });
});
