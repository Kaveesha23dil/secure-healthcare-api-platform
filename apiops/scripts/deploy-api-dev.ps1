$ErrorActionPreference = "Stop"
if ($env:WSO2_ENVIRONMENT -ne "development") { Write-Error "WSO2_ENVIRONMENT must be development"; exit 2 }
& (Join-Path $PSScriptRoot "deploy-api.ps1")
exit $LASTEXITCODE
