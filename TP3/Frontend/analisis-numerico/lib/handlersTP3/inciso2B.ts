import { fetchTexto, fetchImagen } from "../utils";

export async function handleInciso2B({
  setConsigna,
  setSalidaConsola,
  setImagenes,
  setExperiencia,
  setIsLoading3,
}: {
  setConsigna: (val: string) => void;
  setSalidaConsola: (val: string) => void;
  setImagenes: (val: string[]) => void;
  setExperiencia: (val: string) => void;
  setIsLoading3: (val: boolean) => void;
}) {
  try {
    setConsigna("");
    setSalidaConsola("");
    setImagenes([]);
    setIsLoading3(true);

    // Consigna
    const consignaGral = await fetchTexto(
      "http://localhost:8000/api/gases/consigna-gral"
    );
    const consignaB = await fetchTexto(
      "http://localhost:8000/api/gases/consigna-b"
    );
    const consignaTexto = `${consignaGral}\n\n${consignaB}`;

    // Dificultades
    const problemasTexto = await fetchTexto(
      "http://localhost:8000/api/gases/dificultad-b"
    );

    // Resultado
    const consolaTexto = await fetchTexto(
      "http://localhost:8000/api/gases/taylor-vdw"
    );

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(consolaTexto || "Error cargando salida.");
    setExperiencia(problemasTexto || "Error cargando experiencias.");

    // Cargar imágenes en orden: grafico-a, grafico-b, zoom
    const rutas = ["grafico-a", "grafico-b", "zoom"];
    const imagenes: string[] = [];

    for (const ruta of rutas) {
      const img = await fetchImagen(`http://localhost:8000/api/gases/${ruta}`);
      if (img) imagenes.push(img);
    }

    setImagenes(imagenes);
  } catch (error) {
    console.error("❌ Error general al cargar datos del inciso 2B:", error);
  } finally {
    setIsLoading3(false);
  }
}
