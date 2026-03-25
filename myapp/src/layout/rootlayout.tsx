import { Outlet } from "react-router-dom";
import { Navbar } from "../component/navbar";

function RootLayout() {
  return (
    <div>
      <Navbar />
      <Outlet />
    </div>
  );
}

export default RootLayout;
