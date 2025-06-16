import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import {
  AudioWaveformIcon,
  FunctionSquareIcon,
  ImagePlayIcon,
} from "lucide-react";
import Image from "next/image";

export default function Home() {
  return (
    <main className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">
        PRESENTACIÓN DE LOS TP DE ANÁLISIS NUMÉRICO 2025
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AudioWaveformIcon className="w-5 h-5" /> TP 1: Análisis de
              Señales de Electroencefalograma en Epilepsia
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p>Aplicación de la Transformada Discreta de Fourier.</p>

            <div className="my-4">
              <Image
                src="/tp1.png"
                alt="Visualización EEG"
                width={400}
                height={400}
                className="rounded-xl shadow-md"
              />
            </div>

            <Link href="/tp1">
              <Button className="mt-4" variant="secondary">
                Ver TP 1
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ImagePlayIcon className="w-5 h-5" /> TP 2: Esteganografía en
              Imágenes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p>Aplicación de la Transformada 2D de Fourier.</p>

            <div className="my-4">
              <Image
                src="/tp2.png"
                alt="Visualización EEG"
                width={300}
                height={300}
                className="rounded-xl shadow-md"
              />
            </div>

            <Link href="/tp2">
              <Button className="mt-4" variant="secondary">
                Ver TP 2
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FunctionSquareIcon className="w-5 h-5" /> TP 3: Búsqueda de
              Raíces en funciones no lineales
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p>y aplicación a un sistema de gases.</p>

            <div className="my-4">
              <Image
                src="/tp3.png"
                alt="Visualización EEG"
                width={400}
                height={400}
                className="rounded-xl shadow-md"
              />
            </div>

            <Link href="/tp3">
              <Button className="mt-4" variant="secondary">
                Ver TP 3
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
