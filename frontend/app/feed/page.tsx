"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";

import { fetchCategories, fetchCurrentAffairs, type CurrentAffair } from "@/lib/api";
import CategoryFilter from "@/components/CategoryFilter";
import CurrentAffairCard from "@/components/CurrentAffairCard";

export default function FeedPage() {
  const [items, setItems] = useState<CurrentAffair[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [category, setCategory] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCategories()
      .then(setCategories)
      .catch(() => {
        /* filter bar just stays empty if this fails — not fatal */
      });
  }, []);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    fetchCurrentAffairs({ category: category ?? undefined, q: search || undefined })
      .then((res) => setItems(res.items))
      .catch(() => setError("Couldn't load the feed. Is the backend running on port 8000?"))
      .finally(() => setLoading(false));
  }, [category, search]);

  useEffect(() => {
    const timeout = setTimeout(load, 250); // light debounce for the search box
    return () => clearTimeout(timeout);
  }, [load]);

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-3xl">
        <div className="mb-8 flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-blue-900">Today&apos;s Current Affairs</h1>
            <p className="mt-1 text-slate-600">
              Curated for UPSC, SSC, Banking &amp; State PSC aspirants
            </p>
          </div>
          <Link href="/" className="whitespace-nowrap text-sm text-blue-800 hover:underline">
            ← Home
          </Link>
        </div>

        <div className="mb-6">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search headlines and summaries..."
            className="w-full rounded-lg border border-slate-300 px-4 py-2 text-sm focus:border-blue-500 focus:outline-none sm:max-w-xs"
          />
        </div>

        <div className="mb-8">
          <CategoryFilter categories={categories} active={category} onSelect={setCategory} />
        </div>

        {loading && <p className="text-slate-500">Loading...</p>}
        {error && <p className="text-red-600">{error}</p>}

        {!loading && !error && items.length === 0 && (
          <p className="text-slate-500">No current affairs match these filters yet.</p>
        )}

        <div className="space-y-4">
          {items.map((item) => (
            <CurrentAffairCard key={item.id} item={item} />
          ))}
        </div>
      </div>
    </main>
  );
}
