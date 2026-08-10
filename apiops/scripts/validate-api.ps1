$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
python (Join-Path $PSScriptRoot "api_contract_checks.py") validate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output "OpenAPI validation passed"
