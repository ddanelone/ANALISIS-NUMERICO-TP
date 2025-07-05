"use client";

import { PanelAccordion } from "@/components/panelAccordion";
import {
  fundamentacion,
  proposito,
  objetivos,
  resultadosAprendizaje,
  metodologia,
} from "@/lib/contenido/planificacion";

const Planificacion = () => {
  return (
    <div className="flex flex-col w-full min-h-screen px-4 pt-10 lg:px-12">
      <h1 className="text-3xl font-bold text-center mb-8">
        Planificación de la Materia
      </h1>

      <div className="flex flex-col w-full gap-6  text-justify">
        <PanelAccordion
          titulo="Presentación – Fundamentación"
          contenido={fundamentacion}
          placeholder="No se ha cargado la fundamentación."
        />

        <PanelAccordion
          titulo="Propósito"
          contenido={proposito}
          placeholder="No se ha cargado el propósito."
        />

        <PanelAccordion
          titulo="Objetivos del Diseño Curricular"
          contenido={objetivos}
          placeholder="No se han cargado los objetivos."
        />

        <PanelAccordion
          titulo="Resultados de Aprendizaje"
          contenido={resultadosAprendizaje}
          placeholder="No se han cargado los resultados."
        />

        <PanelAccordion
          titulo="Metodología de la Enseñanza"
          contenido={metodologia}
          placeholder="No se ha cargado la metodología."
        />
      </div>
    </div>
  );
};

export default Planificacion;
