export type AppointmentStatus =
  "proposed" | "booked" | "checked-in" | "completed" | "cancelled" | "no-show";
export interface Page<T> {
  items: T[];
  page: number;
  size: number;
  totalItems: number;
  totalPages: number;
}
export interface DoctorSummary {
  id: string;
  displayName: string;
  specialization: string;
  clinicName: string;
}
export interface Doctor extends DoctorSummary {
  active: boolean;
}
export interface DoctorInput {
  displayName: string;
  specialization: string;
  clinicName: string;
}
export interface DoctorUpdate {
  displayName?: string;
  specialization?: string;
  clinicName?: string;
  active?: boolean;
}
export interface AvailabilitySlot {
  id: string;
  doctorId: string;
  startAt: string;
  endAt: string;
  available: boolean;
}
export interface CreateAvailabilitySlotRequest {
  startAt: string;
  endAt: string;
}
export interface Appointment {
  id: string;
  doctorId: string;
  slotId: string;
  startAt: string;
  endAt: string;
  reason: string;
  status: AppointmentStatus;
  createdAt: string;
  updatedAt: string;
}
export interface CreateAppointmentRequest {
  doctorId: string;
  slotId: string;
  reason: string;
}
export interface UpdateAppointmentRequest {
  status: AppointmentStatus;
}
export interface PatientSummary {
  id: string;
  displayName: string;
  maskedEmail: string;
  status: "active" | "disabled";
}
export interface ProblemDetails {
  type?: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  traceId?: string;
}
export interface HealthResponse {
  status: string;
}
