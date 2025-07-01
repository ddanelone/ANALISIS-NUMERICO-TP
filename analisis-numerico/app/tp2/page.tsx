import { Metadata } from "next";
import TrabajoPractico2 from "./components/trabajoPractico2";

export const metadata: Metadata = {
  title: "Trabajo Práctico 2",
  description: "Selecciona el inciso que quieras ver del trabajo práctico 2",
};

export default function TP1() {
  return (
    <div>
      <TrabajoPractico2 />
    </div>
  );
}
