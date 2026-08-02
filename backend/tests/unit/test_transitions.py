from app.services.appointment_service import TRANSITIONS


def test_transition_map_has_terminal_states() -> None:
    assert TRANSITIONS["completed"] == frozenset()
    assert TRANSITIONS["cancelled"] == frozenset()
    assert TRANSITIONS["no-show"] == frozenset()
    assert "checked-in" in TRANSITIONS["booked"]
