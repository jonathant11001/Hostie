import { useState } from "react";
import ReactMarkdown from "react-markdown";

const API_BASE = "http://localhost:8000";

type Message = { sender: "user" | "bot"; text: string };

export default function ChatWidget({ apiKey }: { apiKey: string }) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { sender: "bot", text: "Hi! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { sender: "user", text }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat/widget`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Api-Key": apiKey,
        },
        body: JSON.stringify({
          message: text,
          ...(conversationId ? { conversation_id: conversationId } : {}),
        }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const data = await res.json();
      if (!conversationId) setConversationId(data.conversation_id);
      setMessages((prev) => [...prev, { sender: "bot", text: data.response }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed bottom-5 right-5 flex flex-col-reverse items-end">
      <button
        onClick={() => setOpen(!open)}
        className="w-12 h-12 rounded-full bg-blue-600 text-white text-xl shadow-lg flex items-center justify-center hover:bg-blue-700 transition-colors"
      >
        💬
      </button>

      <div
        className={`mb-2 w-[375px] h-[555px] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-200 transition-all duration-300 ease-out origin-bottom-right ${
          open
            ? "opacity-100 scale-100 pointer-events-auto"
            : "opacity-0 scale-0 pointer-events-none"
        }`}
      >
          {/* Header */}
          <div className="px-4 py-3 bg-black text-white font-semibold text-sm">
            Hostie Chat
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-2">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.sender === "user" ? "justify-end" : "justify-start"}`}>
                <span
                  className={`max-w-[75%] px-3 py-2 text-sm leading-snug break-words ${
                    m.sender === "user"
                      ? "bg-blue-600 text-white rounded-[18px_18px_4px_18px]"
                      : "bg-gray-200 text-black rounded-[18px_18px_18px_4px]"
                  }`}
                >
                  {m.sender === "bot" ? (
                    <ReactMarkdown
                      components={{
                        p: ({ children }) => <p className="mb-1 last:mb-0">{children}</p>,
                        ul: ({ children }) => <ul className="pl-0 mb-1 list-none">{children}</ul>,
                        ol: ({ children }) => <ol className="pl-0 mb-1 list-none">{children}</ol>,
                        li: ({ children }) => <li className="mb-0.5">{children}</li>,
                        strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
                      }}
                    >
                      {m.text}
                    </ReactMarkdown>
                  ) : (
                    m.text
                  )}
                </span>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <span className="px-3 py-2 bg-gray-200 text-gray-400 text-sm rounded-[18px_18px_18px_4px]">
                  ...
                </span>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Type a message…"
              disabled={loading}
              className="w-full px-3 py-2 text-sm text-black bg-gray-200 border border-gray-200 rounded-full outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            />
          </div>
        </div>
    </div>
  );
}
