import { describe, expect, it } from "vitest";
import { completeLogin } from "../auth/oidc";
import { tokenStorage } from "../auth/token-storage";
describe("OIDC callback", () => {
  it("rejects a mismatched state and clears the transaction", async () => {
    sessionStorage.setItem(
      "oauth_transaction",
      JSON.stringify({ verifier: "verifier", state: "expected" }),
    );
    await expect(
      completeLogin(new URLSearchParams("code=secret-code&state=wrong")),
    ).rejects.toThrow("state validation");
    expect(sessionStorage.getItem("oauth_transaction")).toBeNull();
  });
  it("rejects a missing authorization code", async () => {
    sessionStorage.setItem(
      "oauth_transaction",
      JSON.stringify({ verifier: "verifier", state: "expected" }),
    );
    await expect(
      completeLogin(new URLSearchParams("state=expected")),
    ).rejects.toThrow("code is missing");
  });
  it("clears authentication and transaction state on logout cleanup", () => {
    tokenStorage.set("token", {
      user: { subject: "test", roles: ["patient"], scopes: [] },
      expiresAt: Date.now() + 1000,
    });
    sessionStorage.setItem("oauth_transaction", "temporary");
    tokenStorage.clear();
    expect(tokenStorage.token()).toBeNull();
    expect(sessionStorage.getItem("oauth_transaction")).toBeNull();
  });
});
