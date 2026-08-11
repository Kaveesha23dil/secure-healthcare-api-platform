import { defineConfig, devices } from "@playwright/test";
import dotenv from "dotenv";
import path from "node:path";

dotenv.config({ path: path.resolve(__dirname, ".env") });

const frontendUrl = process.env.E2E_FRONTEND_URL || "http://127.0.0.1:5173";
const gatewayUrl = process.env.E2E_GATEWAY_URL || "https://localhost:8243";
const context = process.env.E2E_API_CONTEXT || "/healthcare/1.0.0";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : undefined,
  timeout: 60_000,
  expect: { timeout: 10_000 },
  outputDir: "test-results",
  reporter: [["list"], ["html", { open: "never" }], ["junit", { outputFile: "test-results/junit.xml" }]],
  use: {
    baseURL: frontendUrl,
    ignoreHTTPSErrors: process.env.E2E_IGNORE_HTTPS_ERRORS !== "false",
    screenshot: "only-on-failure",
    trace: "on-first-retry",
    video: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: process.env.E2E_SKIP_WEBSERVER === "true" ? undefined : {
    command: "npm --prefix ../frontend run dev -- --host 127.0.0.1",
    url: frontendUrl,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
    env: {
      VITE_WSO2_AUTHORIZATION_URL: process.env.E2E_WSO2_AUTHORIZATION_URL || "https://localhost:9443/oauth2/authorize",
      VITE_WSO2_TOKEN_URL: process.env.E2E_WSO2_TOKEN_URL || "https://localhost:9443/oauth2/token",
      VITE_WSO2_LOGOUT_URL: process.env.E2E_WSO2_LOGOUT_URL || "https://localhost:9443/oidc/logout",
      VITE_WSO2_CLIENT_ID: process.env.E2E_WSO2_CLIENT_ID || "e2e-public-client",
      VITE_OAUTH_REDIRECT_URI: `${frontendUrl}/auth/callback`,
      VITE_OAUTH_POST_LOGOUT_REDIRECT_URI: `${frontendUrl}/login`,
      VITE_OAUTH_SCOPES: process.env.E2E_OAUTH_SCOPES || "openid profile roles",
      VITE_WSO2_GATEWAY_URL: gatewayUrl,
      VITE_WSO2_API_CONTEXT: context,
    },
  },
});
