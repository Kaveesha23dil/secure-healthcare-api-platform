import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { AuthContext, type AuthContextValue } from "../auth/AuthContext";
import type { UserRole } from "../auth/auth-types";
import { RoleRoute } from "../components/RoleRoute";
const context = (role: UserRole): AuthContextValue => ({
  user: { subject: "test", roles: [role], scopes: [] },
  isAuthenticated: true,
  isLoading: false,
  login: vi.fn(),
  completeCallback: vi.fn(),
  logout: vi.fn(),
  getAccessToken: () => "token",
  hasRole: (value) => value === role,
  hasAnyRole: (values) => values.includes(role),
  hasScope: () => false,
});
function renderRoute(role: UserRole, expected: UserRole) {
  render(
    <AuthContext.Provider value={context(role)}>
      <MemoryRouter initialEntries={["/protected"]}>
        <Routes>
          <Route element={<RoleRoute roles={[expected]} />}>
            <Route path="/protected" element={<p>Allowed</p>} />
          </Route>
          <Route path="/unauthorized" element={<p>Unauthorized</p>} />
        </Routes>
      </MemoryRouter>
    </AuthContext.Provider>,
  );
}
describe("role UX routes", () => {
  it("allows the matching patient route", () => {
    renderRoute("patient", "patient");
    expect(screen.getByText("Allowed")).toBeInTheDocument();
  });
  it("blocks a patient from administrator routes", () => {
    renderRoute("patient", "administrator");
    expect(screen.getByText("Unauthorized")).toBeInTheDocument();
  });
  it("allows doctors and administrators only in their areas", () => {
    renderRoute("doctor", "doctor");
    expect(screen.getByText("Allowed")).toBeInTheDocument();
  });
});
