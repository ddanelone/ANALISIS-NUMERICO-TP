import { API_BASE_URL } from "../utils";

type Parametros = {
  a: number;
  b: number;
  tol: number;
  max_iter: number;
};

export async function handleInciso2B({
  setConsigna,
  setSalidaConsola,
  setImagenes,
  setExperiencia,
  setIsLoading3,
  a,
  b,
  tol,
  max_iter,
}: {
  setConsigna: (val: string) => void;
  setSalidaConsola: (val: string) => void;
  setImagenes: (val: string[]) => void;
  setExperiencia: (val: string) => void;
  setIsLoading3: (val: boolean) => void;
} & Parametros) {
  try {
    setConsigna("");
    setSalidaConsola("");
    setImagenes([]);
    setIsLoading3(true);

    const payload: Parametros = { a, b, tol, max_iter };

    // Consignas
    const consignaGral = await fetch(
      `${API_BASE_URL}/tp3/gases/consigna-gral`
    ).then((res) => res.text());
    const consignaB = await fetch(`${API_BASE_URL}/tp3/gases/consigna-b`).then(
      (res) => res.text()
    );
    setConsigna(`${consignaGral}\n\n${consignaB}`);

    // Experiencia
    const experienciaTexto = await fetch(
      `${API_BASE_URL}/tp3/gases/dificultad-b`
    ).then((res) => res.text());
    setExperiencia(experienciaTexto);

    // Resultado (texto consola)
    const salida = await fetch(`${API_BASE_URL}/tp3/gases/taylor-vdw`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then(async (res) => {
      if (!res.ok) throw new Error(await res.text());
      return res.text();
    });
    setSalidaConsola(salida);

    // Imágenes en orden
    const rutas = ["grafico-a", "grafico-b", "zoom"];
    const imagenes: string[] = [];

    for (const ruta of rutas) {
      const imgBlob = await fetch(`${API_BASE_URL}/tp3/gases/${ruta}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).then((res) => (res.ok ? res.blob() : null));

      if (imgBlob) {
        const imgUrl = URL.createObjectURL(imgBlob);
        imagenes.push(imgUrl);
      }
    }

    setImagenes(imagenes);
  } catch (error) {
    console.error("❌ Error al procesar el inciso 2B:", error);
    setSalidaConsola("Error al obtener los resultados del backend.");
  } finally {
    setIsLoading3(false);
  }
}
