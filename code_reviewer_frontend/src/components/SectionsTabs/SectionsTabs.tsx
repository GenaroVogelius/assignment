import { TabsList, TabsTrigger } from "@/components/ui/tabs";

export interface SectionsTabsProps {
  sections: {
    value: string;
    title: string;
  }[];
}

export function SectionsTabs({ sections }: SectionsTabsProps) {
  const getGridCols = (count: number) => {
    const gridMap: Record<number, string> = {
      1: "grid-cols-1",
      2: "grid-cols-2",
      3: "grid-cols-3",
      4: "grid-cols-4",
      5: "grid-cols-5",
      6: "grid-cols-6",
    };
    return gridMap[count] || "grid-cols-1";
  };

  return (
    <TabsList className={`grid w-full ${getGridCols(sections.length)}`}>
      {sections.map((section) => (
        <TabsTrigger
          key={section.value}
          value={section.value}
          className="flex items-center gap-2"
        >
          {section.title}
        </TabsTrigger>
      ))}
    </TabsList>
  );
}
