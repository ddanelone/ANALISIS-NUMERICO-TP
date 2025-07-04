import { fetchTexto, API_BASE_URL } from "../utils";

export async function handleInciso3({
  setConsigna,
  setSalidaConsola,
  setImagenes,
  setExperiencia,
  setIsLoading,
}: {
  setConsigna: (val: string) => void;
  setSalidaConsola: (val: string) => void;
  setImagenes: (val: string[]) => void;
  setExperiencia: (val: string) => void;
  setIsLoading: (val: boolean) => void;
  delta: number;
}) {
  try {
    setConsigna("");
    setSalidaConsola("");
    setImagenes([]);
    setIsLoading(true);

    // Traer textos
    const [consignaTexto, explicacionTexto, problemasTexto, conclusionesTexto] =
      await Promise.all([
        fetchTexto(`${API_BASE_URL}/tp2/inciso_3/consigna`),
        fetchTexto(`${API_BASE_URL}/tp2/inciso_3/explicacion`),
        fetchTexto(`${API_BASE_URL}/tp2/inciso_3/problemas`),
        fetchTexto(`${API_BASE_URL}/tp2/inciso_3/conclusiones`),
      ]);

    setConsigna(consignaTexto || "Error cargando consigna.");

    // Salida en consola: explicación + conclusiones
    const textoSalida = `${explicacionTexto || ""}\n\n${
      conclusionesTexto || ""
    }`.trim();
    setSalidaConsola(
      textoSalida || "Error cargando explicación o conclusiones."
    );

    // Problemas → se renderiza en el accordion
    setExperiencia(problemasTexto || "Error cargando problemas.");

    // Cargar imágenes
    const rutas = ["portadora", "oculta", "estego", "recuperada"];
    const imagenesUrls: string[] = [];

    for (const ruta of rutas) {
      try {
        const res = await fetch(`${API_BASE_URL}/tp2/inciso_3/${ruta}`, {
          method: "GET",
          headers: { Accept: "image/png" },
        });

        if (!res.ok) {
          const errorText = await res.text();
          console.warn(`Error cargando imagen ${ruta}: ${errorText}`);
          continue;
        }

        const blob = await res.blob();
        imagenesUrls.push(URL.createObjectURL(blob));
      } catch (err) {
        console.warn(`Excepción al cargar imagen ${ruta}:`, err);
      }
    }

    setImagenes(imagenesUrls);
  } catch (error) {
    console.error("❌ Error general en handleInciso3 (TP2):", error);
  } finally {
    setIsLoading(false);
  }
}
