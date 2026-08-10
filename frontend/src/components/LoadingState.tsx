export const LoadingState = ({ label = "Loading…" }: { label?: string }) => (
  <p role="status" className="state">
    {label}
  </p>
);
