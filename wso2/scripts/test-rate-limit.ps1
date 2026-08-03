$ErrorActionPreference = "Stop"
if ($env:CONFIRM_RATE_LIMIT_TEST -ne "true") { Write-Error "Set CONFIRM_RATE_LIMIT_TEST=true for a controlled non-production test"; exit 2 }
if (-not $env:WSO2_ACCESS_TOKEN) { Write-Error "WSO2_ACCESS_TOKEN is required"; exit 2 }
$gateway=if($env:WSO2_GATEWAY_URL){$env:WSO2_GATEWAY_URL.TrimEnd('/')}else{"https://localhost:8243"}; $context=if($env:WSO2_API_CONTEXT){$env:WSO2_API_CONTEXT}else{"/healthcare/1.0.0"}; $count=if($env:RATE_LIMIT_REQUEST_COUNT){[int]$env:RATE_LIMIT_REQUEST_COUNT}else{110}
$counts=@{success=0;rate_limited=0;other=0}
1..$count | ForEach-Object {
  $params=@{Uri="$gateway$context/api/v1/doctors";Headers=@{Authorization="Bearer $($env:WSO2_ACCESS_TOKEN)"};UseBasicParsing=$true}
  if($env:ALLOW_INSECURE_LOCAL_TLS -eq "true"){
    if($PSVersionTable.PSVersion.Major -lt 7){Write-Error "ALLOW_INSECURE_LOCAL_TLS requires PowerShell 7+";exit 2}
    $params.SkipCertificateCheck=$true
  }
  try{$status=[int](Invoke-WebRequest @params).StatusCode}catch{$status=if($_.Exception.Response){[int]$_.Exception.Response.StatusCode}else{0}}
  if($status -eq 429){$counts.rate_limited++}elseif($status -ge 200 -and $status -lt 300){$counts.success++}else{$counts.other++}
}
Write-Output "success=$($counts.success) rate_limited=$($counts.rate_limited) other=$($counts.other)"
if($counts.rate_limited -eq 0){exit 1}
