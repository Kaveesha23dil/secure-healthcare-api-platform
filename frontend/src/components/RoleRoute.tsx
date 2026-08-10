import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
import type { UserRole } from "../auth/auth-types";
export function RoleRoute({ roles }: { roles: UserRole[] }) {
  return useAuth().hasAnyRole(roles) ? (
    <Outlet />
  ) : (
    <Navigate to="/unauthorized" replace />
  );
}
