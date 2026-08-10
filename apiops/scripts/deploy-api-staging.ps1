$ErrorActionPreference = "Stop"
if ($env:WSO2_ENVIRONMENT -ne "staging") { Write-Error "WSO2_ENVIRONMENT must be staging"; exit 2 }
if ($env:CONFIRM_STAGING_DEPLOY -ne "true") { Write-Error "CONFIRM_STAGING_DEPLOY=true is required"; exit 2 }
& (Join-Path $PSScriptRoot "deploy-api.ps1")
exit $LASTEXITCODE
