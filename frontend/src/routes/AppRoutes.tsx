import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
import { dashboardFor } from "../auth/oidc";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { RoleRoute } from "../components/RoleRoute";
import { AdminLayout } from "../layouts/AdminLayout";
import { DoctorLayout } from "../layouts/DoctorLayout";
import { PatientLayout } from "../layouts/PatientLayout";
import { AdminAppointmentsPage } from "../pages/admin/AdminAppointmentsPage";
import { AdminDashboardPage } from "../pages/admin/AdminDashboardPage";
import { AdminDoctorsPage } from "../pages/admin/AdminDoctorsPage";
import { AdminPatientsPage } from "../pages/admin/AdminPatientsPage";
import { DoctorAppointmentsPage } from "../pages/doctor/DoctorAppointmentsPage";
import { DoctorAvailabilityPage } from "../pages/doctor/DoctorAvailabilityPage";
import { DoctorDashboardPage } from "../pages/doctor/DoctorDashboardPage";
import { LoginPage } from "../pages/LoginPage";
import { NotFoundPage } from "../pages/NotFoundPage";
import { OAuthCallbackPage } from "../pages/OAuthCallbackPage";
import { DoctorDetailsPage } from "../pages/patient/DoctorDetailsPage";
import { DoctorsPage } from "../pages/patient/DoctorsPage";
import { PatientAppointmentsPage } from "../pages/patient/PatientAppointmentsPage";
import { PatientDashboardPage } from "../pages/patient/PatientDashboardPage";
import { UnauthorizedPage } from "../pages/UnauthorizedPage";
function Root() {
  const auth = useAuth();
  return (
    <Navigate
      replace
      to={auth.user ? dashboardFor(auth.user.roles) : "/login"}
    />
  );
}
export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Root />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/auth/callback" element={<OAuthCallbackPage />} />
      <Route path="/unauthorized" element={<UnauthorizedPage />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<RoleRoute roles={["patient"]} />}>
          <Route path="/patient" element={<PatientLayout />}>
            <Route path="dashboard" element={<PatientDashboardPage />} />
            <Route path="doctors" element={<DoctorsPage />} />
            <Route path="doctors/:doctorId" element={<DoctorDetailsPage />} />
            <Route path="appointments" element={<PatientAppointmentsPage />} />
          </Route>
        </Route>
        <Route element={<RoleRoute roles={["doctor"]} />}>
          <Route path="/doctor" element={<DoctorLayout />}>
            <Route path="dashboard" element={<DoctorDashboardPage />} />
            <Route path="appointments" element={<DoctorAppointmentsPage />} />
            <Route path="availability" element={<DoctorAvailabilityPage />} />
          </Route>
        </Route>
        <Route element={<RoleRoute roles={["administrator"]} />}>
          <Route path="/admin" element={<AdminLayout />}>
            <Route path="dashboard" element={<AdminDashboardPage />} />
            <Route path="doctors" element={<AdminDoctorsPage />} />
            <Route path="appointments" element={<AdminAppointmentsPage />} />
            <Route path="patients" element={<AdminPatientsPage />} />
          </Route>
        </Route>
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
