import { fetchTexto, fetchImagen, API_BASE_URL, fetchPostJSON } from "../utils";

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
      `${API_BASE_URL}/tp3/gases/consigna-gral`
    );
    const consignaA = await fetchTexto(`${API_BASE_URL}/tp3/gases/consigna-a`);
    const consignaTexto = `${consignaGral}\n\n${consignaA}`;

    // Explicación teórica
    const explicacionTexto = await fetchTexto(
      `${API_BASE_URL}/tp3/gases/explicacion-inciso-a`
    );

    // Dificultades encontradas
    const problemasTexto = await fetchTexto(
      `${API_BASE_URL}/tp3/gases/dificultad-a`
    );

    const resultado = await fetchPostJSON<{
      volumen_ideal: number;
      volumen_taylor: number;
      volumen_combinado: number;
      "diferencia_taylor_%": number;
      "diferencia_combinado_%": number;
    }>(`${API_BASE_URL}/tp3/gases/resultado`, {
      a: 0.364,
      b: 0.00004267,
      tol: 0.000001,
      max_iter: 50,
    });

    const textoSalida = `
${explicacionTexto}

📌 Resultado numérico:
- Volumen ideal: ${resultado?.volumen_ideal} m³/mol

- Volumen calculado con Taylor: ${resultado?.volumen_taylor} m³/mol
- Diferencia relativa con Taylor: ${resultado?.["diferencia_taylor_%"]} %
- Volumen calculado con Taylor + Bisección: ${resultado?.volumen_combinado} m³/mol
- Diferencia relativa con Taylor + Bisección: ${resultado?.["diferencia_combinado_%"]} %
`;

    setConsigna(consignaTexto || "Error cargando consigna.");
    setSalidaConsola(textoSalida || "Error cargando salida.");
    setExperiencia(problemasTexto || "Error cargando experiencias.");

    // Cargar imágenes (en orden)
    const urls = [
      `${API_BASE_URL}/tp3/gases/grafico_comparativo_gral`,
      `${API_BASE_URL}/tp3/gases/grafico_comparativo_z`,
      `${API_BASE_URL}/tp3/gases/grafico-f-vdw`,
      `${API_BASE_URL}/tp3/gases/grafico_comparacion_volumenes`,
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
