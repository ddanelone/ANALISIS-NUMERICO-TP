import { fetchTexto, API_BASE_URL } from "../utils";

export async function handleInciso2({
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

    // Cargar los textos del inciso 2 del TP1
    const [consignaTexto, explicacionTexto, problemasTexto] = await Promise.all(
      [
        fetchTexto(`${API_BASE_URL}/tp1/inciso-2/consigna`),
        fetchTexto(`${API_BASE_URL}/tp1/inciso-2/explicacion`),
        fetchTexto(`${API_BASE_URL}/tp1/inciso-2/problemas`),
      ]
    );

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(explicacionTexto || "Error cargando explicación.");
    setExperiencia(problemasTexto || "Error cargando problemas.");

    // Por ahora no hay imágenes para este inciso
    setImagenes([]);
  } catch (error) {
    console.error("❌ Error general en handleInciso2A (TP1):", error);
  } finally {
    setIsLoading(false);
  }
}
