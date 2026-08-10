#!/usr/bin/env sh
set -eu
script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python "$script_dir/api_contract_checks.py" breaking --base "${API_BASE_REF:-origin/develop}"
