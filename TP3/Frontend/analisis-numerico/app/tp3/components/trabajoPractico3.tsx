"use client";

import { useState } from "react";
import CarouselOrientation from "./carousel";
import { handleInciso1A } from "@/lib/handlersTP3/inciso1A";
import { handleInciso1B } from "@/lib/handlersTP3/inciso1B";
import { handleInciso2A } from "@/lib/handlersTP3/inciso2A";
import { handleInciso2B } from "@/lib/handlersTP3/inciso2B";
import { IncisoButton } from "@/components/incisoButton";
import { PanelAccordion } from "@/components/panelAccordion";
import { Skeleton } from "@/components/ui/skeleton";
import { LogoHoverCard } from "@/components/logoHoverCard";

const TrabajoPractico3 = () => {
  const [consigna, setConsigna] = useState("");
  const [salidaConsola, setSalidaConsola] = useState("");
  const [experiencia, setExperiencia] = useState("");
  const [imagenes, setImagenes] = useState<string[]>([]);
  const [isLoading, setisLoading] = useState<boolean>(false);
  const [isLoading1, setisLoading1] = useState<boolean>(false);
  const [isLoading2, setisLoading2] = useState<boolean>(false);
  const [isLoading3, setisLoading3] = useState<boolean>(false);
  const isAnyLoading = isLoading || isLoading1 || isLoading2 || isLoading3;
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const onClickIncisoA = () =>
    handleInciso1A({
      setConsigna,
      setSalidaConsola,
      setImagenes,
      setExperiencia,
      setIsLoading: setisLoading,
    });

  const onClickIncisoB = () =>
    handleInciso1B({
      setConsigna,
      setSalidaConsola,
      setImagenes,
      setExperiencia,
      setIsLoading: setisLoading1,
    });

  const onClickInciso2A = () =>
    handleInciso2A({
      setConsigna,
      setSalidaConsola,
      setImagenes,
      setExperiencia,
      setIsLoading2: setisLoading2,
    });

  const onClickInciso2B = () =>
    handleInciso2B({
      setConsigna,
      setSalidaConsola,
      setImagenes,
      setExperiencia,
      setIsLoading3: setisLoading3,
    });

  return (
    <div className="flex flex-row w-full min-h-screen ">
      {/* Menú lateral */}
      <button
        onClick={() => setSidebarOpen(!isSidebarOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-gray-800 text-white rounded-md"
      >
        ☰
      </button>
      <div
        className={`
    fixed top-0 left-0 h-full z-40 bg-gray-800 text-white p-6 transition-transform duration-300 ease-in-out
    ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}
    lg:translate-x-0 lg:static lg:flex lg:w-[250px]
    w-64 flex-col
  `}
      >
        <div className="absolute inset-0 z-[-1] bg-menu-lateral" />
        <LogoHoverCard />

        <ul className="space-y-4 mt-6 w-full">
          <li className="text-lg font-bold px-1 text-center">T.P. 3</li>
          <li className="text-lg font-semibold px-2">Punto 1</li>
          <li>
            <IncisoButton
              label="Inciso a"
              onClick={onClickIncisoA}
              isLoading={isLoading}
            />
          </li>
          <li>
            <IncisoButton
              label="Inciso b"
              onClick={onClickIncisoB}
              isLoading={isLoading1}
            />
          </li>
          <li className="text-lg font-semibold px-2">Punto 2</li>
          <li>
            <IncisoButton
              label="Inciso a"
              onClick={onClickInciso2A}
              isLoading={isLoading2}
            />
          </li>
          <li>
            <IncisoButton
              label="Inciso b"
              onClick={onClickInciso2B}
              isLoading={isLoading3}
            />
          </li>
        </ul>

        <footer className="mt-auto text-sm text-center">
          Grupo 7: Bagnarol - Danelone - Farías - Paduli - Rafart
        </footer>
      </div>

      {/* Contenido principal */}
      <div className="flex-1 h-screen px-4 pt-10 lg:p-8 flex flex-col items-center">
        <div className="w-full max-w-5xl flex flex-col justify-start gap-6">
          <PanelAccordion
            titulo="Consigna a resolver"
            contenido={consigna}
            placeholder="Cargá un inciso para ver la consigna."
          />

          <PanelAccordion
            titulo="Salida en consola"
            contenido={salidaConsola}
            placeholder="Cargá un inciso para ver la salida."
          />

          <PanelAccordion
            titulo="Problemas en la resolución"
            contenido={experiencia}
            placeholder="Cargá un inciso para ver las experiencias."
          />

          {/* Gráficos */}
          <div className="w-full h-auto border rounded-md p-4 bg-background shadow-sm">
            <h2 className="text-xl font-semibold mb-2">Galería de gráficos</h2>

            {imagenes.length === 0 && !isAnyLoading && (
              <p className="text-muted-foreground">No hay imágenes cargadas.</p>
            )}

            {isAnyLoading && (
              <div className="flex gap-4 flex-wrap justify-center">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="flex flex-col items-center space-y-3">
                    {/* Línea superior (título simulado) */}
                    <Skeleton className="h-4 w-[200px] rounded-md" />

                    {/* Imagen cuadrada */}
                    <Skeleton className="h-[250px] w-[250px] rounded-xl" />

                    {/* Línea inferior (texto simulado) */}
                    <Skeleton className="h-4 w-[150px] rounded-md" />
                  </div>
                ))}
              </div>
            )}

            {imagenes.length > 0 && !isAnyLoading && (
              <CarouselOrientation images={imagenes} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrabajoPractico3;
