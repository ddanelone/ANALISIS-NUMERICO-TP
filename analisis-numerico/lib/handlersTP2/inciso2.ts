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
    setIsLoading(true);
    setConsigna("");
    setSalidaConsola("");
    setImagenes([]);

    console.log("🔄 Solicitando textos para TP2 - Inciso 2...");
    const [consignaTexto, explicacionTexto, problemasTexto] = await Promise.all(
      [
        fetchTexto(`${API_BASE_URL}/tp2/inciso_2/consigna`),
        fetchTexto(`${API_BASE_URL}/tp2/inciso_2/explicacion`),
        fetchTexto(`${API_BASE_URL}/tp2/inciso_2/problemas`),
      ]
    );

    console.log("✅ Textos cargados correctamente");
    setConsigna(consignaTexto || "Error cargando consigna.");
    setExperiencia(problemasTexto || "Error cargando problemas.");

    const salidaTexto = `
 ${explicacionTexto}
 
 📥 Proceso realizado:
 - Imagen oculta: wp.png
 - Imagen portadora: globo.png
 - Imagen estego generada: imagen_estego.tiff
 `.trim();
    setSalidaConsola(salidaTexto);

    console.log("🔄 Cargando imágenes...");
    const rutas = ["portadora", "oculta", "estego-png", "recuperada"];

    const imagenPromises = rutas.map(async (nombre) => {
      const url = `${API_BASE_URL}/tp2/inciso_2/${nombre}`;
      console.log(`📷 Solicitando imagen: ${url}`);
      try {
        const res = await fetch(url);
        console.log(`➡️  ${nombre} → Status: ${res.status}`);
        if (!res.ok) {
          console.warn(`⚠️ Imagen fallida: ${nombre} (${res.status})`);
          return null;
        }
        const blob = await res.blob();
        return URL.createObjectURL(blob);
      } catch (err) {
        console.error(`❌ Error de red al cargar ${nombre}:`, err);
        return null;
      }
    });

    const imagenes = await Promise.all(imagenPromises);
    const imagenesValidas = imagenes.filter((img): img is string => !!img);

    console.log("🖼 Imágenes válidas cargadas:", imagenesValidas.length);

    if (imagenesValidas.length === rutas.length) {
      setImagenes(imagenesValidas);
      console.log("✅ Todas las imágenes cargadas correctamente.");
    } else {
      console.error(
        "❌ Faltan imágenes. Solo se cargaron:",
        imagenesValidas.length
      );
      throw new Error("No se pudieron cargar todas las imágenes.");
    }
  } catch (error) {
    console.error("❌ Error general en handleInciso2 (TP2):", error);
  } finally {
    setIsLoading(false);
  }
}
