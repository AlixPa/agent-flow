import { Outlet, useNavigate } from "react-router";
import { useEffect } from "react";

function Layout() {
  const navigate = useNavigate();
  useEffect(() => {
    navigate("/graph");
  }, []);

  return (
    <div className="p-5">
      <Outlet />
    </div>
  );
}

export default Layout;
