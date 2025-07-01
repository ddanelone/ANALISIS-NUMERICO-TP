import { fetchTexto, fetchImagen, API_BASE_URL } from "../utils";

export async function handleInciso4({
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

    // Traer textos
    const [
      consignaTexto,
      explicacionTexto,
      problemasTexto,
      analisisBandasTexto,
    ] = await Promise.all([
      fetchTexto(`${API_BASE_URL}/tp1/inciso-4/consigna`),
      fetchTexto(`${API_BASE_URL}/tp1/inciso-4/explicacion`),
      fetchTexto(`${API_BASE_URL}/tp1/inciso-4/problemas`),
      fetchTexto(`${API_BASE_URL}/tp1/inciso-4/analisis-bandas`),
    ]);

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(
      `${explicacionTexto || "Error cargando explicación."}\n\n${
        analisisBandasTexto || "Error cargando análisis de bandas."
      }`
    );
    setExperiencia(problemasTexto || "Error cargando problemas.");

    // Cargar gráficos: autocorrelación y potencia por bandas
    const rutas = ["grafico1", "grafico2"];
    const imagenes: string[] = [];

    for (const ruta of rutas) {
      const img = await fetchImagen(`${API_BASE_URL}/tp1/inciso-4/${ruta}`);
      if (img) imagenes.push(img);
    }

    setImagenes(imagenes);
  } catch (error) {
    console.error(
      "❌ Error general al cargar datos del inciso 4 (TP1):",
      error
    );
  } finally {
    setIsLoading3(false);
  }
}
