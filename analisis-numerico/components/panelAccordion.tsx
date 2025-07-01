import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

export function PanelAccordion({
  titulo,
  contenido,
  placeholder,
}: {
  titulo: string;
  contenido: string;
  placeholder: string;
}) {
  return (
    <div className="w-full border rounded-md p-4 bg-background shadow-sm">
      <Accordion type="single" collapsible>
        <AccordionItem value="item-1">
          <AccordionTrigger className="h-10 flex items-center hover:bg-muted/50 rounded-md transition">
            <h2 className="text-xl font-semibold mb-2">{titulo}</h2>
          </AccordionTrigger>
          <AccordionContent>
            <div className="whitespace-pre-wrap">
              {contenido || placeholder}
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
}
