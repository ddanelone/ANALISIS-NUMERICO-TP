import { fetchImagen, fetchTexto, API_BASE_URL } from "../utils";

export async function handleInciso1B({
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

    const [consignaTexto, consolaTexto, problemasTexto] = await Promise.all([
      fetchTexto(`${API_BASE_URL}/raices/consigna-b`),
      fetchTexto(`${API_BASE_URL}/raices/inciso1b`),
      fetchTexto(`${API_BASE_URL}/raices/dificultad-b`),
    ]);

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(consolaTexto || "Error cargando salida.");
    setExperiencia(problemasTexto || "Error cargando experiencias.");

    const grafico = await fetchImagen(`${API_BASE_URL}/raices/grafico4`);
    setImagenes(grafico ? [grafico] : []);
  } catch (error) {
    console.error("❌ Error general en handleInciso1B:", error);
  } finally {
    setIsLoading(false);
  }
}
