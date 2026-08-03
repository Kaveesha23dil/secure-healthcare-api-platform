$ErrorActionPreference = "Stop"
if (-not $env:WSO2_ACCESS_TOKEN) { Write-Error "WSO2_ACCESS_TOKEN is required"; exit 2 }
$gateway = if ($env:WSO2_GATEWAY_URL) { $env:WSO2_GATEWAY_URL.TrimEnd('/') } else { "https://localhost:8243" }
$context = if ($env:WSO2_API_CONTEXT) { $env:WSO2_API_CONTEXT } else { "/healthcare/1.0.0" }
$params = @{ Uri="$gateway$context/api/v1/doctors"; Headers=@{Authorization="Bearer $($env:WSO2_ACCESS_TOKEN)"}; UseBasicParsing=$true }
if ($env:ALLOW_INSECURE_LOCAL_TLS -eq "true") {
    if ($PSVersionTable.PSVersion.Major -lt 7) { Write-Error "ALLOW_INSECURE_LOCAL_TLS requires PowerShell 7+"; exit 2 }
    $params.SkipCertificateCheck = $true
}
try { $response = Invoke-WebRequest @params; $status = [int]$response.StatusCode; $content = $response.Content }
catch { $status = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { 0 }; $content = $_.ErrorDetails.Message }
Write-Output "Gateway list doctors -> HTTP $status"
Write-Output $content
if ($status -lt 200 -or $status -ge 300) { exit 1 }
