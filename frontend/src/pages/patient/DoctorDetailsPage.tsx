import { useCallback, useState, type FormEvent } from "react";
import { useParams } from "react-router-dom";
import { ApiError } from "../../api/client";
import { createAppointment } from "../../api/appointments";
import { listAvailability } from "../../api/availability";
import { getDoctor } from "../../api/doctors";
import { EmptyState } from "../../components/EmptyState";
import { ErrorAlert } from "../../components/ErrorAlert";
import { LoadingState } from "../../components/LoadingState";
import { useAsync } from "../../hooks/useAsync";
import { formatDate } from "../../utils/dates";
export function DoctorDetailsPage() {
  const { doctorId = "" } = useParams(),
    loadDoctor = useCallback(() => getDoctor(doctorId), [doctorId]),
    loadSlots = useCallback(() => listAvailability(doctorId), [doctorId]),
    doctor = useAsync(loadDoctor),
    slots = useAsync(loadSlots),
    [slotId, setSlotId] = useState(""),
    [reason, setReason] = useState(""),
    [message, setMessage] = useState("");
  async function book(event: FormEvent) {
    event.preventDefault();
    setMessage("");
    try {
      await createAppointment({ doctorId, slotId, reason });
      setMessage("Appointment booked successfully.");
      slots.reload();
    } catch (error) {
      setMessage(
        error instanceof ApiError && error.problem.status === 409
          ? "This appointment slot is no longer available. Please choose another time."
          : error instanceof ApiError
            ? error.problem.title
            : "Booking failed.",
      );
      if (error instanceof ApiError && error.problem.status === 409)
        slots.reload();
    }
  }
  if (doctor.loading) return <LoadingState />;
  if (doctor.error || !doctor.data) return <ErrorAlert error={doctor.error} />;
  return (
    <>
      <h1>{doctor.data.displayName}</h1>
      <p>
        {doctor.data.specialization} · {doctor.data.clinicName}
      </p>
      <h2>Available appointments</h2>
      {slots.loading ? (
        <LoadingState />
      ) : slots.error ? (
        <ErrorAlert error={slots.error} />
      ) : !slots.data?.items.length ? (
        <EmptyState>No available time slots.</EmptyState>
      ) : (
        <form className="panel form" onSubmit={(event) => void book(event)}>
          <label>
            Appointment time
            <select
              required
              value={slotId}
              onChange={(e) => setSlotId(e.target.value)}
            >
              <option value="">Select a time</option>
              {slots.data.items
                .filter((x) => x.available)
                .map((slot) => (
                  <option key={slot.id} value={slot.id}>
                    {formatDate(slot.startAt)}
                  </option>
                ))}
            </select>
          </label>
          <label>
            Reason
            <textarea
              required
              maxLength={500}
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            />
          </label>
          <button className="primary" type="submit">
            Book appointment
          </button>
          {message && <p aria-live="polite">{message}</p>}
        </form>
      )}
    </>
  );
}
