import { useCallback, useState, type FormEvent } from "react";
import {
  createDoctor,
  deactivateDoctor,
  listDoctors,
  updateDoctor,
} from "../../api/doctors";
import { EmptyState } from "../../components/EmptyState";
import { ErrorAlert } from "../../components/ErrorAlert";
import { LoadingState } from "../../components/LoadingState";
import { useAsync } from "../../hooks/useAsync";
export function AdminDoctorsPage() {
  const load = useCallback(() => listDoctors(), []),
    state = useAsync(load),
    [error, setError] = useState<unknown>();
  async function create(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    try {
      await createDoctor({
        displayName: String(form.get("displayName")),
        specialization: String(form.get("specialization")),
        clinicName: String(form.get("clinicName")),
      });
      event.currentTarget.reset();
      state.reload();
    } catch (e) {
      setError(e);
    }
  }
  return (
    <>
      <h1>Manage doctors</h1>
      <form className="panel form" onSubmit={(e) => void create(e)}>
        <h2>Add fictional doctor</h2>
        <label>
          Name
          <input name="displayName" required maxLength={120} />
        </label>
        <label>
          Specialization
          <input name="specialization" required maxLength={100} />
        </label>
        <label>
          Clinic
          <input name="clinicName" required maxLength={160} />
        </label>
        <button className="primary">Create doctor</button>
      </form>
      {error && <ErrorAlert error={error} />}{" "}
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
              <button
                onClick={() => {
                  const clinicName = window.prompt(
                    "Updated clinic name",
                    doctor.clinicName,
                  );
                  if (clinicName)
                    void updateDoctor(doctor.id, { clinicName })
                      .then(state.reload)
                      .catch(setError);
                }}
              >
                Edit clinic
              </button>
              <button
                className="danger"
                onClick={() => {
                  if (window.confirm("Deactivate this doctor?"))
                    void deactivateDoctor(doctor.id)
                      .then(state.reload)
                      .catch(setError);
                }}
              >
                Deactivate doctor
              </button>
            </article>
          ))}
        </div>
      )}
    </>
  );
}
