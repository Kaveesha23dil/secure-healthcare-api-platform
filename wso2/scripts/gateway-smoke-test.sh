#!/usr/bin/env sh
set -eu
[ -n "${WSO2_ACCESS_TOKEN:-}" ] || { echo "WSO2_ACCESS_TOKEN is required" >&2; exit 2; }
gateway="${WSO2_GATEWAY_URL:-https://localhost:8243}"
context="${WSO2_API_CONTEXT:-/healthcare/1.0.0}"
tls=""
if [ "${ALLOW_INSECURE_LOCAL_TLS:-false}" = "true" ]; then tls="--insecure"; fi
output="$(mktemp)"; trap 'rm -f "$output"' EXIT
status="$(curl $tls --silent --show-error --output "$output" --write-out '%{http_code}' --header "Authorization: Bearer $WSO2_ACCESS_TOKEN" "$gateway$context/api/v1/doctors")"
printf 'Gateway list doctors -> HTTP %s\n' "$status"
sed -n '1,40p' "$output"
case "$status" in 2??) exit 0;; *) exit 1;; esac
