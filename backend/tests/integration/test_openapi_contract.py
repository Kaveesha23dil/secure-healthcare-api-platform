from fastapi.testclient import TestClient


def test_generated_paths_and_operation_ids_match_contract(client: TestClient) -> None:
    generated = client.get("/openapi.json").json()
    expected = {
        ("/health", "get", "getHealth"),
        ("/api/v1/doctors", "get", "listDoctors"),
        ("/api/v1/doctors", "post", "createDoctor"),
        ("/api/v1/doctors/{doctorId}", "get", "getDoctor"),
        ("/api/v1/doctors/{doctorId}", "patch", "updateDoctor"),
        ("/api/v1/doctors/{doctorId}", "delete", "deleteDoctor"),
        ("/api/v1/doctors/{doctorId}/availability", "get", "listDoctorAvailability"),
        ("/api/v1/doctors/{doctorId}/availability", "post", "createDoctorAvailability"),
        ("/api/v1/appointments", "post", "createAppointment"),
        ("/api/v1/appointments/{appointmentId}", "get", "getAppointment"),
        ("/api/v1/appointments/{appointmentId}", "patch", "updateAppointment"),
        ("/api/v1/patients/me/appointments", "get", "listMyAppointments"),
        ("/api/v1/admin/appointments", "get", "listAllAppointments"),
        ("/api/v1/admin/patients", "get", "listPatients"),
    }
    actual = {
        (p, m, o["operationId"])
        for p, item in generated["paths"].items()
        for m, o in item.items()
        if m in {"get", "post", "patch", "delete"} and p != "/ready"
    }
    assert actual == expected
    assert generated["paths"]["/health"]["get"].get("security") in (None, [])
    assert generated["paths"]["/api/v1/doctors"]["get"]["security"] == [{"oauth2": ["doctor:read"]}]
    assert generated["paths"]["/api/v1/admin/appointments"]["get"]["security"] == [
        {"oauth2": ["appointment:read:all", "admin:manage"]}
    ]
