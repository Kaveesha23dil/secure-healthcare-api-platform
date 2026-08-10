import { apiRequest } from "./client";
import type { Appointment, Page } from "./types";
export const listMyAppointments = () =>
  apiRequest<Page<Appointment>>(
    "/api/v1/patients/me/appointments?page=1&size=100",
  );
