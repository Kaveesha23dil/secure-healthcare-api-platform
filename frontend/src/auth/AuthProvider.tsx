import { useCallback, useMemo, useState, type ReactNode } from "react";
import { setUnauthorizedHandler } from "../api/client";
import { AuthContext } from "./AuthContext";
import { authConfig } from "./authConfig";
import { beginLogin, completeLogin, dashboardFor } from "./oidc";
import { tokenStorage } from "./token-storage";
import type { AuthenticatedUser, UserRole } from "./auth-types";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthenticatedUser | null>(
    tokenStorage.state()?.user ?? null,
  );
  const clear = useCallback(() => {
    tokenStorage.clear();
    setUser(null);
  }, []);
  setUnauthorizedHandler(clear);
  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user && tokenStorage.token()),
      isLoading: false,
      login: beginLogin,
      async completeCallback(params: URLSearchParams) {
        const result = await completeLogin(params);
        tokenStorage.set(result.tokens.access_token, {
          user: result.user,
          expiresAt: Date.now() + result.tokens.expires_in * 1000,
        });
        setUser(result.user);
        return result.returnTo === "/"
          ? dashboardFor(result.user.roles)
          : result.returnTo;
      },
      logout() {
        clear();
        const url = new URL(authConfig.logoutUrl);
        url.searchParams.set(
          "post_logout_redirect_uri",
          authConfig.postLogoutRedirectUri,
        );
        window.location.assign(url);
      },
      getAccessToken: tokenStorage.token,
      hasRole: (role: UserRole) => user?.roles.includes(role) ?? false,
      hasAnyRole: (roles: UserRole[]) =>
        roles.some((role) => user?.roles.includes(role)),
      hasScope: (scope: string) => user?.scopes.includes(scope) ?? false,
    }),
    [clear, user],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
