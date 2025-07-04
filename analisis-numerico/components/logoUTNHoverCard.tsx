import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import LogoUTN from "./logo_utn";

export const LogoUTNHoverCard = () => {
  return (
    <HoverCard openDelay={150} closeDelay={100}>
      <HoverCardTrigger asChild>
        <div className="cursor-pointer">
          <LogoUTN />
        </div>
      </HoverCardTrigger>
      <HoverCardContent className="w-80 bg-background border border-muted shadow-xl">
        {/* Imagen */}
        <img
          src="/utn.jpg"
          alt="UTN FRSF"
          className="w-full h-36 object-cover rounded-md mb-2"
        />

        {/* Datos de la facultad */}
        <div className="text-sm text-muted-foreground space-y-1">
          <div className="font-medium text-base text-foreground">
            UTN - Facultad Regional Santa Fe
          </div>
          <div>Dirección: Lavaisse 610, S3004 Santa Fe</div>
          <div>Teléfono: (0342) 4601573</div>
          <div>
            Sitio web:{" "}
            <a
              href="https://www.frsf.utn.edu.ar"
              target="_blank"
              className="underline"
            >
              frsf.utn.edu.ar
            </a>
          </div>
        </div>

        <p className="text-xs text-right text-muted-foreground mt-2">
          Año 2025 • Impulsando Ingeniería
        </p>
      </HoverCardContent>
    </HoverCard>
  );
};
