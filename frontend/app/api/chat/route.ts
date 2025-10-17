import { NextRequest } from "next/server";

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export async function POST(request: NextRequest) {
  const body = await request.text();
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body,
  });

  return new Response(response.body, {
    status: response.status,
    headers: {
      "Content-Type": "application/jsonl",
    },
  });
}
