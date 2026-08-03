#!/usr/bin/env sh
set -eu
backend_url="${BACKEND_URL:-http://localhost:8000}"
for path in /health /ready; do
  status="$(curl --silent --show-error --output /tmp/healthcare-response.txt --write-out '%{http_code}' "${backend_url}${path}")"
  printf '%s -> HTTP %s\n' "$path" "$status"
  sed -n '1,20p' /tmp/healthcare-response.txt
  [ "$status" = "200" ] || exit 1
done
