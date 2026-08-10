$ErrorActionPreference = "Stop"
& (Join-Path $PSScriptRoot "..\..\wso2\scripts\gateway-smoke-test.ps1")
exit $LASTEXITCODE
