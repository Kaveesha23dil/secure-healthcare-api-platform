import { Link } from "react-router-dom";
export const DoctorDashboardPage = () => (
  <>
    <h1>Doctor dashboard</h1>
    <p>Use authorized appointment references and manage your own schedule.</p>
    <div className="cards">
      <Link className="card" to="/doctor/appointments">
        <h2>Appointments</h2>
        <p>View and update an assigned appointment.</p>
      </Link>
      <Link className="card" to="/doctor/availability">
        <h2>Availability</h2>
        <p>Manage schedule after resolving your doctor identity.</p>
      </Link>
    </div>
  </>
);
