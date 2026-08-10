from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = (
    "BEGIN " + "PRIVATE KEY",
    "BEGIN RSA " + "PRIVATE KEY",
    "access_" + "token=",
    "refresh_" + "token=",
    "client_" + "secret=",
    "consumer_" + "secret=",
    "AWS_" + "SECRET_ACCESS_KEY",
    "pass" + "word=",
)

result = subprocess.run(  # noqa: S603
    ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],  # noqa: S607
    cwd=ROOT,
    check=True,
    capture_output=True,
)
findings: list[str] = []
for relative_bytes in result.stdout.split(b"\0"):
    if not relative_bytes:
        continue
    relative = relative_bytes.decode()
    if relative.endswith((".example", ".env.example")):
        continue
    path = ROOT / relative
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for line in text.splitlines():
        lowered = line.lower()
        if any(marker in lowered for marker in ("placeholder", "temporary-token-not-saved")):
            continue
        if any(pattern.lower() in lowered for pattern in PATTERNS):
            findings.append(relative)
            break
if findings:
    print("Potential secret material detected in tracked files:")
    for finding in findings:
        print(f"- {finding}")
    raise SystemExit(1)
print("Tracked-file secret scan passed")
