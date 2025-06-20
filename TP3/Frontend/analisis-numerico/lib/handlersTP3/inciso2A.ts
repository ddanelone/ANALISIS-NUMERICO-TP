import { fetchTexto, fetchJSON, fetchImagen } from "../utils";

export async function handleInciso2A({
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

    // Cargar consigna general + específica
    const consignaGral = await fetchTexto(
      "http://localhost:8000/api/gases/consigna-gral"
    );
    const consignaA = await fetchTexto(
      "http://localhost:8000/api/gases/consigna-a"
    );
    const consignaTexto = `${consignaGral}\n\n${consignaA}`;

    // Explicación teórica
    const explicacionTexto = await fetchTexto(
      "http://localhost:8000/api/gases/explicacion-inciso-a"
    );

    // Dificultades encontradas
    const problemasTexto = await fetchTexto(
      "http://localhost:8000/api/gases/dificultad-a"
    );

    // Resultado (JSON)
    const resultado = await fetchJSON<{
      volumen_ideal: number;
      volumen_real: number;
      "diferencia_relativa_%": number;
    }>("http://localhost:8000/api/gases/resultado");

    const textoSalida = `
${explicacionTexto}

📌 Resultado numérico:
- Volumen ideal: ${resultado?.volumen_ideal} m³/mol
- Volumen real: ${resultado?.volumen_real} m³/mol
- Diferencia relativa: ${resultado?.["diferencia_relativa_%"]} %
`;

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(textoSalida || "Error cargando salida.");
    setExperiencia(problemasTexto || "Error cargando experiencias.");

    // Cargar imágenes (en orden)
    const urls = [
      "http://localhost:8000/api/gases/grafico_comparativo_gral",
      "http://localhost:8000/api/gases/grafico_comparativo_z",
      "http://localhost:8000/api/gases/grafico_comparacion_volumenes",
    ];
    const imagenes: string[] = [];

    for (const url of urls) {
      const img = await fetchImagen(url);
      if (img) imagenes.push(img);
    }

    setImagenes(imagenes);
  } catch (error) {
    console.error("❌ Error general al cargar datos del inciso 2A:", error);
  } finally {
    setIsLoading2(false);
  }
}
