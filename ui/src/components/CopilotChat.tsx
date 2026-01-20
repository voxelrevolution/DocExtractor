import { useMemo, useState } from "react";
import { EvidencePanel } from "./EvidencePanel";

type Citation = {
  source: string;
  page?: number;
  line?: number;
  snippet?: string;
};

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
};

type Scope = "document" | "corpus";

const seedMessages: ChatMessage[] = [
  {
    id: "msg-1",
    role: "assistant",
    content: "Ask a question about the selected document or the full corpus."
  }
];

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const clientId = (import.meta.env.VITE_DOCEXTRACTOR_CLIENT_ID ?? "").trim() || undefined;

function isLocalApiBase(urlString: string): boolean {
  try {
    const parsed = new URL(urlString);
    return parsed.hostname === "localhost" || parsed.hostname === "127.0.0.1" || parsed.hostname === "::1";
  } catch {
    return false;
  }
}

export function CopilotChat() {
  const [scope, setScope] = useState<Scope>("document");
  const [messages, setMessages] = useState<ChatMessage[]>(seedMessages);
  const [input, setInput] = useState("");
  const [error, setError] = useState<string | null>(null);

  const localOnly = useMemo(() => isLocalApiBase(apiBaseUrl), []);

  const history = useMemo(() => messages, [messages]);

  const handleSend = async () => {
    if (!localOnly) {
      setError("Copilot chat requires local API access. Set VITE_API_BASE_URL to http://localhost:8000.");
      return;
    }
    if (!input.trim()) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: input.trim()
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const response = await fetch(`${apiBaseUrl}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          scope,
          message: userMessage.content,
          client_id: clientId,
          history: messages
            .filter((message) => message.role === "user" || message.role === "assistant")
            .map((message) => ({ role: message.role, content: message.content }))
        })
      });

      if (!response.ok) {
        throw new Error(`chat request failed: ${response.status}`);
      }

      const data = (await response.json()) as { reply: string; citations?: Citation[] };
      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: data.reply,
        citations: data.citations ?? []
      };

      setError(null);
      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      setError("Unable to run inference. Please retry in a moment.");
    }
  };

  const handleKeyDown: React.KeyboardEventHandler<HTMLTextAreaElement> = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <section className="chat" aria-label="Copilot chat">
      <div className="chat-header">
        <div>
          <h3>Copilot chat</h3>
          <p className="panel-subtitle">Local inference only. Evidence shown per response.</p>
        </div>
        <div className="scope-toggle" role="group" aria-label="Scope">
          <button
            type="button"
            className={scope === "document" ? "scope-button active" : "scope-button"}
            onClick={() => setScope("document")}
          >
            Document
          </button>
          <button
            type="button"
            className={scope === "corpus" ? "scope-button active" : "scope-button"}
            onClick={() => setScope("corpus")}
          >
            Corpus
          </button>
        </div>
      </div>

      {error ? (
        <div className="status-banner error" role="alert">
          {error}
        </div>
      ) : null}

      <div className="chat-history" role="log" aria-live="polite">
        {history.map((message) => (
          <div
            key={message.id}
            className={message.role === "user" ? "chat-bubble user" : "chat-bubble assistant"}
          >
            <div className="chat-role">{message.role === "user" ? "You" : "Copilot"}</div>
            <div className="chat-content">{message.content}</div>
            {message.citations ? (
              <EvidencePanel
                title="Evidence"
                evidence={message.citations.map((citation) => ({
                  source: citation.source,
                  page: citation.page,
                  line: citation.line,
                  snippet: citation.snippet
                }))}
              />
            ) : null}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <textarea
          rows={3}
          placeholder="Ask a question about this document or the full corpus..."
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button type="button" className="primary-button" onClick={handleSend}>
          Send
        </button>
      </div>
    </section>
  );
}
