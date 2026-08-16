import Link from "next/link";

import type { CurrentAffair } from "@/lib/api";
import { categoryStyles } from "@/lib/categoryStyles";

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export default function CurrentAffairCard({ item }: { item: CurrentAffair }) {
  const style = categoryStyles[item.category] ?? categoryStyles.default;

  return (
    <Link
      href={`/feed/${item.id}`}
      className="block rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-blue-300 hover:shadow-md"
    >
      <div className="flex items-center justify-between gap-3">
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${style.bg} ${style.text}`}>
          {item.category}
        </span>
        <time className="shrink-0 text-xs text-slate-500">{formatDate(item.published_date)}</time>
      </div>

      <h3 className="mt-3 text-lg font-semibold text-slate-900">{item.headline}</h3>
      <p className="mt-2 line-clamp-3 text-sm leading-relaxed text-slate-600">{item.summary}</p>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        {item.exam_tags.map((tag) => (
          <span
            key={tag}
            className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600"
          >
            {tag}
          </span>
        ))}
        {item.importance === "high" && (
          <span className="ml-auto text-xs font-semibold text-red-600">● High priority</span>
        )}
      </div>
    </Link>
  );
}
