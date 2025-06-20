import { fetchImagen, fetchTexto } from "../utils";

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
      fetchTexto("http://localhost:8000/api/raices/consigna-b"),
      fetchTexto("http://localhost:8000/api/raices/inciso1b"),
      fetchTexto("http://localhost:8000/api/raices/dificultad-b"),
    ]);

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(consolaTexto || "Error cargando salida.");
    setExperiencia(problemasTexto || "Error cargando experiencias.");

    const grafico = await fetchImagen(
      "http://localhost:8000/api/raices/grafico4"
    );
    setImagenes(grafico ? [grafico] : []);
  } catch (error) {
    console.error("❌ Error general en handleInciso1B:", error);
  } finally {
    setIsLoading(false);
  }
}
