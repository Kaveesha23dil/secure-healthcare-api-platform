$ErrorActionPreference = "Stop"
$required = @("WSO2_USERNAME", "WSO2_PASSWORD", "WSO2_ENVIRONMENT", "WSO2_HOST", "WSO2_GATEWAY_URL", "BACKEND_URL", "APICTL_API_PROJECT")
foreach ($name in $required) {
    if (-not [Environment]::GetEnvironmentVariable($name)) { Write-Error "$name is required"; exit 2 }
}
if (-not (Test-Path -LiteralPath $env:APICTL_API_PROJECT)) { Write-Error "APICTL_API_PROJECT does not exist"; exit 2 }
if ($env:APICTL_PARAMS_FILE -and -not (Test-Path -LiteralPath $env:APICTL_PARAMS_FILE)) { Write-Error "APICTL_PARAMS_FILE does not exist"; exit 2 }
$apictl = if ($env:APICTL_HOME) { Join-Path $env:APICTL_HOME "apictl.exe" } else { "apictl" }
& (Join-Path $PSScriptRoot "validate-api.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $apictl add env $env:WSO2_ENVIRONMENT --apim $env:WSO2_HOST
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $apictl login $env:WSO2_ENVIRONMENT -u $env:WSO2_USERNAME -p $env:WSO2_PASSWORD
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$arguments = @("import", "api", "-f", $env:APICTL_API_PROJECT, "-e", $env:WSO2_ENVIRONMENT, "--update")
if ($env:APICTL_PARAMS_FILE) { $arguments += @("--params", $env:APICTL_PARAMS_FILE) }
& $apictl @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output "SecureHealthcareAPI deployment completed for $($env:WSO2_ENVIRONMENT)"
