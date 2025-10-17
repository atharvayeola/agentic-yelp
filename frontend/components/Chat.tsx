"use client";

import { useEffect, useRef, useState } from "react";
import { createSessionId, streamChat } from "../lib/api";

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sessionId] = useState<string>(() => createSessionId());
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    return () => abortRef.current?.abort();
  }, []);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = input.trim();
    if (!value) return;

    const nextMessages = [
      ...messages,
      { id: crypto.randomUUID(), role: "user" as const, content: value },
    ];
    setMessages(nextMessages);
    setInput("");

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    for await (const chunk of streamChat({
      session_id: sessionId,
      message: value,
    }, controller.signal)) {
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "assistant", content: chunk },
      ]);
    }
  }

  return (
    <div className="space-y-4 rounded-xl bg-white p-6 shadow">
      <div className="flex max-h-96 flex-col gap-2 overflow-y-auto">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`rounded-lg px-3 py-2 text-sm ${
              message.role === "user"
                ? "self-end bg-slate-900 text-white"
                : "self-start bg-slate-100 text-slate-900"
            }`}
          >
            <span className="block whitespace-pre-line">{message.content}</span>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask for a restaurant recommendation…"
          className="flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm"
        />
        <button
          type="submit"
          className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white"
        >
          Send
        </button>
      </form>
    </div>
  );
}
