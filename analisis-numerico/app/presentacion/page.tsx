import { Metadata } from "next";
import Planificacion from "./components/presentacion";

export const metadata: Metadata = {
  title: "Planificación Análisis Numérico 2025",
  description: "Ver los objetivos y metodología de la materia",
};

export default function TP1() {
  return (
    <div>
      <Planificacion />{" "}
    </div>
  );
}
