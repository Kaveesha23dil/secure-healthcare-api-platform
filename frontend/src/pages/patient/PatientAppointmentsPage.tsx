import { useCallback, useState } from "react";
import { updateAppointment } from "../../api/appointments";
import { listMyAppointments } from "../../api/patients";
import { AppointmentTable } from "../../components/AppointmentTable";
import { EmptyState } from "../../components/EmptyState";
import { ErrorAlert } from "../../components/ErrorAlert";
import { LoadingState } from "../../components/LoadingState";
import { useAsync } from "../../hooks/useAsync";
export function PatientAppointmentsPage() {
  const load = useCallback(() => listMyAppointments(), []),
    state = useAsync(load),
    [actionError, setActionError] = useState<unknown>();
  return (
    <>
      <h1>My appointments</h1>
      {actionError && <ErrorAlert error={actionError} />}{" "}
      {state.loading ? (
        <LoadingState />
      ) : state.error ? (
        <ErrorAlert error={state.error} />
      ) : !state.data?.items.length ? (
        <EmptyState>No appointments found.</EmptyState>
      ) : (
        <AppointmentTable
          items={state.data.items}
          action={(item, status) => {
            if (
              status !== "cancelled" ||
              !window.confirm("Cancel this appointment?")
            )
              return;
            void updateAppointment(item.id, { status })
              .then(state.reload)
              .catch(setActionError);
          }}
        />
      )}
    </>
  );
}
