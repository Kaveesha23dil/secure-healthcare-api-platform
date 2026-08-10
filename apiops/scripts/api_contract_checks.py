from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
EXPECTED_SCOPES = {
    item["name"]
    for item in yaml.safe_load((ROOT / "wso2/config/scopes.yaml").read_text(encoding="utf-8"))[
        "scopes"
    ]
}


def load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: document must be a mapping")
    return value


def operations(document: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (path, method): operation
        for path, item in document.get("paths", {}).items()
        for method, operation in item.items()
        if method in METHODS
    }


def resolve_refs(document: dict[str, Any]) -> None:
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "$ref":
                    if not isinstance(child, str) or not child.startswith("#/"):
                        raise ValueError(f"unsupported reference: {child}")
                    current: Any = document
                    for part in child[2:].split("/"):
                        current = current[part.replace("~1", "/").replace("~0", "~")]
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(document)


def validate() -> None:
    source = load(ROOT / "api-spec/healthcare-api.yaml")
    gateway = load(ROOT / "wso2/api/healthcare-api-wso2.yaml")
    for name, document in (("source", source), ("gateway", gateway)):
        if not str(document.get("openapi", "")).startswith("3."):
            raise ValueError(f"{name}: OpenAPI 3.x is required")
        info = document.get("info", {})
        if not info.get("title") or not info.get("version"):
            raise ValueError(f"{name}: info.title and info.version are required")
        ids = [op.get("operationId") for op in operations(document).values()]
        if any(not item for item in ids) or len(ids) != len(set(ids)):
            raise ValueError(f"{name}: operationId values must be present and unique")
        resolve_refs(document)
    text = (ROOT / "wso2/api/healthcare-api-wso2.yaml").read_text(encoding="utf-8")
    if text.count("\n  schemas:") != 1:
        raise ValueError("gateway: exactly one components.schemas section is required")
    if "/ready" in gateway.get("paths", {}):
        raise ValueError("gateway: /ready must not be exposed")
    if gateway["paths"]["/health"]["get"].get("security") != []:
        raise ValueError("gateway: /health must remain public")
    if gateway.get("x-wso2-basePath") != "/healthcare/1.0.0":
        raise ValueError("gateway: context/version must remain /healthcare/1.0.0")
    if "/api/v1/api/v1" in text:
        raise ValueError("gateway: duplicated API base path detected")
    declared = set(
        gateway["components"]["securitySchemes"]["oauth2"]["flows"]["authorizationCode"]["scopes"]
    )
    if declared != EXPECTED_SCOPES:
        raise ValueError("gateway: OAuth scope set differs from the approved mapping")
    for (path, method), operation in operations(gateway).items():
        if path == "/health":
            continue
        scopes = {
            scope for item in operation.get("security", []) for scope in item.get("oauth2", [])
        }
        if not scopes:
            raise ValueError(f"gateway: protected operation {method.upper()} {path} has no scope")
    secret_markers = (
        "BEGIN " + "PRIVATE KEY",
        "access_" + "token=",
        "refresh_" + "token=",
        "client_" + "secret=",
        "consumer_" + "secret=",
    )
    if any(marker.lower() in text.lower() for marker in secret_markers):
        raise ValueError("gateway: possible secret value detected")
    print("API contracts validated")


def from_git(ref: str, path: str) -> dict[str, Any]:
    result = subprocess.run(  # noqa: S603
        ["git", "show", f"{ref}:{path}"],  # noqa: S607
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return yaml.safe_load(result.stdout)


def breaking(base: str) -> None:
    path = "api-spec/healthcare-api.yaml"
    old, new = from_git(base, path), load(ROOT / path)
    old_ops, new_ops = operations(old), operations(new)
    errors = [
        f"removed operation {method.upper()} {route}"
        for route, method in sorted(set(old_ops) - set(new_ops))
    ]
    for key in set(old_ops) & set(new_ops):
        before, after = old_ops[key], new_ops[key]
        if before.get("operationId") != after.get("operationId"):
            errors.append(f"changed operationId for {key[1].upper()} {key[0]}")
        old_success = {code for code in before.get("responses", {}) if str(code).startswith("2")}
        new_success = {code for code in after.get("responses", {}) if str(code).startswith("2")}
        if old_success - new_success:
            errors.append(f"removed success response for {key[1].upper()} {key[0]}")
    old_schemas = old.get("components", {}).get("schemas", {})
    new_schemas = new.get("components", {}).get("schemas", {})
    for name in set(old_schemas) & set(new_schemas):
        before, after = old_schemas[name], new_schemas[name]
        old_props, new_props = before.get("properties", {}), after.get("properties", {})
        removed_required = set(before.get("required", [])) & (set(old_props) - set(new_props))
        if removed_required:
            fields = sorted(removed_required)
            errors.append(f"removed required response/model properties from {name}: {fields}")
        added_required = set(after.get("required", [])) - set(before.get("required", []))
        if added_required:
            errors.append(f"new required fields in {name}: {sorted(added_required)}")
        for prop in set(old_props) & set(new_props):
            for attribute in ("type", "format"):
                if old_props[prop].get(attribute) != new_props[prop].get(attribute):
                    errors.append(f"changed {attribute} of {name}.{prop}")
    old_scopes = set(
        old["components"]["securitySchemes"]["oauth2"]["flows"]["authorizationCode"]["scopes"]
    )
    new_scopes = set(
        new["components"]["securitySchemes"]["oauth2"]["flows"]["authorizationCode"]["scopes"]
    )
    if old_scopes - new_scopes:
        errors.append(f"removed OAuth scopes: {sorted(old_scopes - new_scopes)}")
    if errors:
        print("Potential breaking API changes:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"No covered breaking changes detected against {base}")


parser = argparse.ArgumentParser()
parser.add_argument("command", choices=("validate", "breaking"))
parser.add_argument("--base", default="origin/develop")
args = parser.parse_args()
validate()
if args.command == "breaking":
    breaking(args.base)
