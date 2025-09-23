import { Searcheable } from "@/components/Searcheable";
import { Selector } from "@/components/Selector";
import { Button } from "@/components/ui/button";
import { SCORE_FILTERS, STATUS_FILTERS } from "@/lib/utils";
import { Search } from "lucide-react";
import { useState } from "react";

export interface ReviewFiltersProps {
  handleSearchById: (searchId: string) => void;
  handleSearchByFilters: () => void;
  languageFilter: string;
  setLanguageFilter: (value: string) => void;
  statusFilter: string;
  setStatusFilter: (value: string) => void;
  scoreFilter: string;
  setScoreFilter: (value: string) => void;
  programmingLanguages: string[];
  currentSearchId: string;
  setCurrentSearchId: (value: string) => void;
}

export function ReviewFilters({
  handleSearchByFilters,
  languageFilter,
  setLanguageFilter,
  statusFilter,
  setStatusFilter,
  scoreFilter,
  setScoreFilter,
  programmingLanguages,
  currentSearchId,
  setCurrentSearchId,
  handleSearchById,
}: ReviewFiltersProps) {
  const [selectorsDisabled, setSelectorsDisabled] = useState(false);

  const SelectorClassName =
    "lg:flex md:flex-col lg:items-center lg:text-center";

  const handleSearchByIdLocal = (value: string) => {

    if (value === "") {
      setSelectorsDisabled(false);
    } else {
      setSelectorsDisabled(true);
    }
    setCurrentSearchId(value);
  };

  const handleSearchButtonClickLocal = () => {
    if (currentSearchId !== "") {
      // Search by ID
      setSelectorsDisabled(false);
      setCurrentSearchId("");
      handleSearchById(currentSearchId);
    } else {
      // Search by filters
      handleSearchByFilters();
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-6 gap-4">
      <Searcheable
        label="Search by ID"
        placeholder="Review ID"
        value={currentSearchId}
        onChange={handleSearchByIdLocal}
      />

      <Selector
        label="Language"
        placeholder="Select language"
        value={languageFilter}
        onChange={setLanguageFilter}
        required={true}
        options={programmingLanguages}
        disabled={selectorsDisabled}
        className={SelectorClassName}
      />

      <Selector
        label="Status"
        placeholder="Select status"
        value={statusFilter}
        onChange={setStatusFilter}
        required={true}
        options={STATUS_FILTERS}
        disabled={selectorsDisabled}
        className={SelectorClassName}
      />

      <Selector
        label="Score"
        placeholder="Select score"
        value={scoreFilter}
        onChange={setScoreFilter}
        required={true}
        options={SCORE_FILTERS}
        disabled={selectorsDisabled}
        className={SelectorClassName}
      />
      <div className="space-y-2 flex justify-end items-end">
        <Button
          onClick={() => handleSearchButtonClickLocal()}
          variant="outline"
          size="sm"
        >
          Search
          <Search className="size-4" />
        </Button>
      </div>
    </div>
  );
}
