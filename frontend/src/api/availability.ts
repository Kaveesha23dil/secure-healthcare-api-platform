import { apiRequest } from "./client";
import type {
  AvailabilitySlot,
  CreateAvailabilitySlotRequest,
  Page,
} from "./types";
export const listAvailability = (doctorId: string) =>
  apiRequest<Page<AvailabilitySlot>>(
    `/api/v1/doctors/${encodeURIComponent(doctorId)}/availability?page=1&size=100`,
  );
export const createAvailability = (
  doctorId: string,
  input: CreateAvailabilitySlotRequest,
) =>
  apiRequest<AvailabilitySlot>(
    `/api/v1/doctors/${encodeURIComponent(doctorId)}/availability`,
    { method: "POST", body: JSON.stringify(input) },
  );
