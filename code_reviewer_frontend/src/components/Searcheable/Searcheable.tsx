import { Input } from "../ui/input";
import { Label } from "../ui/label";

export function Searcheable({
  label,
  placeholder,
  value,
  onChange,
  disabled = false,
}: {
  label: string;
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}) {
  return (
    <div className="space-y-2">
      <Label htmlFor="search">{label}</Label>
      <div className="relative">
        <Input
          id="search"
          placeholder={placeholder}
          value={value}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            onChange(e.target.value)
          }
          disabled={disabled}
        />
      </div>
    </div>
  );
}
