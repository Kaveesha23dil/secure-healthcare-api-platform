$ErrorActionPreference = "Stop"
$backendUrl = if ($env:BACKEND_URL) { $env:BACKEND_URL.TrimEnd('/') } else { "http://localhost:8000" }
foreach ($path in @("/health", "/ready")) {
    try {
        $response = Invoke-WebRequest -Uri "$backendUrl$path" -UseBasicParsing
        Write-Output "$path -> HTTP $($response.StatusCode)"
        Write-Output $response.Content
        if ($response.StatusCode -ne 200) { exit 1 }
    } catch {
        Write-Error "Backend check failed for ${path}: $($_.Exception.Message)"
        exit 1
    }
}
