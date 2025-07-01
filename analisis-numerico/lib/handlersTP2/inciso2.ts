import { fetchTexto, fetchImagen, API_BASE_URL } from "../utils";

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

    // Textos (teoría y experiencia)
    const [consignaTexto, explicacionTexto, problemasTexto] = await Promise.all(
      [
        fetchTexto(`${API_BASE_URL}/tp2/inciso_2/consigna`),
        fetchTexto(`${API_BASE_URL}/tp2/inciso_2/explicacion`),
        fetchTexto(`${API_BASE_URL}/tp2/inciso_2/problemas`),
      ]
    );

    setConsigna(consignaTexto || "Error cargando consigna.");
    setExperiencia(problemasTexto || "Error cargando problemas.");

    // Ejecutar ocultamiento (POST)
    const ocultarResp = await fetch(`${API_BASE_URL}/tp2/inciso_2/ocultar`, {
      method: "POST",
    });

    if (!ocultarResp.ok) {
      const errorText = await ocultarResp.text();
      throw new Error(`Error en /ocultar: ${errorText}`);
    }

    // Ejecutar extracción (GET)
    const extraido = await fetchTexto(`${API_BASE_URL}/tp2/inciso_2/extraer`);

    const salidaTexto = `
${explicacionTexto}

📥 Proceso realizado:
- Imagen oculta: wp.png
- Imagen portadora: globo.png
- Imagen estego generada: imagen_estego.tiff

📤 Recuperación:
${extraido || "Error extrayendo imagen recuperada."}
`.trim();

    setSalidaConsola(salidaTexto);

    // Cargar imágenes: portadora, oculta, estego, recuperada
    const rutas = ["portadora", "oculta", "estego-png", "recuperada"];

    const imagenes: string[] = [];

    for (const nombre of rutas) {
      const img = await fetchImagen(`${API_BASE_URL}/tp2/inciso_2/${nombre}`);
      if (img) imagenes.push(img);
    }

    setImagenes(imagenes);
  } catch (error) {
    console.error("❌ Error general en handleInciso2 (TP2):", error);
  } finally {
    setIsLoading(false);
  }
}
