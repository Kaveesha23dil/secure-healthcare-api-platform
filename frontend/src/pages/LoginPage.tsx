import { useLocation } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../auth/useAuth";
export function LoginPage() {
  const auth = useAuth(),
    location = useLocation();
  const from = (location.state as { from?: string } | null)?.from || "/";
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);
  async function signIn() {
    setError("");
    setPending(true);
    try {
      await auth.login(from);
    } catch (cause) {
      setError(
        cause instanceof Error
          ? cause.message
          : "Sign-in could not start. Please try again.",
      );
      setPending(false);
    }
  }
  return (
    <main className="login">
      <section className="panel">
        <p className="eyebrow">WSO2-secured access</p>
        <h1>Secure Healthcare Platform</h1>
        <p>
          Manage fictional appointments through a gateway-protected
          demonstration.
        </p>
        <button
          className="primary"
          disabled={pending}
          onClick={() => void signIn()}
        >
          {pending ? "Redirecting to WSO2…" : "Sign in with WSO2"}
        </button>
        {error && <p role="alert">{error}</p>}
        <p className="muted">
          Credentials are entered only on the WSO2 authorization server.
        </p>
      </section>
    </main>
  );
}
