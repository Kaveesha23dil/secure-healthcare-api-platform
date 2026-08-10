#!/usr/bin/env sh
set -eu
for name in WSO2_USERNAME WSO2_PASSWORD WSO2_ENVIRONMENT WSO2_HOST WSO2_GATEWAY_URL BACKEND_URL APICTL_API_PROJECT; do
  eval "value=\${$name:-}"
  [ -n "$value" ] || { echo "$name is required" >&2; exit 2; }
done
[ -e "$APICTL_API_PROJECT" ] || { echo 'APICTL_API_PROJECT does not exist' >&2; exit 2; }
if [ -n "${APICTL_PARAMS_FILE:-}" ]; then [ -e "$APICTL_PARAMS_FILE" ] || { echo 'APICTL_PARAMS_FILE does not exist' >&2; exit 2; }; fi
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
apictl_bin="${APICTL_HOME:+$APICTL_HOME/}apictl"
"$script_dir/validate-api.sh"
"$apictl_bin" add env "$WSO2_ENVIRONMENT" --apim "$WSO2_HOST"
"$apictl_bin" login "$WSO2_ENVIRONMENT" -u "$WSO2_USERNAME" -p "$WSO2_PASSWORD"
set -- import api -f "$APICTL_API_PROJECT" -e "$WSO2_ENVIRONMENT" --update
if [ -n "${APICTL_PARAMS_FILE:-}" ]; then set -- "$@" --params "$APICTL_PARAMS_FILE"; fi
"$apictl_bin" "$@"
printf 'SecureHealthcareAPI deployment completed for %s\n' "$WSO2_ENVIRONMENT"
