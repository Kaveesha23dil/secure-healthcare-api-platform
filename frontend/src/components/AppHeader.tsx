import { NavLink } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
import type { UserRole } from "../auth/auth-types";
const links: Record<UserRole, [string, string][]> = {
  patient: [
    ["Dashboard", "/patient/dashboard"],
    ["Doctors", "/patient/doctors"],
    ["Appointments", "/patient/appointments"],
  ],
  doctor: [
    ["Dashboard", "/doctor/dashboard"],
    ["Appointments", "/doctor/appointments"],
    ["Availability", "/doctor/availability"],
  ],
  administrator: [
    ["Dashboard", "/admin/dashboard"],
    ["Doctors", "/admin/doctors"],
    ["Appointments", "/admin/appointments"],
    ["Patients", "/admin/patients"],
  ],
};
export function AppHeader({ role }: { role: UserRole }) {
  const auth = useAuth();
  return (
    <header>
      <div>
        <strong>Secure Healthcare</strong>
        <span className="role">{role}</span>
      </div>
      <nav aria-label="Main navigation">
        {links[role].map(([label, path]) => (
          <NavLink key={path} to={path}>
            {label}
          </NavLink>
        ))}
      </nav>
      <div>
        <span>{auth.user?.displayName || "Signed-in user"}</span>
        <button onClick={auth.logout}>Sign out</button>
      </div>
    </header>
  );
}
