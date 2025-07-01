import { fetchTexto, fetchImagen, API_BASE_URL } from "../utils";

export async function handleInciso3({
  setConsigna,
  setSalidaConsola,
  setImagenes,
  setExperiencia,
  setIsLoading2,
}: {
  setConsigna: (val: string) => void;
  setSalidaConsola: (val: string) => void;
  setImagenes: (val: string[]) => void;
  setExperiencia: (val: string) => void;
  setIsLoading2: (val: boolean) => void;
}) {
  try {
    setConsigna("");
    setSalidaConsola("");
    setImagenes([]);
    setIsLoading2(true);

    // Cargar textos desde backend
    const [consignaTexto, explicacionTexto, problemasTexto] = await Promise.all(
      [
        fetchTexto(`${API_BASE_URL}/tp1/inciso-3/consigna`),
        fetchTexto(`${API_BASE_URL}/tp1/inciso-3/explicacion`),
        fetchTexto(`${API_BASE_URL}/tp1/inciso-3/problemas`),
      ]
    );

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(explicacionTexto || "Error cargando explicación.");
    setExperiencia(problemasTexto || "Error cargando experiencia.");

    // Cargar imágenes de los gráficos
    const urls = [
      `${API_BASE_URL}/tp1/inciso-3/grafico1`,
      `${API_BASE_URL}/tp1/inciso-3/grafico2`,
    ];
    const imagenes: string[] = [];

    for (const url of urls) {
      const img = await fetchImagen(url);
      if (img) imagenes.push(img);
    }

    setImagenes(imagenes);
  } catch (error) {
    console.error(
      "❌ Error general al cargar datos del inciso 3 (TP1):",
      error
    );
  } finally {
    setIsLoading2(false);
  }
}
