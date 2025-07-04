import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectGroup,
  SelectLabel,
  SelectItem,
} from "@/components/ui/select";

const opcionesValidas = [
  { a: 0.364, b: 0.00004267, tol: 0.000001, max_iter: 50 },
  { a: 0.4, b: 0.00005, tol: 0.000001, max_iter: 50 },
  { a: 0.35, b: 0.000045, tol: 0.000001, max_iter: 50 },
  { a: 0.39, b: 0.000048, tol: 0.000001, max_iter: 50 },
  { a: 0.37, b: 0.000046, tol: 0.000001, max_iter: 50 },
];

const opcionesInvalidas = [
  { a: 0.0001, b: 1.0, tol: 0.000001, max_iter: 50 },
  { a: 0.00001, b: 0.1, tol: 0.000001, max_iter: 50 },
  { a: 0.0001, b: 0.01, tol: 0.000001, max_iter: 50 },
];

type Props = {
  onChange: (val: {
    a: number;
    b: number;
    tol: number;
    max_iter: number;
  }) => void;
  valorSeleccionado?: string;
};

export const SelectCondicionesIniciales = ({ onChange }: Props) => {
  const handleChange = (value: string) => {
    const parsed = JSON.parse(value);
    onChange(parsed);
  };

  return (
    <div className="w-full max-w-[220px]">
      <Select onValueChange={handleChange}>
        <SelectTrigger>
          <SelectValue placeholder="Condiciones iniciales" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectLabel className="text-green-600">Rangos válidos</SelectLabel>
            {opcionesValidas.map((opcion, i) => (
              <SelectItem key={`valido-${i}`} value={JSON.stringify(opcion)}>
                {`a=${opcion.a} - b=${opcion.b}`}
              </SelectItem>
            ))}
          </SelectGroup>
          <SelectGroup>
            <SelectLabel className="text-red-500">Rangos inválidos</SelectLabel>
            {opcionesInvalidas.map((opcion, i) => (
              <SelectItem key={`invalido-${i}`} value={JSON.stringify(opcion)}>
                {`a=${opcion.a} - b=${opcion.b}`}
              </SelectItem>
            ))}
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>
  );
};
