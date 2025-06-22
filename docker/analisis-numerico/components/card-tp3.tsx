import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FunctionSquareIcon } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function CardTP3() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FunctionSquareIcon className="w-5 h-5" /> TP 3: Búsqueda de Raíces en
          funciones no lineales
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p>Cálculo numérico y su aplicación a un sistema de gases.</p>

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
          <Button className="mt-4" variant="default">
            Ver desarrollo
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
