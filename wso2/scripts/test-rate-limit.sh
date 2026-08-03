#!/usr/bin/env sh
set -eu
[ "${CONFIRM_RATE_LIMIT_TEST:-false}" = "true" ] || { echo "Set CONFIRM_RATE_LIMIT_TEST=true for a controlled non-production test" >&2; exit 2; }
[ -n "${WSO2_ACCESS_TOKEN:-}" ] || { echo "WSO2_ACCESS_TOKEN is required" >&2; exit 2; }
gateway="${WSO2_GATEWAY_URL:-https://localhost:8243}"; context="${WSO2_API_CONTEXT:-/healthcare/1.0.0}"; count="${RATE_LIMIT_REQUEST_COUNT:-110}"; insecure=""
[ "${ALLOW_INSECURE_LOCAL_TLS:-false}" = "true" ] && insecure="--insecure"
ok=0; limited=0; other=0; i=1
while [ "$i" -le "$count" ]; do
  status="$(curl $insecure --silent --output /dev/null --write-out '%{http_code}' --header "Authorization: Bearer $WSO2_ACCESS_TOKEN" "$gateway$context/api/v1/doctors")"
  case "$status" in 2??) ok=$((ok+1));; 429) limited=$((limited+1));; *) other=$((other+1));; esac
  i=$((i+1))
done
printf 'success=%s rate_limited=%s other=%s\n' "$ok" "$limited" "$other"
[ "$limited" -gt 0 ] || exit 1
