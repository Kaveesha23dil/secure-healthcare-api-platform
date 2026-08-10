import { useLocation } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
export function LoginPage() {
  const auth = useAuth(),
    location = useLocation();
  const from = (location.state as { from?: string } | null)?.from || "/";
  return (
    <main className="login">
      <section className="panel">
        <p className="eyebrow">WSO2-secured access</p>
        <h1>Secure Healthcare Platform</h1>
        <p>
          Manage fictional appointments through a gateway-protected
          demonstration.
        </p>
        <button className="primary" onClick={() => void auth.login(from)}>
          Sign in with WSO2
        </button>
        <p className="muted">
          Credentials are entered only on the WSO2 authorization server.
        </p>
      </section>
    </main>
  );
}
