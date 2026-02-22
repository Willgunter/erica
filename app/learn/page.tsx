"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type Phase = "sparring" | "quiz" | "results";

type StoredChunk = {
  source?: string;
  text?: string;
};

type QuizQuestion = {
  id: string;
  prompt: string;
  choices: [string, string, string, string];
  correctIndex: number;
  explanation: string;
};

type ReviewedAnswer = {
  questionId: string;
  prompt: string;
  selectedChoice: string;
  correctChoice: string;
  isCorrect: boolean;
  explanation: string;
};

type QuizResult = {
  correctCount: number;
  totalCount: number;
  percentage: number;
  reviewedAnswers: ReviewedAnswer[];
};

type StoredQuizSummary = {
  className: string;
  completedAt: string;
  correctCount: number;
  incorrectCount: number;
  totalCount: number;
  percentage: number;
  needsReview: boolean;
  focusAreas: string[];
};

const QUIZ_SUMMARY_STORAGE_KEY = "erica_latest_quiz_summary";
const LESSON_HISTORY_STORAGE_KEY = "erica_profile_lesson_history";

const QUIZ_QUESTIONS: QuizQuestion[] = [
  {
    id: "q1",
    prompt: "What best describes active recall during studying?",
    choices: [
      "Re-reading notes multiple times",
      "Trying to retrieve ideas from memory before checking notes",
      "Highlighting every key sentence",
      "Watching a lecture at 2x speed"
    ],
    correctIndex: 1,
    explanation: "Active recall means practicing retrieval from memory, not just re-consuming content."
  },
  {
    id: "q2",
    prompt: "Which approach is most aligned with spaced repetition?",
    choices: [
      "Studying once right before the test",
      "Reviewing all material only when confused",
      "Revisiting topics at increasing intervals over time",
      "Focusing only on the easiest topics first"
    ],
    correctIndex: 2,
    explanation: "Spaced repetition schedules reviews across time, usually with widening intervals."
  },
  {
    id: "q3",
    prompt: "A useful way to check true understanding is to:",
    choices: [
      "Explain the idea in your own words with an example",
      "Copy definitions exactly from notes",
      "Memorize headings only",
      "Skip questions until the end"
    ],
    correctIndex: 0,
    explanation: "Explaining concepts in your own words exposes gaps in reasoning."
  },
  {
    id: "q4",
    prompt: "If a learner misses a question, the best immediate step is usually to:",
    choices: [
      "Move on and avoid the topic",
      "Retry blindly until lucky",
      "Review why the answer was wrong and attempt a similar question",
      "Change topics permanently"
    ],
    correctIndex: 2,
    explanation: "Error-focused review plus a similar follow-up question improves retention."
  },
  {
    id: "q5",
    prompt: "What is the main goal of a checkpoint question in a lesson?",
    choices: [
      "To rank students publicly",
      "To test only trivia facts",
      "To diagnose understanding before moving forward",
      "To replace instruction entirely"
    ],
    correctIndex: 2,
    explanation: "Checkpoints are diagnostic and guide next steps in learning."
  },
  {
    id: "q6",
    prompt: "Which practice most improves transfer to new problems?",
    choices: [
      "Solving only one identical question type",
      "Mixing related problem types and identifying differences",
      "Studying with no feedback",
      "Ignoring conceptual explanations"
    ],
    correctIndex: 1,
    explanation: "Interleaving related problem types supports flexible application."
  },
  {
    id: "q7",
    prompt: "What is the best reason to delay feedback until after a full quiz submission?",
    choices: [
      "To reduce server costs",
      "To keep question order secret",
      "To prevent answer leakage during the same attempt",
      "To make the interface look simpler"
    ],
    correctIndex: 2,
    explanation: "Withheld feedback reduces contamination from earlier items in the same attempt."
  },
  {
    id: "q8",
    prompt: "A strong learning session should include:",
    choices: [
      "Only passive reading",
      "A cycle of learning, retrieval, and reflection",
      "No breaks, regardless of fatigue",
      "Skipping practice to save time"
    ],
    correctIndex: 1,
    explanation: "The cycle of study, retrieval practice, and reflection drives durable learning."
  },
  {
    id: "q9",
    prompt: "When confidence is high but accuracy is low, this usually indicates:",
    choices: [
      "Good calibration",
      "Overconfidence and shallow verification",
      "A perfect study plan",
      "That no more practice is needed"
    ],
    correctIndex: 1,
    explanation: "Miscalibration appears when confidence is not validated by performance."
  },
  {
    id: "q10",
    prompt: "What is the best next step after finishing a quiz?",
    choices: [
      "Ignore results and start a new topic",
      "Only celebrate correct answers",
      "Review misses, target weak areas, and retest later",
      "Delete prior notes"
    ],
    correctIndex: 2,
    explanation: "Post-quiz review should convert misses into a focused follow-up plan."
  }
];

if (QUIZ_QUESTIONS.length !== 10) {
  throw new Error("QUIZ_QUESTIONS must contain exactly 10 questions.");
}

function parseStoredChunks(raw: string | null): StoredChunk[] {
  if (!raw) {
    return [];
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed
      .filter((entry): entry is StoredChunk => typeof entry === "object" && entry !== null)
      .map((entry) => ({
        source: typeof entry.source === "string" ? entry.source : undefined,
        text: typeof entry.text === "string" ? entry.text : undefined
      }));
  } catch {
    return [];
  }
}

function parseStoredQuizSummary(raw: string | null): StoredQuizSummary[] {
  if (!raw) {
    return [];
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed
      .filter((entry): entry is StoredQuizSummary => typeof entry === "object" && entry !== null)
      .map((entry) => ({
        className: typeof entry.className === "string" ? entry.className : "General Learning",
        completedAt: typeof entry.completedAt === "string" ? entry.completedAt : new Date().toISOString(),
        correctCount: typeof entry.correctCount === "number" ? entry.correctCount : 0,
        incorrectCount: typeof entry.incorrectCount === "number" ? entry.incorrectCount : 0,
        totalCount: typeof entry.totalCount === "number" ? entry.totalCount : 10,
        percentage: typeof entry.percentage === "number" ? entry.percentage : 0,
        needsReview: Boolean(entry.needsReview),
        focusAreas: Array.isArray(entry.focusAreas)
          ? entry.focusAreas.filter((item): item is string => typeof item === "string")
          : []
      }));
  } catch {
    return [];
  }
}

function deriveClassName(chunks: StoredChunk[]): string {
  if (chunks.length === 0) {
    return "General Learning";
  }

  const first = chunks[0];
  const source = (first.source ?? "").trim();
  if (source && source.toLowerCase() !== "topic") {
    return source.replace(/\.[^/.]+$/, "");
  }

  const text = (first.text ?? "").trim();
  if (!text) {
    return "General Learning";
  }
  return text.slice(0, 48);
}

function phaseMeta(phase: Phase): { stepLabel: string; progress: string; title: string } {
  if (phase === "sparring") {
    return {
      stepLabel: "Step 3 of 5: Sparring",
      progress: "60%",
      title: "Sparring Partner / General Learning"
    };
  }
  if (phase === "quiz") {
    return {
      stepLabel: "Step 4 of 5: Quizzes and tests",
      progress: "80%",
      title: "Course quiz (10 hardcoded questions)"
    };
  }
  return {
    stepLabel: "Step 5 of 5: Results",
    progress: "100%",
    title: "Quiz results"
  };
}

export default function LearnPage() {
  const router = useRouter();
  const [phase, setPhase] = useState<Phase>("sparring");
  const [storedChunks, setStoredChunks] = useState<StoredChunk[]>([]);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [quizError, setQuizError] = useState<string | null>(null);
  const [result, setResult] = useState<QuizResult | null>(null);
  const [redirectSeconds, setRedirectSeconds] = useState<number | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const raw = window.sessionStorage.getItem("erica_content_chunks");
    setStoredChunks(parseStoredChunks(raw));
  }, []);

  const meta = useMemo(() => phaseMeta(phase), [phase]);

  const answeredCount = useMemo(() => {
    return QUIZ_QUESTIONS.filter((question) => answers[question.id] !== undefined).length;
  }, [answers]);

  useEffect(() => {
    if (phase !== "results" || !result) {
      setRedirectSeconds(null);
      return;
    }

    setRedirectSeconds(7);
    const timer = window.setInterval(() => {
      setRedirectSeconds((previous) => {
        if (previous === null) {
          return previous;
        }
        if (previous <= 1) {
          window.clearInterval(timer);
          router.push("/profile");
          return 0;
        }
        return previous - 1;
      });
    }, 1000);

    return () => window.clearInterval(timer);
  }, [phase, result, router]);

  function setAnswer(questionId: string, choiceIndex: number) {
    setAnswers((prev) => ({ ...prev, [questionId]: choiceIndex }));
    setQuizError(null);
  }

  function startQuiz() {
    setPhase("quiz");
    setQuizError(null);
  }

  function submitQuiz() {
    if (answeredCount < QUIZ_QUESTIONS.length) {
      const remaining = QUIZ_QUESTIONS.length - answeredCount;
      setQuizError(`Answer all 10 questions before submitting. ${remaining} remaining.`);
      return;
    }

    const reviewedAnswers: ReviewedAnswer[] = QUIZ_QUESTIONS.map((question) => {
      const selectedIndex = answers[question.id] ?? -1;
      return {
        questionId: question.id,
        prompt: question.prompt,
        selectedChoice: question.choices[selectedIndex] ?? "No answer",
        correctChoice: question.choices[question.correctIndex],
        isCorrect: selectedIndex === question.correctIndex,
        explanation: question.explanation
      };
    });

    const correctCount = reviewedAnswers.filter((item) => item.isCorrect).length;
    const totalCount = QUIZ_QUESTIONS.length;
    const percentage = Number(((correctCount / totalCount) * 100).toFixed(1));
    const incorrectCount = totalCount - correctCount;
    const focusAreas = reviewedAnswers.filter((item) => !item.isCorrect).map((item) => item.prompt);

    if (typeof window !== "undefined") {
      const summary: StoredQuizSummary = {
        className: deriveClassName(storedChunks),
        completedAt: new Date().toISOString(),
        correctCount,
        incorrectCount,
        totalCount,
        percentage,
        needsReview: percentage < 80,
        focusAreas: focusAreas.slice(0, 3)
      };

      window.sessionStorage.setItem(QUIZ_SUMMARY_STORAGE_KEY, JSON.stringify(summary));

      const existing = parseStoredQuizSummary(window.sessionStorage.getItem(LESSON_HISTORY_STORAGE_KEY));
      const nextHistory = [summary, ...existing].slice(0, 12);
      window.sessionStorage.setItem(LESSON_HISTORY_STORAGE_KEY, JSON.stringify(nextHistory));
    }

    setResult({
      correctCount,
      totalCount,
      percentage,
      reviewedAnswers
    });
    setPhase("results");
    setQuizError(null);
  }

  function retakeQuiz() {
    setAnswers({});
    setResult(null);
    setQuizError(null);
    setRedirectSeconds(null);
    setPhase("quiz");
  }

  return (
    <main className="onboarding-shell">
      <header className="hero-band">
        <h1 className="hero-title">{meta.title}</h1>
        <p className="hero-sub">{meta.stepLabel}</p>
        <div className="progress-wrap" aria-hidden="true">
          <div className="progress-bar" style={{ width: meta.progress }} />
        </div>
      </header>

      <section className="onboarding-body learn-body">
        {phase === "sparring" && (
          <article className="step-card">
            <h2 className="step-title">General learning phase (stub)</h2>
            <p className="step-subtitle">
              This screen is a temporary stub for the sparring partner experience. Replace this
              section with the real tutoring interaction later.
            </p>

            <div className="sparring-stub">
              <p className="label">Current behavior</p>
              <ul className="stub-list">
                <li>Shows placeholder sparring prompts</li>
                <li>Loads submitted content context from session storage</li>
                <li>Lets the student continue to the quiz phase</li>
              </ul>
            </div>

            {storedChunks.length > 0 && (
              <div className="context-preview">
                <p className="label">Learning context snapshot</p>
                <ul className="context-list">
                  {storedChunks.slice(0, 5).map((chunk, index) => (
                    <li key={`${chunk.source ?? "topic"}-${index}`} className="context-item">
                      <strong>{chunk.source ?? "topic"}:</strong>{" "}
                      {(chunk.text ?? "").slice(0, 140) || "No text found"}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="transcript-shell">
              <p className="label">Stub transcript</p>
              <div className="transcript-line transcript-line-ai">
                Tutor: Explain the concept in your own words and identify one point of confusion.
              </div>
              <div className="transcript-line transcript-line-user">
                Student: I can describe the basics, but I still mix up when to apply the method.
              </div>
              <div className="transcript-line transcript-line-ai">
                Tutor: Good. We will lock that in with a short quiz next.
              </div>
            </div>

            <footer className="footer">
              <button type="button" className="button secondary" onClick={() => router.push("/upload")}>
                Back
              </button>
              <button type="button" className="button primary" onClick={startQuiz}>
                Continue to quiz
              </button>
            </footer>
          </article>
        )}

        {phase === "quiz" && (
          <article className="step-card">
            <h2 className="step-title">Quizzes and tests phase</h2>
            <p className="step-subtitle">
              Answer all 10 hardcoded questions. Feedback appears after full submission.
            </p>

            <p className="helper">
              Progress: {answeredCount}/10 answered
            </p>

            <form
              className="quiz-form"
              onSubmit={(event) => {
                event.preventDefault();
                submitQuiz();
              }}
            >
              {QUIZ_QUESTIONS.map((question, index) => (
                <fieldset key={question.id} className="question-card">
                  <legend className="question-prompt">
                    {index + 1}. {question.prompt}
                  </legend>
                  <div className="question-options">
                    {question.choices.map((choice, choiceIndex) => {
                      const checked = answers[question.id] === choiceIndex;
                      return (
                        <label key={`${question.id}-${choiceIndex}`} className={`choice${checked ? " active" : ""}`}>
                          <input
                            type="radio"
                            name={question.id}
                            checked={checked}
                            onChange={() => setAnswer(question.id, choiceIndex)}
                          />
                          <span>{choice}</span>
                        </label>
                      );
                    })}
                  </div>
                </fieldset>
              ))}

              {quizError && <p className="error">{quizError}</p>}

              <footer className="footer">
                <button type="button" className="button secondary" onClick={() => setPhase("sparring")}>
                  Back to sparring
                </button>
                <button type="submit" className="button primary">
                  Submit quiz
                </button>
              </footer>
            </form>
          </article>
        )}

        {phase === "results" && result && (
          <article className="step-card">
            <h2 className="step-title">Quiz complete</h2>
            <p className="step-subtitle">
              Score: {result.correctCount}/{result.totalCount} ({result.percentage}%)
            </p>

            <div className="quiz-summary-grid">
              <div className="summary-stat">
                <p className="label">Correct</p>
                <p className="summary-value">{result.correctCount}</p>
              </div>
              <div className="summary-stat">
                <p className="label">Incorrect</p>
                <p className="summary-value">{result.totalCount - result.correctCount}</p>
              </div>
              <div className="summary-stat">
                <p className="label">Accuracy</p>
                <p className="summary-value">{result.percentage}%</p>
              </div>
            </div>

            {redirectSeconds !== null && (
              <p className="helper">Redirecting to your profile in {redirectSeconds}s...</p>
            )}

            <ul className="result-list">
              {result.reviewedAnswers.map((item, index) => (
                <li key={item.questionId} className={`result-item${item.isCorrect ? " correct" : " incorrect"}`}>
                  <p className="result-prompt">
                    {index + 1}. {item.prompt}
                  </p>
                  <p className="result-answer">Your answer: {item.selectedChoice}</p>
                  {!item.isCorrect && <p className="result-answer">Correct answer: {item.correctChoice}</p>}
                  <p className="result-explanation">{item.explanation}</p>
                </li>
              ))}
            </ul>

            <footer className="footer">
              <button type="button" className="button secondary" onClick={retakeQuiz}>
                Retake quiz
              </button>
              <button type="button" className="button primary" onClick={() => router.push("/profile")}>
                Go to profile now
              </button>
            </footer>
          </article>
        )}
      </section>
    </main>
  );
}
