import CardTp1 from "@/components/card-tp1";
import CardTP2 from "@/components/card-tp2";
import CardTP3 from "@/components/card-tp3";

export default function Home() {
  return (
    <main className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">
        PRESENTACIÓN DE LOS T.P. DE ANÁLISIS NUMÉRICO 2025
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <CardTp1 />
        <CardTP2 />
        <CardTP3 />
      </div>
    </main>
  );
}
