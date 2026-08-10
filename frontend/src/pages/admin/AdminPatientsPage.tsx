import { useCallback } from "react";
import { listAdminPatients } from "../../api/admin";
import { EmptyState } from "../../components/EmptyState";
import { ErrorAlert } from "../../components/ErrorAlert";
import { LoadingState } from "../../components/LoadingState";
import { useAsync } from "../../hooks/useAsync";
export function AdminPatientsPage() {
  const load = useCallback(() => listAdminPatients(), []),
    state = useAsync(load);
  return (
    <>
      <h1>Patient summaries</h1>
      {state.loading ? (
        <LoadingState />
      ) : state.error ? (
        <ErrorAlert error={state.error} />
      ) : !state.data?.items.length ? (
        <EmptyState>No patients found.</EmptyState>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Masked email</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {state.data.items.map((patient) => (
                <tr key={patient.id}>
                  <td>{patient.displayName}</td>
                  <td>{patient.maskedEmail}</td>
                  <td>{patient.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
