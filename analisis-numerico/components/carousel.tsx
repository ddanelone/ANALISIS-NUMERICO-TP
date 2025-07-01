import * as React from "react";
import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

type Props = {
  images: string[];
};

const CarouselOrientation = ({ images }: Props) => {
  if (!images || images.length === 0) {
    return (
      <div className="text-muted-foreground text-sm italic">
        No hay imágenes cargadas.
      </div>
    );
  }

  return (
    <Carousel
      opts={{ align: "start" }}
      orientation="horizontal"
      className="w-full max-w-full"
    >
      <CarouselContent className="-mt-1 max-h-[500px]">
        {images.map((src, index) => (
          <CarouselItem key={index} className="pt-1 md:basis-full w-full">
            <div className="p-1 h-[470px] w-full">
              <Card className="h-full w-full">
                <CardContent className="h-full w-full p-2 flex items-center justify-center">
                  <img
                    src={src}
                    alt={`Gráfico ${index + 1}`}
                    className="w-full h-full object-contain rounded-md"
                  />
                </CardContent>
              </Card>
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>

      <CarouselPrevious />
      <CarouselNext />
    </Carousel>
  );
};

export default CarouselOrientation;
