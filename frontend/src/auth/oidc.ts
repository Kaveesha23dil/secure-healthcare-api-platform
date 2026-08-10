import { authConfig } from "./authConfig";
import { createCodeChallenge, createCodeVerifier, secureRandom } from "./pkce";
import type { AuthenticatedUser, TokenResponse, UserRole } from "./auth-types";

const TX = "oauth_transaction";
export async function beginLogin(returnTo = "/"): Promise<void> {
  const verifier = createCodeVerifier();
  const state = secureRandom();
  const nonce = secureRandom();
  sessionStorage.setItem(
    TX,
    JSON.stringify({ verifier, state, nonce, returnTo }),
  );
  const url = new URL(authConfig.authorizationUrl);
  url.search = new URLSearchParams({
    response_type: "code",
    client_id: authConfig.clientId,
    redirect_uri: authConfig.redirectUri,
    scope: authConfig.scopes.join(" "),
    state,
    nonce,
    code_challenge: await createCodeChallenge(verifier),
    code_challenge_method: "S256",
  }).toString();
  window.location.assign(url);
}
const decode = (token: string): Record<string, unknown> => {
  const parts = token.split(".");
  if (parts.length !== 3) throw new Error("Invalid ID token structure");
  const encoded = parts[1].replace(/-/g, "+").replace(/_/g, "/");
  return JSON.parse(
    atob(encoded.padEnd(Math.ceil(encoded.length / 4) * 4, "=")),
  ) as Record<string, unknown>;
};
const strings = (value: unknown): string[] =>
  Array.isArray(value)
    ? value.filter((x): x is string => typeof x === "string")
    : typeof value === "string"
      ? value.split(/[ ,]+/).filter(Boolean)
      : [];
export function userFromTokens(
  tokens: TokenResponse,
  expectedNonce: string,
): AuthenticatedUser {
  if (!tokens.id_token)
    throw new Error("WSO2 must return an ID token for UI identity");
  const claims = decode(tokens.id_token);
  if (typeof claims.sub !== "string")
    throw new Error("ID token subject is missing");
  const audience = Array.isArray(claims.aud) ? claims.aud : [claims.aud];
  if (!audience.includes(authConfig.clientId))
    throw new Error("ID token audience is invalid");
  if (typeof claims.exp !== "number" || claims.exp * 1000 <= Date.now())
    throw new Error("ID token is expired");
  if (claims.nonce !== expectedNonce)
    throw new Error("ID token nonce is invalid");
  const allowed: UserRole[] = ["patient", "doctor", "administrator"];
  const roles = strings(
    claims.roles ?? claims["http://wso2.org/claims/role"],
  ).filter((x): x is UserRole => allowed.includes(x as UserRole));
  return {
    subject: claims.sub,
    displayName: typeof claims.name === "string" ? claims.name : undefined,
    email: typeof claims.email === "string" ? claims.email : undefined,
    roles,
    scopes: strings(tokens.scope ?? claims.scope),
  };
}
export async function completeLogin(params: URLSearchParams): Promise<{
  tokens: TokenResponse;
  user: AuthenticatedUser;
  returnTo: string;
}> {
  const raw = sessionStorage.getItem(TX);
  sessionStorage.removeItem(TX);
  if (!raw) throw new Error("Authorization transaction is missing or expired");
  const tx = JSON.parse(raw) as {
    verifier?: string;
    state?: string;
    nonce?: string;
    returnTo?: string;
  };
  const code = params.get("code"),
    state = params.get("state");
  if (!code) throw new Error("Authorization code is missing");
  if (!state || state !== tx.state || !tx.verifier || !tx.nonce)
    throw new Error("Authorization state validation failed");
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    client_id: authConfig.clientId,
    redirect_uri: authConfig.redirectUri,
    code,
    code_verifier: tx.verifier,
  });
  const response = await fetch(authConfig.tokenUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    },
    body,
  });
  if (!response.ok) throw new Error("Authorization code exchange failed");
  const tokens = (await response.json()) as TokenResponse;
  if (!tokens.access_token || tokens.token_type.toLowerCase() !== "bearer")
    throw new Error("Invalid token response");
  return {
    tokens,
    user: userFromTokens(tokens, tx.nonce),
    returnTo: tx.returnTo || "/",
  };
}
export const dashboardFor = (roles: UserRole[]): string =>
  roles.includes("administrator")
    ? "/admin/dashboard"
    : roles.includes("doctor")
      ? "/doctor/dashboard"
      : roles.includes("patient")
        ? "/patient/dashboard"
        : "/unauthorized";
