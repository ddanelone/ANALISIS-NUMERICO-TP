import { Metadata } from "next";
import TrabajoPractico3 from "./components/trabajoPractico3";

export const metadata: Metadata = {
  title: "Trabajo Práctico 3",
  description: "Selecciona el inciso que quieras ver del trabajo práctico 3",
};

export default function TP1() {
  return (
    <div>
      <TrabajoPractico3 />
    </div>
  );
}
