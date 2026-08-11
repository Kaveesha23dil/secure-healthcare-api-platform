export type TestRole = "patientOne" | "patientTwo" | "doctorOne" | "doctorTwo" | "admin" | "limited";
export type Credentials = { username: string; password: string };

const prefixes: Record<TestRole, string> = {
  patientOne: "E2E_PATIENT_ONE",
  patientTwo: "E2E_PATIENT_TWO",
  doctorOne: "E2E_DOCTOR_ONE",
  doctorTwo: "E2E_DOCTOR_TWO",
  admin: "E2E_ADMIN",
  limited: "E2E_LIMITED",
};

export function credentialsFor(role: TestRole): Credentials | undefined {
  const prefix = prefixes[role];
  const username = process.env[`${prefix}_USERNAME`];
  const password = process.env[`${prefix}_PASSWORD`];
  return username && password ? { username, password } : undefined;
}

export const realWso2Enabled = process.env.E2E_RUN_WSO2 === "true";
