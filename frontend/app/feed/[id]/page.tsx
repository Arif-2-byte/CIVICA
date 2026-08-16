"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

import { fetchCurrentAffair, type CurrentAffair } from "@/lib/api";
import { categoryStyles } from "@/lib/categoryStyles";

export default function CurrentAffairDetailPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params.id);
  const [item, setItem] = useState<CurrentAffair | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCurrentAffair(id)
      .then(setItem)
      .catch(() => setError("Couldn't load this item."));
  }, [id]);

  if (error) {
    return (
      <main className="min-h-screen bg-slate-50 px-6 py-10">
        <div className="mx-auto max-w-2xl">
          <p className="text-red-600">{error}</p>
          <Link href="/feed" className="mt-4 inline-block text-blue-800 hover:underline">
            ← Back to feed
          </Link>
        </div>
      </main>
    );
  }

  if (!item) {
    return (
      <main className="min-h-screen bg-slate-50 px-6 py-10">
        <div className="mx-auto max-w-2xl text-slate-500">Loading...</div>
      </main>
    );
  }

  const style = categoryStyles[item.category] ?? categoryStyles.default;

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-2xl">
        <Link href="/feed" className="text-sm text-blue-800 hover:underline">
          ← Back to feed
        </Link>

        <div className="mt-4 flex items-center gap-3">
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${style.bg} ${style.text}`}>
            {item.category}
          </span>
          <time className="text-xs text-slate-500">
            {new Date(item.published_date).toLocaleDateString("en-IN", {
              day: "numeric",
              month: "long",
              year: "numeric",
            })}
          </time>
        </div>

        <h1 className="mt-3 text-2xl font-bold text-slate-900">{item.headline}</h1>

        <p className="mt-4 whitespace-pre-line text-base leading-relaxed text-slate-700">
          {item.summary}
        </p>

        <div className="mt-6 flex flex-wrap gap-2">
          {item.exam_tags.map((tag) => (
            <span
              key={tag}
              className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600"
            >
              {tag}
            </span>
          ))}
        </div>

        {item.source_url && (
          <a
            href={item.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-6 inline-block text-sm text-blue-800 hover:underline"
          >
            Read full source: {item.source_name} ↗
          </a>
        )}
      </div>
    </main>
  );
}
