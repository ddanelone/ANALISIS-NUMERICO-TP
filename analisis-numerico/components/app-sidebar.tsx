import {
  Flame,
  Gauge,
  FunctionSquare,
  Sigma,
  AudioWaveform,
  ImagePlay,
  LayoutList,
  Clipboard,
} from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { LogoUTNHoverCard } from "./logoUTNHoverCard";

// Menu items.
const items = [
  {
    title: "Dashboard",
    url: "/",
    icon: LayoutList,
  },
  {
    title: "Planificación A.N.",
    url: "presentacion",
    icon: Clipboard,
  },
  {
    title: "Trabajo Práctico N°1",
    url: "tp1",
    icon: AudioWaveform,
  },
  {
    title: "Trabajo Práctico N°2",
    url: "tp2",
    icon: ImagePlay,
  },
  {
    title: "Trabajo Práctico N°3",
    url: "tp3",
    icon: FunctionSquare,
  },
  {
    title: "Trabajo Práctico N°4",
    url: "tp4",
    icon: Gauge,
  },
  {
    title: "Trabajo Práctico N°5",
    url: "tp5",
    icon: Flame,
  },
  {
    title: "Trabajo Práctico N°6",
    url: "tp6",
    icon: Sigma,
  },
];

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarContent className="flex flex-col">
        <div className="px-4 py-3 border-b border-white/20">
          <LogoUTNHoverCard />
        </div>
        <SidebarGroup>
          <SidebarGroupLabel className="text-lg font-semibold">
            Opciones navegación:
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
