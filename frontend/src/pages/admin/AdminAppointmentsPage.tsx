import { useCallback } from "react";
import { listAdminAppointments } from "../../api/admin";
import { AppointmentTable } from "../../components/AppointmentTable";
import { EmptyState } from "../../components/EmptyState";
import { ErrorAlert } from "../../components/ErrorAlert";
import { LoadingState } from "../../components/LoadingState";
import { useAsync } from "../../hooks/useAsync";
export function AdminAppointmentsPage() {
  const load = useCallback(() => listAdminAppointments(), []),
    state = useAsync(load);
  return (
    <>
      <h1>All appointments</h1>
      {state.loading ? (
        <LoadingState />
      ) : state.error ? (
        <ErrorAlert error={state.error} />
      ) : !state.data?.items.length ? (
        <EmptyState>No appointments found.</EmptyState>
      ) : (
        <AppointmentTable items={state.data.items} />
      )}
    </>
  );
}
