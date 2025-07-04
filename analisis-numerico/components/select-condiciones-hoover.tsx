import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { Info } from "lucide-react";
import { SelectCondicionesIniciales } from "./select-condiciones-ini";

type Props = {
  onChange: (val: {
    a: number;
    b: number;
    tol: number;
    max_iter: number;
  }) => void;
};

export function CondicionesInicialesHover({ onChange }: Props) {
  return (
    <div className="flex items-center gap-2 w-full">
      <SelectCondicionesIniciales onChange={onChange} />
      <HoverCard openDelay={200} closeDelay={300}>
        <HoverCardTrigger asChild>
          <Info className="h-5 w-5 text-blue-500 cursor-help" />
        </HoverCardTrigger>
        <HoverCardContent className="w-96 border bg-background shadow-xl text-sm pointer-events-auto z-50">
          <div className="flex items-start gap-2">
            <Info className="h-5 w-5 mt-1 text-blue-500" />
            <div className="space-y-2">
              <p className="text-base font-semibold">Condiciones iniciales</p>
              <p>La ecuación de Van der Waals introduce dos parámetros:</p>
              <ul className="list-disc list-inside ml-2">
                <li>
                  <strong>
                    <code>a</code>
                  </strong>
                  : Corrige la presión por las{" "}
                  <em>fuerzas de atracción intermoleculares</em>.
                </li>
                <li>
                  <strong>
                    <code>b</code>
                  </strong>
                  : Representa el <em>volumen efectivo</em> ocupado por las
                  moléculas.
                </li>
              </ul>
              <p>
                Seleccioná un conjunto adecuado de <code>a</code> y{" "}
                <code>b</code> para obtener raíces válidas al resolver.
              </p>
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    </div>
  );
}
