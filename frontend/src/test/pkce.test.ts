import { describe, expect, it } from "vitest";
import {
  createCodeChallenge,
  createCodeVerifier,
  secureRandom,
} from "../auth/pkce";
describe("PKCE", () => {
  it("creates secure verifier and state values", () => {
    expect(createCodeVerifier().length).toBeGreaterThanOrEqual(43);
    expect(secureRandom()).not.toEqual(secureRandom());
  });
  it("uses the RFC 7636 S256 transform", async () => {
    expect(
      await createCodeChallenge("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"),
    ).toBe("E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM");
  });
});
