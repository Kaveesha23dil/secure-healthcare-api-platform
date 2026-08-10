import type { Appointment, AppointmentStatus } from "../api/types";
import { formatDate } from "../utils/dates";
export function AppointmentTable({
  items,
  action,
}: {
  items: Appointment[];
  action?: (item: Appointment, status: AppointmentStatus) => void;
}) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Doctor reference</th>
            <th>Status</th>
            <th>Reason</th>
            {action && <th>Action</th>}
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{formatDate(item.startAt)}</td>
              <td>{item.doctorId}</td>
              <td>
                <span className="badge">{item.status}</span>
              </td>
              <td>{item.reason}</td>
              {action && (
                <td>
                  {["proposed", "booked"].includes(item.status) && (
                    <button onClick={() => action(item, "cancelled")}>
                      Cancel
                    </button>
                  )}
                  {item.status === "booked" && (
                    <button onClick={() => action(item, "checked-in")}>
                      Check in
                    </button>
                  )}
                  {item.status === "checked-in" && (
                    <button onClick={() => action(item, "completed")}>
                      Complete
                    </button>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
