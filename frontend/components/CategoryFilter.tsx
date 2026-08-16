"use client";

interface Props {
  categories: string[];
  active: string | null;
  onSelect: (category: string | null) => void;
}

export default function CategoryFilter({ categories, active, onSelect }: Props) {
  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => onSelect(null)}
        className={`rounded-full px-4 py-1.5 text-sm font-medium transition ${
          active === null
            ? "bg-blue-900 text-white"
            : "border border-slate-200 bg-white text-slate-600 hover:border-blue-300"
        }`}
      >
        All
      </button>
      {categories.map((cat) => (
        <button
          key={cat}
          onClick={() => onSelect(cat)}
          className={`rounded-full px-4 py-1.5 text-sm font-medium transition ${
            active === cat
              ? "bg-blue-900 text-white"
              : "border border-slate-200 bg-white text-slate-600 hover:border-blue-300"
          }`}
        >
          {cat}
        </button>
      ))}
    </div>
  );
}
