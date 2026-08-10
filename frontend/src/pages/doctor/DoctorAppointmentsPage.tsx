import { useState, type FormEvent } from "react";
import { getAppointment, updateAppointment } from "../../api/appointments";
import type { Appointment, AppointmentStatus } from "../../api/types";
import { AppointmentTable } from "../../components/AppointmentTable";
import { ErrorAlert } from "../../components/ErrorAlert";
const next: Partial<Record<AppointmentStatus, AppointmentStatus[]>> = {
  booked: ["checked-in", "cancelled", "no-show"],
  "checked-in": ["completed", "cancelled"],
};
export function DoctorAppointmentsPage() {
  const [id, setId] = useState(""),
    [item, setItem] = useState<Appointment>(),
    [error, setError] = useState<unknown>();
  async function load(event: FormEvent) {
    event.preventDefault();
    setError(undefined);
    try {
      setItem(await getAppointment(id));
    } catch (e) {
      setError(e);
    }
  }
  return (
    <>
      <h1>Assigned appointment</h1>
      <p className="notice">
        Backend gap: no doctor appointment-list endpoint exists. Enter an
        assigned appointment reference; FastAPI still enforces assignment.
      </p>
      <form className="inline" onSubmit={(e) => void load(e)}>
        <label>
          Appointment reference
          <input required value={id} onChange={(e) => setId(e.target.value)} />
        </label>
        <button>Load</button>
      </form>
      {error && <ErrorAlert error={error} />}{" "}
      {item && (
        <AppointmentTable
          items={[item]}
          action={(appointment, status) => {
            if (!(next[appointment.status] || []).includes(status)) return;
            void updateAppointment(appointment.id, { status })
              .then(setItem)
              .catch(setError);
          }}
        />
      )}
    </>
  );
}
