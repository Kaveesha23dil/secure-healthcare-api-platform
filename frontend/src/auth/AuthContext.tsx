import { createContext } from "react";
import type { AuthenticatedUser, UserRole } from "./auth-types";
export interface AuthContextValue {
  user: AuthenticatedUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login(returnTo?: string): Promise<void>;
  completeCallback(params: URLSearchParams): Promise<string>;
  logout(): void;
  getAccessToken(): string | null;
  hasRole(role: UserRole): boolean;
  hasAnyRole(roles: UserRole[]): boolean;
  hasScope(scope: string): boolean;
}
export const AuthContext = createContext<AuthContextValue | null>(null);
