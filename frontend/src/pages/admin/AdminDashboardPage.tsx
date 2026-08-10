import { Link } from "react-router-dom";
export const AdminDashboardPage = () => (
  <>
    <h1>Administrator dashboard</h1>
    <div className="cards">
      <Link className="card" to="/admin/doctors">
        <h2>Doctors</h2>
        <p>Manage directory records.</p>
      </Link>
      <Link className="card" to="/admin/appointments">
        <h2>Appointments</h2>
        <p>View authorized appointment summaries.</p>
      </Link>
      <Link className="card" to="/admin/patients">
        <h2>Patients</h2>
        <p>View minimized, masked summaries.</p>
      </Link>
    </div>
  </>
);
