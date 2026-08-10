import { ApiError } from "../api/client";
const errorMessage = (error: unknown): string =>
  error instanceof ApiError
    ? error.problem.title
    : "The service is temporarily unavailable.";
export const ErrorAlert = ({ error }: { error: unknown }) => (
  <p role="alert" className="alert">
    {errorMessage(error)}
  </p>
);
