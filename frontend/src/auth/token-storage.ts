import type { AuthState } from "./auth-types";
let accessToken: string | null = null;
let authState: AuthState | null = null;
export const tokenStorage = {
  set(token: string, state: AuthState) {
    accessToken = token;
    authState = state;
  },
  token: () => accessToken,
  state: () => authState,
  clear() {
    accessToken = null;
    authState = null;
    sessionStorage.removeItem("oauth_transaction");
  },
};
