import { apiRequest } from "./client";
import type { Appointment, Page, PatientSummary } from "./types";
export const listAdminAppointments = () =>
  apiRequest<Page<Appointment>>("/api/v1/admin/appointments?page=1&size=100");
export const listAdminPatients = () =>
  apiRequest<Page<PatientSummary>>("/api/v1/admin/patients?page=1&size=100");
