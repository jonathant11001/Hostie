import { useState } from "react";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! How can I help you today?" },
    { sender: "user", text: "What are your hours?" },
    { sender: "bot", text: "We're open Monday–Friday, 9am to 10pm." },
  ]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    if (!input) return;

    const userMessage = { sender: "user", text: input };
    setInput("");

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: input }),
    });

    const data = await res.json();

    setMessages((prev) => [
      ...prev,
      userMessage,
      { sender: "bot", text: data.reply },
    ]);
  }

  return (
    <div style={{ position: "fixed", bottom: 20, right: 20 }}>
      <button onClick={() => setOpen(!open)}>💬</button>

      {open && (
        <div style={{ width: 300, height: 400, background: "white", border: "1px solid #ccc" }}>
          <div style={{ padding: 10, background: "black", color: "white" }}>
            Hostie Chat
          </div>

          <div style={{ height: 300, overflowY: "auto", padding: 10 }}>
            {messages.map((m, i) => (
              <div key={i} className={`text-black ${m.sender === "user" ? "text-right" : "text-left"}`}>
                {m.text}
              </div>
            ))}
          </div>

          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
        </div>
      )}
    </div>
  );
}