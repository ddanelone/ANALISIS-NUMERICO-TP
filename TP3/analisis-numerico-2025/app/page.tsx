import { AppSidebar } from "@/components/ui/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";

export default function Home() {
  return (
    <div>
      <SidebarProvider>
        <AppSidebar />
      </SidebarProvider>{" "}
    </div>
  );
}
