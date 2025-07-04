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
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
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

    // Cargar imágenes
    const rutas = ["imagen-original", "imagen-estego"];
    const imagenesUrls: string[] = [];

    for (const ruta of rutas) {
      try {
        const res = await fetch(`${API_BASE_URL}/tp2/inciso_1/${ruta}`, {
          method: "GET",
          headers: { Accept: "image/png" },
        });

        if (!res.ok) {
          const errorText = await res.text();
          console.warn(`Error cargando imagen ${ruta}: ${errorText}`);
          continue;
        }

        const blob = await res.blob();
        imagenesUrls.push(URL.createObjectURL(blob));
      } catch (err) {
        console.warn(`Excepción al cargar imagen ${ruta}:`, err);
      }
    }

    setImagenes(imagenesUrls);
    setExperiencia("");
  } catch (error) {
    console.error("❌ Error general en handleInciso2 (TP2):", error);
    setSalidaConsola("Error ejecutando el ocultamiento o la extracción.");
  } finally {
    setIsLoading(false);
  }
}
