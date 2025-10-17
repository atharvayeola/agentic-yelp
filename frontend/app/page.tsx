"use client";

import { Chat } from "../components/Chat";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center bg-slate-50 p-6">
      <div className="w-full max-w-3xl space-y-6">
        <header className="space-y-2 text-center">
          <h1 className="text-3xl font-bold">TableTalk</h1>
          <p className="text-slate-600">
            A conversational dining assistant powered by Google ADK tools and AWS Bedrock.
          </p>
        </header>
        <Chat />
      </div>
    </main>
  );
}
