import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

export function Selector({
  label,
  placeholder,
  value,
  onChange,
  options,
  className,
  disabled = false,
}: {
  label: string;
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
  required: boolean;
  options: string[];
  className?: string;
  disabled?: boolean;
}) {
  return (
    <div className={cn("space-y-2", className)}>
      <Label>{label}</Label>
      <Select value={value} onValueChange={onChange} required disabled={disabled}>
        <SelectTrigger>
          <SelectValue placeholder={placeholder} />
        </SelectTrigger>
        <SelectContent className="max-h-48">
          {options.map((lang) => (
            <SelectItem key={lang} value={lang}>
              {lang.charAt(0).toUpperCase() + lang.slice(1)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
