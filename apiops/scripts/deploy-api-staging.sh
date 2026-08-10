#!/usr/bin/env sh
set -eu
[ "${WSO2_ENVIRONMENT:-}" = staging ] || { echo 'WSO2_ENVIRONMENT must be staging' >&2; exit 2; }
[ "${CONFIRM_STAGING_DEPLOY:-}" = true ] || { echo 'CONFIRM_STAGING_DEPLOY=true is required' >&2; exit 2; }
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "$script_dir/deploy-api.sh"
