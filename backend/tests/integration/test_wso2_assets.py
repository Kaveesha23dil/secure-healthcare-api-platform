from pathlib import Path

import yaml

ROOT = Path(__file__).parents[3]
METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}


def load(relative: str) -> dict[str, object]:
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def operations(document: dict[str, object]) -> dict[tuple[str, str], dict[str, object]]:
    return {
        (path, method): operation
        for path, path_item in document["paths"].items()
        for method, operation in path_item.items()
        if method in METHODS
    }


def test_wso2_contract_preserves_paths_operations_and_resolves_refs() -> None:
    source = load("api-spec/healthcare-api.yaml")
    wso2 = load("wso2/api/healthcare-api-wso2.yaml")
    source_operations = operations(source)
    wso2_operations = operations(wso2)
    assert set(wso2_operations) == set(source_operations)
    assert "/ready" not in wso2["paths"]
    assert wso2["paths"]["/health"]["get"]["security"] == []
    operation_ids = [operation["operationId"] for operation in wso2_operations.values()]
    assert len(operation_ids) == len(set(operation_ids))
    assert operation_ids == [operation["operationId"] for operation in source_operations.values()]
    text = (ROOT / "wso2/api/healthcare-api-wso2.yaml").read_text(encoding="utf-8")
    assert text.count("\n  schemas:") == 1
    references: list[str] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "$ref":
                    references.append(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(wso2)
    for reference in references:
        current = wso2
        for part in reference.removeprefix("#/").split("/"):
            current = current[part.replace("~1", "/").replace("~0", "~")]


def test_scope_and_resource_mappings_match_contract() -> None:
    wso2 = load("wso2/api/healthcare-api-wso2.yaml")
    declared = {item["name"] for item in load("wso2/config/scopes.yaml")["scopes"]}
    oauth_scopes = set(
        wso2["components"]["securitySchemes"]["oauth2"]["flows"]["authorizationCode"]["scopes"]
    )
    assert declared == oauth_scopes
    mappings = load("wso2/config/api-resource-scope-mapping.yaml")["resources"]
    operations_by_key = operations(wso2)
    assert {(item["path"], item["method"].lower()) for item in mappings} == set(operations_by_key)
    for item in mappings:
        operation = operations_by_key[(item["path"], item["method"].lower())]
        if item.get("authentication") == "none":
            assert operation["security"] == []
        else:
            required = {scope for entry in operation["security"] for scope in entry["oauth2"]}
            assert item["scope"] in required
