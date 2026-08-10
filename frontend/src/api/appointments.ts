import { apiRequest } from "./client";
import type {
  Appointment,
  CreateAppointmentRequest,
  UpdateAppointmentRequest,
} from "./types";
export const createAppointment = (input: CreateAppointmentRequest) =>
  apiRequest<Appointment>("/api/v1/appointments", {
    method: "POST",
    body: JSON.stringify(input),
    headers: { "Idempotency-Key": crypto.randomUUID() },
  });
export const getAppointment = (id: string) =>
  apiRequest<Appointment>(`/api/v1/appointments/${encodeURIComponent(id)}`);
export const updateAppointment = (
  id: string,
  input: UpdateAppointmentRequest,
) =>
  apiRequest<Appointment>(`/api/v1/appointments/${encodeURIComponent(id)}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
