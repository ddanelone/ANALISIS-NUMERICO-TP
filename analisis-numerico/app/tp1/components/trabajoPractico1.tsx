"use client";

import { useState } from "react";
import { IncisoButton } from "@/components/incisoButton";
import { PanelAccordion } from "@/components/panelAccordion";
import { Skeleton } from "@/components/ui/skeleton";
import { LogoHoverCard } from "@/components/logoHoverCard";
import CarouselOrientation from "@/components/carousel";
import { handleInciso1 } from "@/lib/handlersTP1/inciso1";
import { handleInciso2 } from "@/lib/handlersTP1/inciso2";
import { handleInciso3 } from "@/lib/handlersTP1/inciso3";
import { handleInciso4 } from "@/lib/handlersTP1/inciso4";

const TrabajoPractico1 = () => {
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

  const onClickInciso1 = () =>
    handleInciso1({
      setConsigna,
      setSalidaConsola,
      setImagenes,
      setExperiencia,
      setIsLoading: setisLoading,
    });

  const onClickInciso2 = () =>
    handleInciso2({
      setConsigna,
      setSalidaConsola,
      setImagenes,
      setExperiencia,
      setIsLoading: setisLoading1,
    });

  const onClickInciso3 = () =>
    handleInciso3({
      setConsigna,
      setSalidaConsola,
      setImagenes,
      setExperiencia,
      setIsLoading2: setisLoading2,
    });

  const onClickInciso4 = () =>
    handleInciso4({
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
          <li className="text-lg font-bold px-1 text-center">T.P. 1</li>
          <li>
            <IncisoButton
              label="Inciso 1"
              onClick={onClickInciso1}
              isLoading={isLoading}
            />
          </li>
          <li>
            <IncisoButton
              label="Inciso 2"
              onClick={onClickInciso2}
              isLoading={isLoading1}
            />
          </li>
          <li>
            <IncisoButton
              label="Inciso 3"
              onClick={onClickInciso3}
              isLoading={isLoading2}
            />
          </li>
          <li>
            <IncisoButton
              label="Inciso 4 "
              onClick={onClickInciso4}
              isLoading={isLoading3}
            />
          </li>
        </ul>

        <br />
        <br />
        <br />
        <br />
        <br />

        <footer className="mt-auto text-sm text-center">
          Grupo 7: Bagnarol - Danelone - Farías - Paduli - Rafart
        </footer>
      </div>

      {/* Contenido principal */}
      <div className="flex-1 h-screen px-4 pt-10 lg:p-8 flex flex-col items-center">
        <div className="w-full max-w-5xl flex flex-col justify-start gap-6">
          <h1 className="text-2xl font-bold text-center">
            T.P.1: Transformada de Fourier
          </h1>
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

export default TrabajoPractico1;
