"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface Message {
  id: string;
  role: "erica" | "user";
  content: string;
  timestamp: Date;
}

interface SessionQuestion {
  id: string;
  text: string;
  answer?: string;
  hints?: string[];
}

interface KnowledgeCheckProps {
  lesson: { id: string };
  module: {
    module_id: string;
    title: string;
    objective: string;
  };
  checkpoint: {
    checkpoint_id: string;
    questions: string[];
  };
  onComplete: (sessionId: string) => void;
}

export function KnowledgeCheck({
  lesson,
  module,
  checkpoint,
  onComplete,
}: KnowledgeCheckProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sessionQuestions, setSessionQuestions] = useState<SessionQuestion[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [showHint, setShowHint] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const initialized = useRef(false);

  const addMessage = useCallback((role: "erica" | "user", content: string) => {
    setMessages((prev) => [
      ...prev,
      {
        id: `msg-${Date.now()}-${Math.random()}`,
        role,
        content,
        timestamp: new Date(),
      },
    ]);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;
    initializeCheckpoint();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const initializeCheckpoint = async () => {
    try {
      const response = await fetch("/api/checkpoint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lesson: { id: lesson.id },
          module_id: module.module_id,
        }),
      });

      const data = await response.json();
      setIsInitializing(false);

      if (!response.ok || !data.session_id) {
        const fallbackQs: SessionQuestion[] = checkpoint.questions.map((q) => ({
          id: `fallback-${Math.random()}`,
          text: q,
        }));
        setSessionQuestions(fallbackQs);
        addMessage("erica", `Hey! Let's spar on **${module.title}**. I'll ask you questions from your material — think out loud, I'm here to guide you, not grade you. 🧠`);
        setTimeout(() => addMessage("erica", `**Question 1/${fallbackQs.length}:** ${fallbackQs[0]?.text}`), 800);
        return;
      }

      const questions: SessionQuestion[] = data.questions || [];
      setSessionId(data.session_id);
      setSessionQuestions(questions);

      addMessage("erica", `Hey! Let's spar on **${module.title}**. I'll ask you questions directly from your practice material — think out loud, I'm here to guide you, not grade you. 🧠`);

      if (questions.length > 0) {
        setTimeout(() => {
          addMessage("erica", `**Question 1/${questions.length}:** ${questions[0].text}`);
        }, 800);
      }
    } catch {
      setIsInitializing(false);
      const fallbackQs: SessionQuestion[] = checkpoint.questions.map((q) => ({
        id: `fallback-${Math.random()}`,
        text: q,
      }));
      setSessionQuestions(fallbackQs);
      addMessage("erica", `Let's get started on **${module.title}**!`);
      setTimeout(() => addMessage("erica", `**Question 1/${fallbackQs.length}:** ${fallbackQs[0]?.text}`), 800);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = inputValue.trim();
    if (!trimmed || isLoading) return;

    setInputValue("");
    setShowHint(false);
    addMessage("user", trimmed);
    setIsLoading(true);

    const currentQuestion = sessionQuestions[currentQuestionIndex];

    try {
      let aiResponse: string | null = null;
      let completed = false;
      let remainingIds: string[] = [];

      if (sessionId && currentQuestion && !currentQuestion.id.startsWith("fallback-")) {
        const res = await fetch("/api/checkpoint", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: sessionId,
            lesson: { id: lesson.id },
            module_id: module.module_id,
            answers: [{ question_id: currentQuestion.id, answer: trimmed }],
          }),
        });
        const data = await res.json();
        aiResponse = data.ai_feedback || null;
        completed = data.completed || false;
        remainingIds = data.remaining_question_ids || [];
      }

      const nextIndex = currentQuestionIndex + 1;
      const hasMore = nextIndex < sessionQuestions.length;

      if (aiResponse) {
        addMessage("erica", aiResponse);
      } else {
        const genericResponses = [
          `That's a solid attempt! ${hasMore ? "Let's keep going." : "You've worked through all the questions!"}`,
          `Good thinking — keep building on that. ${hasMore ? "Ready for the next one?" : ""}`,
          `I like your reasoning. ${hasMore ? "Moving on..." : "We're done — great work!"}`,
        ];
        addMessage("erica", genericResponses[currentQuestionIndex % genericResponses.length]);
      }

      if (completed || (!hasMore && remainingIds.length === 0)) {
        setTimeout(() => {
          setIsCompleted(true);
          addMessage("erica", `🌟 **Excellent!** You've completed the knowledge check for **${module.title}**. Your engagement shows real understanding — you're ready to move on!`);
        }, 1200);
      } else if (hasMore) {
        setCurrentQuestionIndex(nextIndex);
        setTimeout(() => {
          addMessage("erica", `**Question ${nextIndex + 1}/${sessionQuestions.length}:** ${sessionQuestions[nextIndex].text}`);
        }, 1400);
      } else {
        setTimeout(() => {
          setIsCompleted(true);
          addMessage("erica", `🌟 **Excellent!** You've completed the knowledge check for **${module.title}**!`);
        }, 1200);
      }
    } catch {
      addMessage("erica", "Let's keep going — what are your thoughts on that?");
      const nextIndex = currentQuestionIndex + 1;
      if (nextIndex < sessionQuestions.length) {
        setCurrentQuestionIndex(nextIndex);
        setTimeout(() => {
          addMessage("erica", `**Question ${nextIndex + 1}/${sessionQuestions.length}:** ${sessionQuestions[nextIndex].text}`);
        }, 1400);
      } else {
        setIsCompleted(true);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const currentQuestion = sessionQuestions[currentQuestionIndex];
  const progress = sessionQuestions.length > 0
    ? (currentQuestionIndex / sessionQuestions.length) * 100
    : 0;

  if (isInitializing) {
    return (
      <div className="knowledge-check-container">
        <div className="lesson-sidebar">
          <div className="sidebar-header">
            <h2 className="sidebar-title">AI Sparring</h2>
          </div>
        </div>
        <div className="lesson-content">
          <div className="loading-state">
            <div className="spinner" />
            <p style={{ marginTop: "1rem", color: "var(--ink-soft)" }}>Preparing your sparring session…</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="knowledge-check-container">
      <div className="lesson-sidebar">
        <div className="sidebar-header">
          <h2 className="sidebar-title">🥊 AI Spar</h2>
          <p className="sidebar-subtitle">Socratic Learning</p>
        </div>

        <div style={{ padding: "1rem 1.2rem" }}>
          <div style={{ fontSize: "0.8rem", fontWeight: 700, color: "var(--ink-soft)", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: "0.5rem" }}>
            Progress
          </div>
          <div style={{ background: "#e7ddd0", borderRadius: "999px", height: "8px", overflow: "hidden" }}>
            <div style={{ width: `${progress}%`, height: "100%", background: "linear-gradient(90deg, var(--accent-2), var(--accent))", transition: "width 0.6s ease" }} />
          </div>
          <div style={{ marginTop: "0.4rem", fontSize: "0.82rem", color: "var(--ink-soft)" }}>
            {isCompleted ? "Complete! 🎉" : `Question ${currentQuestionIndex + 1} of ${sessionQuestions.length}`}
          </div>
        </div>

        <div className="sparring-info">
          <p className="info-heading">How Erica spars</p>
          <p className="info-text">
            She asks questions from your actual material. Think out loud — uncertainty is fine. She guides, not grades.
          </p>
        </div>

        {currentQuestion?.hints && currentQuestion.hints.length > 0 && !isCompleted && (
          <div style={{ padding: "0 1.2rem" }}>
            <button
              style={{ width: "100%", padding: "0.6rem", background: "rgba(232,95,60,0.08)", border: "1px solid rgba(232,95,60,0.3)", borderRadius: "10px", cursor: "pointer", fontSize: "0.85rem", color: "var(--accent)" }}
              onClick={() => setShowHint(!showHint)}
            >
              {showHint ? "Hide hint" : "💡 Show hint"}
            </button>
            {showHint && (
              <div style={{ marginTop: "0.5rem", padding: "0.7rem", background: "rgba(232,95,60,0.06)", borderRadius: "8px", fontSize: "0.85rem", lineHeight: 1.5, color: "var(--ink-soft)" }}>
                {currentQuestion.hints[0]}
              </div>
            )}
          </div>
        )}
      </div>

      <div className="lesson-content">
        <div className="content-header" style={{ padding: "1rem 1.5rem" }}>
          <h1 style={{ margin: 0, fontSize: "1.3rem", fontWeight: 700 }}>
            Knowledge Check — {module.title}
          </h1>
          <p className="breadcrumb">{module.objective}</p>
        </div>

        <div className="chat-container">
          <div className="chat-messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`chat-message ${msg.role}`}>
                <div className="message-avatar">{msg.role === "erica" ? "🤖" : "👤"}</div>
                <div className="message-content">
                  <div className="message-author">{msg.role === "erica" ? "Erica" : "You"}</div>
                  <div
                    className="message-text"
                    dangerouslySetInnerHTML={{
                      __html: msg.content
                        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                        .replace(/\n/g, "<br/>"),
                    }}
                  />
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="chat-message erica">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="message-author">Erica</div>
                  <div className="message-text" style={{ display: "flex", gap: "4px", alignItems: "center", padding: "0.9rem 1.1rem" }}>
                    <span className="typing-dot" />
                    <span className="typing-dot" style={{ animationDelay: "0.15s" }} />
                    <span className="typing-dot" style={{ animationDelay: "0.3s" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {!isCompleted ? (
            <form className="chat-input-form" onSubmit={handleSubmit}>
              <textarea
                className="chat-input"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your answer… (Enter to send, Shift+Enter for new line)"
                rows={3}
                disabled={isLoading}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e as unknown as React.FormEvent);
                  }
                }}
              />
              <div style={{ display: "flex", gap: "0.8rem", alignItems: "center" }}>
                <span style={{ fontSize: "0.78rem", color: "var(--ink-soft)", flex: 1 }}>
                  Be specific — Erica will guide you deeper
                </span>
                <button
                  className="button primary"
                  type="submit"
                  disabled={isLoading || !inputValue.trim()}
                  style={{ minWidth: "80px" }}
                >
                  {isLoading ? "…" : "Send →"}
                </button>
              </div>
            </form>
          ) : (
            <div className="completion-actions">
              <div style={{ textAlign: "center", marginBottom: "1.2rem" }}>
                <div style={{ fontSize: "3rem", marginBottom: "0.5rem" }}>🎉</div>
                <h3 style={{ margin: "0 0 0.4rem" }}>Knowledge Check Complete!</h3>
                <p style={{ margin: 0, color: "var(--ink-soft)", fontSize: "0.95rem" }}>
                  You&apos;ve demonstrated solid understanding of {module.title}
                </p>
              </div>
              <button
                className="button primary"
                style={{ width: "100%" }}
                onClick={() => onComplete(sessionId || "")}
              >
                Continue to Next Module →
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
