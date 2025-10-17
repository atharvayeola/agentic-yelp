export interface ChatPayload {
  session_id: string;
  message: string;
}

export function createSessionId() {
  if (typeof window === "undefined") {
    return "demo-session";
  }
  const existing = window.localStorage.getItem("tabletalk-session");
  if (existing) return existing;
  const fresh = crypto.randomUUID();
  window.localStorage.setItem("tabletalk-session", fresh);
  return fresh;
}

export async function* streamChat(payload: ChatPayload, signal?: AbortSignal) {
  const response = await fetch("/api/chat", {
    method: "POST",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" },
    signal,
  });

  if (!response.ok || !response.body) {
    throw new Error("Failed to stream chat");
  }

  const reader = response.body
    .pipeThrough(new TextDecoderStream())
    .getReader();

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (!value) continue;
      const lines = value.trim().split(/\n+/);
      for (const line of lines) {
        yield line;
      }
    }
  } finally {
    reader.releaseLock();
  }
}
