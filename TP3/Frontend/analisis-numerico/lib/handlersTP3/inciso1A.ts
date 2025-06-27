import { fetchTexto, fetchJSON, API_BASE_URL } from "../utils";

export async function handleInciso1A({
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

    // Textos
    const [consignaTexto, taylorData, problemasTexto] = await Promise.all([
      fetchTexto(`${API_BASE_URL}/raices/consigna-a`),
      fetchJSON<{ salida: string }>(`${API_BASE_URL}/raices/taylor`),
      fetchTexto(`${API_BASE_URL}/raices/dificultad-a`),
    ]);

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(taylorData?.salida || "Error cargando salida.");
    setExperiencia(problemasTexto || "Error cargando experiencias.");

    // Gráficos grafico1 y grafico2
    const imagenesBase: (string | null)[] = [];
    for (let i = 1; i <= 2; i++) {
      try {
        const res = await fetch(`${API_BASE_URL}/raices/grafico${i}`, {
          method: "GET",
          headers: { Accept: "image/png" },
        });
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

    // Gráficos grafico3/0, grafico3/1, grafico3/2
    const imagenesGrafico3: string[] = [];
    for (let iter = 0; iter <= 2; iter++) {
      try {
        const res = await fetch(`${API_BASE_URL}/raices/grafico3/${iter}`, {
          method: "GET",
          headers: { Accept: "image/png" },
        });
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

    // Gráfico extra: f(x) = e⁻ˣ − x con su raíz
    let graficoExtra: string | null = null;
    try {
      const res = await fetch(`${API_BASE_URL}/raices/grafico-f-exponencial`, {
        method: "GET",
        headers: { Accept: "image/png" },
      });
      if (res.ok) {
        const blob = await res.blob();
        graficoExtra = URL.createObjectURL(blob);
      } else {
        const errorText = await res.text();
        console.warn(
          `Error cargando grafico-f-exponencial: ${res.status} - ${errorText}`
        );
      }
    } catch (err) {
      console.warn("Excepción en grafico-f-exponencial:", err);
    }

    // Armar lista final (solo imágenes válidas, en orden)
    const imagenesValidas = [
      ...imagenesBase,
      ...imagenesGrafico3,
      ...(graficoExtra ? [graficoExtra] : []),
    ].filter((url): url is string => url !== null);

    setImagenes(imagenesValidas);

    setImagenes(imagenesValidas);
  } catch (error) {
    console.error("❌ Error general en handleInciso1A:", error);
  } finally {
    setIsLoading(false);
  }
}
