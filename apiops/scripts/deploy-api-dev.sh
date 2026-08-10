#!/usr/bin/env sh
set -eu
[ "${WSO2_ENVIRONMENT:-}" = development ] || { echo 'WSO2_ENVIRONMENT must be development' >&2; exit 2; }
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "$script_dir/deploy-api.sh"
