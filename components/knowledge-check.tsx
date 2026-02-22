"use client";

import { useState, useEffect, useRef } from "react";

type Checkpoint = {
  checkpoint_id: string;
  module_id: string;
  marker: string;
  questions: string[];
};

type Module = {
  module_id: string;
  title: string;
};

type Lesson = {
  id: string;
};

type Message = {
  id: string;
  role: "erica" | "user";
  content: string;
  timestamp: number;
};

type KnowledgeCheckProps = {
  lesson: Lesson;
  module: Module;
  checkpoint: Checkpoint;
  onComplete: (sessionId: string) => void;
  progress: number;
  moduleNumber: number;
  totalModules: number;
};

export function KnowledgeCheck({
  lesson,
  module,
  checkpoint,
  onComplete,
  progress,
  moduleNumber,
  totalModules
}: KnowledgeCheckProps) {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState("");
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    initializeCheckpoint();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const initializeCheckpoint = async () => {
    try {
      const response = await fetch("/api/checkpoint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lesson: { id: lesson.id },
          module_id: module.module_id
        })
      });

      if (!response.ok) {
        throw new Error("Failed to start knowledge check");
      }

      const data = await response.json();
      setSessionId(data.session_id);

      const welcomeMessage: Message = {
        id: crypto.randomUUID(),
        role: "erica",
        content: `Great work on completing "${module.title}"! Let's reinforce what you learned with a quick knowledge check. I'm here to guide you, not quiz you. Take your time and explain your thinking.`,
        timestamp: Date.now()
      };

      setMessages([welcomeMessage]);
      
      setTimeout(() => {
        askQuestion(0);
      }, 1500);
    } catch (err) {
      console.error("Checkpoint initialization error:", err);
    }
  };

  const askQuestion = (questionIdx: number) => {
    if (questionIdx >= checkpoint.questions.length) {
      handleCheckpointComplete();
      return;
    }

    const questionMessage: Message = {
      id: crypto.randomUUID(),
      role: "erica",
      content: checkpoint.questions[questionIdx],
      timestamp: Date.now()
    };

    setMessages((prev) => [...prev, questionMessage]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userInput.trim() || !sessionId || isProcessing) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: userInput.trim(),
      timestamp: Date.now()
    };

    setMessages((prev) => [...prev, userMessage]);
    setUserInput("");
    setIsProcessing(true);

    try {
      const response = await fetch("/api/checkpoint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          answers: [
            {
              question_id: `q${currentQuestionIndex}`,
              answer: userMessage.content
            }
          ]
        })
      });

      if (!response.ok) {
        throw new Error("Failed to submit answer");
      }

      const data = await response.json();

      setTimeout(() => {
        const feedback = generateFeedback(userMessage.content, currentQuestionIndex);
        const feedbackMessage: Message = {
          id: crypto.randomUUID(),
          role: "erica",
          content: feedback,
          timestamp: Date.now()
        };

        setMessages((prev) => [...prev, feedbackMessage]);

        setTimeout(() => {
          const nextIdx = currentQuestionIndex + 1;
          setCurrentQuestionIndex(nextIdx);
          askQuestion(nextIdx);
        }, 1200);
      }, 800);
    } catch (err) {
      console.error("Answer submission error:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  const generateFeedback = (answer: string, questionIdx: number): string => {
    const feedbacks = [
      [
        "Good start! I can see you're connecting the concepts. Let me help you dig a bit deeper.",
        "Nice explanation! You're on the right track. Can you expand on that a little more?",
        "That's a solid understanding. Let's make sure we connect this to the bigger picture."
      ],
      [
        "Excellent thinking! You're applying what you learned really well.",
        "I like how you're connecting this back to your goals. Keep that up!",
        "Great job relating this to practical use. That's exactly what we want."
      ],
      [
        "That's okay - it's normal to have some uncertainty. Let's talk through it.",
        "I appreciate your honesty. Understanding what you don't know is just as important.",
        "Good awareness! Recognizing areas to revisit is a key part of learning."
      ]
    ];

    const feedbackSet = feedbacks[questionIdx] || feedbacks[0];
    return feedbackSet[Math.floor(Math.random() * feedbackSet.length)];
  };

  const handleCheckpointComplete = () => {
    const completionMessage: Message = {
      id: crypto.randomUUID(),
      role: "erica",
      content: `Fantastic work! You've completed the knowledge check for this module. You're making real progress. Ready to move on?`,
      timestamp: Date.now()
    };

    setMessages((prev) => [...prev, completionMessage]);
    setIsComplete(true);
  };

  const handleContinue = () => {
    if (sessionId) {
      onComplete(sessionId);
    }
  };

  return (
    <main className="knowledge-check-container">
      <aside className="lesson-sidebar">
        <div className="sidebar-header">
          <h2 className="sidebar-title">Knowledge Check</h2>
          <p className="sidebar-subtitle">
            Module {moduleNumber} of {totalModules}
          </p>
        </div>

        <div className="check-progress">
          <div className="progress-circle">
            <svg width="120" height="120">
              <circle
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="var(--line)"
                strokeWidth="8"
              />
              <circle
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="var(--accent-2)"
                strokeWidth="8"
                strokeDasharray={`${(currentQuestionIndex / checkpoint.questions.length) * 314} 314`}
                strokeDashoffset="0"
                transform="rotate(-90 60 60)"
                style={{ transition: "stroke-dasharray 0.5s ease" }}
              />
            </svg>
            <div className="progress-label">
              {currentQuestionIndex} / {checkpoint.questions.length}
            </div>
          </div>
          <p className="helper" style={{ textAlign: "center", marginTop: "1rem" }}>
            Questions answered
          </p>
        </div>

        <div className="sparring-info">
          <h3 className="info-heading">About Knowledge Checks</h3>
          <p className="info-text">
            I'm your AI sparring partner. I'll ask questions and guide you to think through
            concepts, not just test you. This is a conversation, not a quiz.
          </p>
        </div>
      </aside>

      <section className="lesson-content">
        <header className="content-header">
          <div className="progress-wrap">
            <div className="progress-bar" style={{ width: `${progress}%` }} />
          </div>
          <div className="breadcrumb">Knowledge Check · {module.title}</div>
        </header>

        <article className="chat-container">
          <div className="chat-messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`chat-message ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === "erica" ? "🎓" : "👤"}
                </div>
                <div className="message-content">
                  <div className="message-author">
                    {msg.role === "erica" ? "Erica" : "You"}
                  </div>
                  <div className="message-text">{msg.content}</div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {!isComplete && (
            <form className="chat-input-form" onSubmit={handleSubmit}>
              <textarea
                className="chat-input"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                placeholder="Type your response... (Shift+Enter for new line)"
                rows={3}
                disabled={isProcessing}
              />
              <button
                type="submit"
                className="button primary"
                disabled={!userInput.trim() || isProcessing}
              >
                {isProcessing ? "Thinking..." : "Send"}
              </button>
            </form>
          )}

          {isComplete && (
            <div className="completion-actions">
              <button
                type="button"
                className="button primary"
                onClick={handleContinue}
                style={{ width: "100%", padding: "1rem" }}
              >
                {moduleNumber < totalModules ? "Continue to next module →" : "Complete lesson →"}
              </button>
            </div>
          )}
        </article>
      </section>
    </main>
  );
}
