$ErrorActionPreference = "Stop"
$base = if ($env:API_BASE_REF) { $env:API_BASE_REF } else { "origin/develop" }
python (Join-Path $PSScriptRoot "api_contract_checks.py") breaking --base $base
exit $LASTEXITCODE
