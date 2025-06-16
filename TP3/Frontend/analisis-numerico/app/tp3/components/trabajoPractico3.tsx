"use client";

import { useState } from "react";
import Logo from "@/components/logo";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import CarouselOrientation from "./carousel";
import { LoaderCircle } from "lucide-react";
import { Label } from "@/components/ui/label";

const TrabajoPractico3 = () => {
  const [consigna, setConsigna] = useState("");
  const [salidaConsola, setSalidaConsola] = useState("");
  const [imagenes, setImagenes] = useState<string[]>([]);
  const [isLoading, setisLoading] = useState<boolean>(false);
  const [isLoading1, setisLoading1] = useState<boolean>(false);
  const [isLoading2, setisLoading2] = useState<boolean>(false);
  const [isLoading3, setisLoading3] = useState<boolean>(false);

  const handleIncisoA = async () => {
    try {
      // Limpiar estado previo
      setConsigna("");
      setSalidaConsola("");
      setImagenes([]);
      // Consigna (texto plano)
      setisLoading(true);
      const consignaRes = await fetch(
        "http://localhost:8000/api/raices/consigna-a"
      );
      const consignaTexto = await consignaRes.text();

      // Método newton (POST, JSON)
      const consolaRes = await fetch(
        "http://localhost:8000/api/raices/newton",
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );
      const consolaData = await consolaRes.json();

      setConsigna(consignaTexto || "Error cargando consigna.");
      setSalidaConsola(consolaData.resultado || "Error cargando salida.");

      // Cargar grafico1 y grafico2 en serie, asegurando orden y carga completa
      const imagenesBase: (string | null)[] = [];
      for (let i = 1; i <= 2; i++) {
        try {
          const res = await fetch(
            `http://localhost:8000/api/raices/grafico${i}`,
            {
              method: "GET",
              headers: { Accept: "image/png" },
            }
          );
          if (!res.ok) {
            const errorText = await res.text();
            console.warn(
              `Error cargando grafico${i}: ${res.status} - ${errorText}`
            );
            imagenesBase.push(null);
            continue;
          }
          const blob = await res.blob();
          imagenesBase.push(URL.createObjectURL(blob));
        } catch (err) {
          console.warn(`Excepción en grafico${i}:`, err);
          imagenesBase.push(null);
        }
      }

      // Cargar grafico3/0, grafico3/1, grafico3/2 en serie
      const imagenesGrafico3: string[] = [];
      for (let iter = 0; iter <= 2; iter++) {
        try {
          const res = await fetch(
            `http://localhost:8000/api/raices/grafico3/${iter}`,
            {
              method: "GET",
              headers: { Accept: "image/png" },
            }
          );
          if (!res.ok) {
            const errorText = await res.text();
            console.warn(
              `Error cargando grafico3/${iter}: ${res.status} - ${errorText}`
            );
            continue;
          }
          const blob = await res.blob();
          imagenesGrafico3.push(URL.createObjectURL(blob));
        } catch (err) {
          console.warn(`Excepción en grafico3/${iter}:`, err);
        }
      }

      // Filtrar imágenes válidas y actualizarlas
      const imagenesValidas = [...imagenesBase, ...imagenesGrafico3].filter(
        Boolean
      ) as string[];
      setImagenes(imagenesValidas);
    } catch (error) {
      console.error("Error general al cargar datos del inciso A:", error);
    } finally {
      setisLoading(false);
    }
  };

  const handleIncisoB = async () => {
    try {
      // Limpiar estado previo
      setConsigna("");
      setSalidaConsola("");
      setImagenes([]);
      setisLoading1(true);

      // Cargar la consigna (texto plano)
      const consignaRes = await fetch(
        "http://localhost:8000/api/raices/consigna-b"
      );
      const consignaTexto = await consignaRes.text();

      // Cargar resultado del método combinado (GET, texto plano)
      const consolaRes = await fetch(
        "http://localhost:8000/api/raices/inciso1b"
      );
      const consolaTexto = await consolaRes.text();

      setConsigna(consignaTexto || "Error cargando consigna.");
      setSalidaConsola(consolaTexto || "Error cargando salida.");

      // Cargar único gráfico (grafico4)
      const imagenes: string[] = [];
      try {
        const res = await fetch("http://localhost:8000/api/raices/grafico4", {
          method: "GET",
          headers: { Accept: "image/png" },
        });
        if (!res.ok) {
          const errorText = await res.text();
          console.warn(`Error cargando grafico4: ${res.status} - ${errorText}`);
        } else {
          const blob = await res.blob();
          imagenes.push(URL.createObjectURL(blob));
        }
      } catch (err) {
        console.warn("Excepción cargando grafico4:", err);
      }

      setImagenes(imagenes);
    } catch (error) {
      console.error("Error general al cargar datos del inciso B:", error);
    } finally {
      setisLoading1(false);
    }
  };

  const handleInciso2A = async () => {
    try {
      // Limpiar estado previo
      setConsigna("");
      setSalidaConsola("");
      setImagenes([]);
      setisLoading2(true);

      // Cargar la consigna (texto plano)
      const consignaGral = await fetch(
        "http://localhost:8000/api/gases/consigna-gral"
      );
      let consignaTexto = await consignaGral.text();

      const consignaRes = await fetch(
        "http://localhost:8000/api/gases/consigna-a"
      );

      const consignaTexto2 = await consignaRes.text();

      consignaTexto += `\n\n${consignaTexto2}`;

      // Cargar resultado del método combinado (GET, texto plano)
      const consolaRes = await fetch(
        "http://localhost:8000/api/gases/explicacion-inciso-a"
      );
      const consolaTexto = await consolaRes.text();

      setConsigna(consignaTexto || "Error cargando consigna.");
      setSalidaConsola(consolaTexto || "Error cargando salida.");

      const imagenes: string[] = [];
      const urls = [
        "http://localhost:8000/api/gases/grafico_comparativo_gral",
        "http://localhost:8000/api/gases/grafico_comparativo_z",
        "http://localhost:8000/api/gases/grafico-a",
      ];

      for (const url of urls) {
        try {
          const res = await fetch(url, {
            method: "GET",
            headers: { Accept: "image/png" },
          });
          if (!res.ok) {
            const errorText = await res.text();
            console.warn(`Error cargando ${url}: ${res.status} - ${errorText}`);
          } else {
            const blob = await res.blob();
            imagenes.push(URL.createObjectURL(blob));
          }
        } catch (err) {
          console.warn(`Excepción cargando ${url}:`, err);
        }
      }
      setImagenes(imagenes);
    } catch (error) {
      console.error("Error general al cargar datos del inciso B:", error);
    } finally {
      setisLoading2(false);
    }
  };

  const handleInciso2B = async () => {
    try {
      // Limpiar estado previo
      setConsigna("");
      setSalidaConsola("");
      setImagenes([]);
      setisLoading3(true);

      // Cargar la consigna (texto plano)
      const consignaGral = await fetch(
        "http://localhost:8000/api/gases/consigna-gral"
      );
      let consignaTexto = await consignaGral.text();

      const consignaRes = await fetch(
        "http://localhost:8000/api/gases/consigna-b"
      );

      const consignaTexto2 = await consignaRes.text();

      consignaTexto += `\n\n${consignaTexto2}`;

      // Cargar resultado del método combinado (GET, recibo texto plano)
      const consolaRes = await fetch(
        "http://localhost:8000/api/gases/taylor-vdw"
      );
      const consolaTexto = await consolaRes.text();

      setConsigna(consignaTexto || "Error cargando consigna.");
      setSalidaConsola(consolaTexto || "Error en los datos recibidos.");

      // Cargar las dos imágenes en orden: grafico-b y zoom
      const imagenes: string[] = [];

      const rutas = ["grafico-b", "zoom"];
      for (const ruta of rutas) {
        try {
          const res = await fetch(`http://localhost:8000/api/gases/${ruta}`, {
            method: "GET",
            headers: { Accept: "image/png" },
          });
          if (!res.ok) {
            const errorText = await res.text();
            console.warn(
              `Error cargando ${ruta}: ${res.status} - ${errorText}`
            );
            continue;
          }
          const blob = await res.blob();
          imagenes.push(URL.createObjectURL(blob));
        } catch (err) {
          console.warn(`Excepción al cargar ${ruta}:`, err);
        }
      }

      setImagenes(imagenes);
    } catch (error) {
      console.error("Error general al cargar datos del inciso A:", error);
    } finally {
      setisLoading3(false);
    }
  };

  return (
    <div className="flex flex-row w-full min-h-screen ">
      {/* Menú lateral */}
      <div className="hidden lg:flex lg:w-[250px] flex-col bg-gray-800 text-white p-6 relative">
        <div className="absolute inset-0 z-[-1] bg-menu-lateral" />
        <Logo />

        <ul className="space-y-4 mt-6 w-full">
          <li className="text-lg font-semibold px-2">Punto 1</li>
          <li>
            <Button
              variant="secondary"
              className="w-full justify-start"
              onClick={handleIncisoA}
              disabled={isLoading}
            >
              <span className="mr-2">Inciso a</span>
              {isLoading && (
                <LoaderCircle className="w-4 h-4 animate-spin ml-auto black" />
              )}
            </Button>
          </li>
          <li>
            <Button
              variant="secondary"
              className="w-full justify-start"
              onClick={handleIncisoB}
              disabled={isLoading1}
            >
              <span className="mr-2">Inciso b</span>
              {isLoading1 && (
                <LoaderCircle className="w-4 h-4 animate-spin ml-auto black" />
              )}
            </Button>
          </li>
          <li className="text-lg font-semibold px-2">Punto 2</li>
          <li>
            <Button
              variant="secondary"
              className="w-full justify-start"
              onClick={handleInciso2A}
              disabled={isLoading2}
            >
              <span className="mr-2">Inciso a</span>
              {isLoading2 && (
                <LoaderCircle className="w-4 h-4 animate-spin ml-auto black" />
              )}
            </Button>
          </li>
          <li>
            <Button
              variant="secondary"
              className="w-full justify-start"
              onClick={handleInciso2B}
              disabled={isLoading3}
            >
              <span className="mr-2">Inciso b</span>
              {isLoading3 && (
                <LoaderCircle className="w-4 h-4 animate-spin ml-auto black" />
              )}
            </Button>
          </li>
        </ul>

        <footer className="mt-auto text-sm text-center">
          Grupo 7: Bagnarol - Danelone - Farías - Paduli - Rafart
        </footer>
      </div>

      {/* Contenido principal */}
      <div className="flex-1 h-screen px-4 pt-10 lg:p-8 flex flex-col items-center">
        <div className="w-full max-w-5xl flex flex-col justify-start gap-6">
          {/* Consigna */}
          <div className="w-full">
            <h2 className="text-xl font-semibold mb-2">Consigna a resolver</h2>
            <Label className="w-full block">
              <ScrollArea className="w-full max-h-32 rounded-md border p-4 font-mono text-sm whitespace-pre-wrap bg-muted overflow-y-auto">
                {consigna || "Cargá un inciso para ver la consigna."}
              </ScrollArea>
            </Label>
          </div>

          {/* Consola */}
          <div className="w-full">
            <h2 className="text-xl font-semibold mb-2">Salida en consola</h2>
            <ScrollArea className="w-full max-h-56 rounded-md border p-4 font-mono text-sm whitespace-pre-wrap bg-muted overflow-y-auto">
              {salidaConsola || "Cargá un inciso para ver la salida."}
            </ScrollArea>
          </div>

          {/* Gráficos */}
          <div className="w-full h-auto">
            <h2 className="text-xl font-semibold mb-2">Galería de gráficos</h2>
            <CarouselOrientation images={imagenes} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrabajoPractico3;
