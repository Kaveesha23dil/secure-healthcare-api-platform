import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  ApiError,
  apiRequest,
  gatewayBaseUrl,
  setUnauthorizedHandler,
} from "../api/client";
import { tokenStorage } from "../auth/token-storage";
describe("gateway API client", () => {
  beforeEach(() =>
    tokenStorage.set("test-access-token", {
      user: {
        subject: "patient-one",
        roles: ["patient"],
        scopes: ["doctor:read"],
      },
      expiresAt: Date.now() + 10000,
    }),
  );
  it("sends tokens only to the configured WSO2 gateway", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(
        new Response(JSON.stringify({ items: [] }), { status: 200 }),
      );
    await apiRequest("/api/v1/doctors");
    const [url, init] = fetchMock.mock.calls[0];
    expect(String(url)).toBe(`${gatewayBaseUrl}/api/v1/doctors`);
    expect(String(url)).not.toContain("localhost:8000");
    expect(new Headers(init?.headers).get("Authorization")).toBe(
      "Bearer test-access-token",
    );
  });
  it.each([403, 404, 409, 422, 429])(
    "maps HTTP %s to a safe typed error",
    async (status) => {
      vi.spyOn(globalThis, "fetch").mockResolvedValue(
        new Response(JSON.stringify({ title: "unsafe detail", status }), {
          status,
        }),
      );
      await expect(apiRequest("/api/v1/doctors")).rejects.toMatchObject({
        problem: { status },
      });
    },
  );
  it("clears authentication on 401", async () => {
    const handler = vi.fn();
    setUnauthorizedHandler(handler);
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(null, { status: 401 }),
    );
    await expect(apiRequest("/api/v1/doctors")).rejects.toBeInstanceOf(
      ApiError,
    );
    expect(handler).toHaveBeenCalled();
  });
});
