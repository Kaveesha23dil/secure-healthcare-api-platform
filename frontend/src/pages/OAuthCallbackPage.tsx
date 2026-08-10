import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
import { LoadingState } from "../components/LoadingState";
export function OAuthCallbackPage() {
  const auth = useAuth(),
    navigate = useNavigate(),
    started = useRef(false),
    [error, setError] = useState("");
  useEffect(() => {
    if (started.current) return;
    started.current = true;
    void auth
      .completeCallback(new URLSearchParams(window.location.search))
      .then((to) => navigate(to, { replace: true }))
      .catch(() =>
        setError(
          "Authentication could not be completed. Please return to sign in.",
        ),
      );
  }, [auth, navigate]);
  return (
    <main className="login">
      {error ? (
        <section className="panel">
          <h1>Sign-in failed</h1>
          <p role="alert">{error}</p>
          <a href="/login">Return to sign in</a>
        </section>
      ) : (
        <LoadingState label="Completing secure sign-in…" />
      )}
    </main>
  );
}
