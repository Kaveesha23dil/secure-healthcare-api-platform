export const DoctorAvailabilityPage = () => (
  <>
    <h1>Doctor availability</h1>
    <p className="notice">
      Backend gap: the verified identity is mapped to a doctor internally, but
      the API exposes no current-doctor profile or safe doctor identifier claim
      contract. Schedule mutation is intentionally unavailable until that
      operation exists.
    </p>
  </>
);
