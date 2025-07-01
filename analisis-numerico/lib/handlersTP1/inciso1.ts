import { fetchTexto, API_BASE_URL } from "../utils";

export async function handleInciso1({
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
}) {
  try {
    setConsigna("");
    setSalidaConsola("");
    setImagenes([]);
    setIsLoading(true);

    // Traer textos desde el backend del TP1
    const [consignaTexto, explicacionTexto, problemasTexto] = await Promise.all(
      [
        fetchTexto(`${API_BASE_URL}/tp1/inciso-1/consigna`),
        fetchTexto(`${API_BASE_URL}/tp1/inciso-1/explicacion`),
        fetchTexto(`${API_BASE_URL}/tp1/inciso-1/problemas`),
      ]
    );

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(explicacionTexto || "Error cargando explicación.");
    setExperiencia(problemasTexto || "Error cargando análisis.");

    // Cargar gráficos: grafico, grafico2, grafico3
    const imagenesUrls: string[] = [];
    const nombres = ["grafico", "grafico2", "grafico3"];

    for (const nombre of nombres) {
      try {
        const res = await fetch(`${API_BASE_URL}/tp1/inciso-1/${nombre}`, {
          method: "GET",
          headers: { Accept: "image/png" },
        });

        if (!res.ok) {
          const errorText = await res.text();
          console.warn(
            `Error cargando ${nombre}: ${res.status} - ${errorText}`
          );
          continue;
        }

        const blob = await res.blob();
        imagenesUrls.push(URL.createObjectURL(blob));
      } catch (err) {
        console.warn(`Excepción al cargar ${nombre}:`, err);
      }
    }

    setImagenes(imagenesUrls);
  } catch (error) {
    console.error("❌ Error general en handleInciso1A (TP1):", error);
  } finally {
    setIsLoading(false);
  }
}
