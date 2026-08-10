import { useCallback } from "react";
import { Link } from "react-router-dom";
import { listDoctors } from "../../api/doctors";
import { EmptyState } from "../../components/EmptyState";
import { ErrorAlert } from "../../components/ErrorAlert";
import { LoadingState } from "../../components/LoadingState";
import { useAsync } from "../../hooks/useAsync";
export function DoctorsPage() {
  const load = useCallback(() => listDoctors(), []),
    state = useAsync(load);
  return (
    <>
      <h1>Doctors</h1>
      {state.loading ? (
        <LoadingState />
      ) : state.error ? (
        <ErrorAlert error={state.error} />
      ) : !state.data?.items.length ? (
        <EmptyState>No doctors available.</EmptyState>
      ) : (
        <div className="cards">
          {state.data.items.map((doctor) => (
            <article className="card" key={doctor.id}>
              <h2>{doctor.displayName}</h2>
              <p>{doctor.specialization}</p>
              <p>{doctor.clinicName}</p>
              <Link to={`/patient/doctors/${doctor.id}`}>
                View details and availability
              </Link>
            </article>
          ))}
        </div>
      )}
    </>
  );
}
