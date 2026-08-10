import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
    env: {
      VITE_WSO2_AUTHORIZATION_URL:
        "https://identity.example.test/oauth2/authorize",
      VITE_WSO2_TOKEN_URL: "https://identity.example.test/oauth2/token",
      VITE_WSO2_LOGOUT_URL: "https://identity.example.test/oidc/logout",
      VITE_WSO2_CLIENT_ID: "public-test-client",
      VITE_WSO2_GATEWAY_URL: "https://gateway.example.test",
      VITE_WSO2_API_CONTEXT: "/healthcare/1.0.0",
      VITE_OAUTH_REDIRECT_URI: "http://localhost:5173/auth/callback",
      VITE_OAUTH_POST_LOGOUT_REDIRECT_URI: "http://localhost:5173/login",
      VITE_OAUTH_SCOPES: "openid profile doctor:read",
    },
  },
});
