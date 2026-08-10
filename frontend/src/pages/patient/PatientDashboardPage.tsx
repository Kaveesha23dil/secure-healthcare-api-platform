import { Link } from "react-router-dom";
import { useAuth } from "../../auth/useAuth";
export function PatientDashboardPage() {
  return (
    <>
      <h1>Welcome, {useAuth().user?.displayName || "patient"}</h1>
      <p>Browse clinicians and manage only your own appointments.</p>
      <div className="cards">
        <Link className="card" to="/patient/doctors">
          <h2>Find a doctor</h2>
          <p>View specialties and available times.</p>
        </Link>
        <Link className="card" to="/patient/appointments">
          <h2>My appointments</h2>
          <p>Review or cancel eligible bookings.</p>
        </Link>
      </div>
    </>
  );
}
