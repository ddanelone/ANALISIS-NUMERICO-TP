import { Metadata } from "next";
import TrabajoPractico1 from "./components/trabajoPractico1";

export const metadata: Metadata = {
  title: "Trabajo Práctico 1",
  description: "Selecciona el inciso que quieras ver del trabajo práctico 1",
};

export default function TP1() {
  return (
    <div>
      <TrabajoPractico1 />
    </div>
  );
}
