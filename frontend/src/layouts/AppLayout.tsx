import { Outlet } from "react-router-dom";
import { AppHeader } from "../components/AppHeader";
import type { UserRole } from "../auth/auth-types";
export function AppLayout({ role }: { role: UserRole }) {
  return (
    <>
      <AppHeader role={role} />
      <main>
        <Outlet />
      </main>
    </>
  );
}
