const required = (name: keyof ImportMetaEnv): string => {
  const value = import.meta.env[name];
  if (!value) throw new Error(`Missing frontend configuration: ${name}`);
  return value;
};
export const authConfig = {
  appName: import.meta.env.VITE_APP_NAME || "Secure Healthcare Platform",
  authorizationUrl: required("VITE_WSO2_AUTHORIZATION_URL"),
  tokenUrl: required("VITE_WSO2_TOKEN_URL"),
  logoutUrl: required("VITE_WSO2_LOGOUT_URL"),
  clientId: required("VITE_WSO2_CLIENT_ID"),
  redirectUri: required("VITE_OAUTH_REDIRECT_URI"),
  postLogoutRedirectUri: required("VITE_OAUTH_POST_LOGOUT_REDIRECT_URI"),
  scopes: required("VITE_OAUTH_SCOPES").split(/\s+/).filter(Boolean),
};
export const gatewayConfig = {
  url: required("VITE_WSO2_GATEWAY_URL").replace(/\/$/, ""),
  context: required("VITE_WSO2_API_CONTEXT").replace(/\/$/, ""),
};
