import { Outlet } from "react-router-dom";
import Sidebar from "../layout/Sidebar";
import { StickyNavbar } from "@/components/Navbar";
import { ThemeProvider } from "@material-tailwind/react";

const AdminDashboard = () => {
  return (
    <ThemeProvider>
      <div className="flex h-screen">
        <div className="w-[256px] flex-shrink-0">
          <Sidebar />
        </div>
        <div className="flex flex-col flex-1 overflow-hidden">
          <StickyNavbar />
          <main className="p-6 overflow-auto">
            <Outlet /> {/* Internal pages are rendered here */}
          </main>
        </div>
      </div>
    </ThemeProvider>
  );
};

export default AdminDashboard;