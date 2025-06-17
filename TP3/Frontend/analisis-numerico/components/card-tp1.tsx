import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AudioWaveformIcon } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function CardTP1() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AudioWaveformIcon className="w-5 h-5" /> TP 1: Análisis de Señales de
          Electroencefalograma en Epilepsia
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
          <Button className="mt-4" variant="default">
            Ver desarrollo
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
