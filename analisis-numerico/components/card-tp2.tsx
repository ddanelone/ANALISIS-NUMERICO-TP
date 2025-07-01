import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ImagePlayIcon } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function CardTP2() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <ImagePlayIcon className="w-5 h-5" /> TP 2: Esteganografía en Imágenes
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
            className="rounded-xl shadow-md "
          />
        </div>

        <Link href="/tp2">
          <Button className="mt-4" variant="default">
            Ver desarrollo
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
