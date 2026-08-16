export type Category =
  | "Polity & Governance"
  | "Economy"
  | "Environment & Ecology"
  | "Science & Technology"
  | "International Relations"
  | "Awards & Honours"
  | "Sports"
  | "Defence & Security"
  | "Person in News"
  | "Place in News"
  | "Schemes & Policies"
  | "Reports & Indices";

export type Importance = "high" | "medium" | "low";

export interface CurrentAffair {
  id: number;
  headline: string;
  summary: string;
  source_name: string;
  source_url?: string | null;
  published_date: string;
  category: Category;
  exam_tags: string[];
  importance: Importance;
}

export interface PaginatedCurrentAffairs {
  total: number;
  page: number;
  page_size: number;
  items: CurrentAffair[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchCurrentAffairs(
  params: { category?: string; q?: string; page?: number } = {}
): Promise<PaginatedCurrentAffairs> {
  const search = new URLSearchParams();
  if (params.category) search.set("category", params.category);
  if (params.q) search.set("q", params.q);
  if (params.page) search.set("page", String(params.page));

  const res = await fetch(`${API_BASE}/api/current-affairs?${search.toString()}`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch current affairs");
  return res.json();
}

export async function fetchCurrentAffair(id: number): Promise<CurrentAffair> {
  const res = await fetch(`${API_BASE}/api/current-affairs/${id}`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch item");
  return res.json();
}

export async function fetchCategories(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/current-affairs/categories`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch categories");
  return res.json();
}
