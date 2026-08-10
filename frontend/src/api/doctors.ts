import { apiRequest } from "./client";
import type {
  Doctor,
  DoctorInput,
  DoctorSummary,
  DoctorUpdate,
  Page,
} from "./types";
export const listDoctors = (page = 1, specialization = "") =>
  apiRequest<Page<DoctorSummary>>(
    `/api/v1/doctors?page=${page}&size=20${specialization ? `&specialization=${encodeURIComponent(specialization)}` : ""}`,
  );
export const getDoctor = (id: string) =>
  apiRequest<Doctor>(`/api/v1/doctors/${encodeURIComponent(id)}`);
export const createDoctor = (input: DoctorInput) =>
  apiRequest<Doctor>("/api/v1/doctors", {
    method: "POST",
    body: JSON.stringify(input),
  });
export const updateDoctor = (id: string, input: DoctorUpdate) =>
  apiRequest<Doctor>(`/api/v1/doctors/${encodeURIComponent(id)}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
export const deactivateDoctor = (id: string) =>
  apiRequest<void>(`/api/v1/doctors/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
