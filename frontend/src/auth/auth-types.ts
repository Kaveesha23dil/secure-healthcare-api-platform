export type UserRole = "patient" | "doctor" | "administrator";
export interface AuthenticatedUser {
  subject: string;
  displayName?: string;
  email?: string;
  roles: UserRole[];
  scopes: string[];
}
export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  id_token?: string;
  scope?: string;
}
export interface AuthState {
  user: AuthenticatedUser;
  expiresAt: number;
}
