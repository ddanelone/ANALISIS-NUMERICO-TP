import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import Logo from "./logo";

export const LogoHoverCard = () => {
  return (
    <HoverCard openDelay={150} closeDelay={100}>
      <HoverCardTrigger asChild>
        <div className="cursor-pointer">
          <Logo />
        </div>
      </HoverCardTrigger>
      <HoverCardContent className="w-80 bg-background border border-muted shadow-xl">
        <h4 className="text-lg font-semibold">Cuerpo docente</h4>
        <div className="text-sm text-muted-foreground mt-1 space-y-1">
          <div>Pablo &apos;The Punisher&apos; Kler</div>
          <div>Luis &apos;The Legend&apos; Bianculi</div>
          <div>Nicolás &apos;The Chaos Coordinator&apos; Frank</div>
        </div>
        <p className="text-xs text-right text-muted-foreground mt-2">
          Año 2025 • React + FastAPI
        </p>
      </HoverCardContent>
    </HoverCard>
  );
};
