import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { LoginPage } from "../pages/LoginPage";

const { login } = vi.hoisted(() => ({ login: vi.fn() }));
vi.mock("../auth/useAuth", () => ({ useAuth: () => ({ login }) }));

describe("Sign-in", () => {
  it("shows a rejected login error and allows another attempt", async () => {
    login.mockRejectedValueOnce(new Error("Sign-in is not configured."));
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>,
    );
    fireEvent.click(screen.getByRole("button", { name: "Sign in with WSO2" }));
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Sign-in is not configured.",
    );
    await waitFor(() => expect(screen.getByRole("button")).toBeEnabled());
  });

  it("prevents repeated clicks while login is starting", () => {
    login.mockReturnValueOnce(new Promise<void>(() => {}));
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>,
    );
    fireEvent.click(screen.getByRole("button", { name: "Sign in with WSO2" }));
    expect(
      screen.getByRole("button", { name: "Redirecting to WSO2…" }),
    ).toBeDisabled();
  });
});
