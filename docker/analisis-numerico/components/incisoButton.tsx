import { Button } from "@/components/ui/button";
import { LoaderCircle } from "lucide-react";

export function IncisoButton({
  label,
  onClick,
  isLoading,
}: {
  label: string;
  onClick: () => void;
  isLoading: boolean;
}) {
  return (
    <Button
      variant="secondary"
      className="w-full justify-start"
      onClick={onClick}
      disabled={isLoading}
    >
      <span className="mr-2">{label}</span>
      {isLoading && <LoaderCircle className="w-4 h-4 animate-spin ml-auto" />}
    </Button>
  );
}
