import { fetchTexto, API_BASE_URL } from "../utils";

export async function handleInciso1({
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

    // 📘 Traer consigna teórica
    const consignaTexto = await fetchTexto(
      `${API_BASE_URL}/tp2/inciso_1/consigna`
    );

    setConsigna(consignaTexto || "Error cargando consigna.");

    // 🔁 Ocultar mensaje (simulado con texto hardcodeado)
    const mensaje = encodeURIComponent(
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    );
    const ocultarURL = `${API_BASE_URL}/tp2/inciso_1/ocultar?mensaje=${mensaje}`;

    const resPost = await fetch(ocultarURL, {
      method: "POST",
      headers: {
        Accept: "text/plain",
      },
    });

    if (!resPost.ok) {
      const errorText = await resPost.text();
      throw new Error(`Error en /ocultar: ${errorText}`);
    }

    const respuestaOcultamiento = await resPost.text();

    // 📤 Extraer imagen oculta
    const respuestaExtraccion = await fetchTexto(
      `${API_BASE_URL}/tp2/inciso_1/extraer`
    );

    const salidaFinal = `
📥 Resultado del ocultamiento:
${respuestaOcultamiento}

📤 Resultado de la extracción:
${respuestaExtraccion}
    `.trim();

    setSalidaConsola(salidaFinal);

    // (Opcional) cargar imágenes en el futuro
    setImagenes([]);
    setExperiencia("");
  } catch (error) {
    console.error("❌ Error general en handleInciso2 (TP2):", error);
    setSalidaConsola("Error ejecutando el ocultamiento o la extracción.");
  } finally {
    setIsLoading(false);
  }
}
