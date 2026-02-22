"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type RawQuestion = {
  id?: string;
  question_id?: string;
  prompt?: string;
  question_text?: string;
  choices?: string[];
};

type Question = {
  id: string;
  prompt: string;
  choices: string[];
};

type RawTestSessionResponse = {
  test_id?: string;
  questions?: RawQuestion[];
  coverage?: {
    module_ids?: string[];
    topics?: string[];
  };
};

type TestSession = {
  test_id: string;
  questions: Question[];
  coverage: {
    module_ids: string[];
    topics: string[];
  };
};

type RawTestSubmitResponse = {
  test_id?: string;
  completed?: boolean;
  message?: string;
  score?: {
    correct?: number;
    total?: number;
    percentage?: number;
  };
  feedback?: {
    summary?: string;
    strong_topics?: string[];
    focus_topics?: string[];
  };
  breakdown?: Array<{
    question_id: string;
    correct: boolean;
    selected: number;
    correct_answer: number;
  }>;
};

type StoredTestResult = {
  test_id: string;
  score: number;
  correct: number;
  total: number;
  breakdown: Array<{
    question_id: string;
    correct: boolean;
    selected: number;
    correct_answer: number;
  }>;
  feedback?: {
    summary?: string;
    strong_topics?: string[];
    focus_topics?: string[];
  };
};

function normalizeQuestion(question: RawQuestion, index: number): Question {
  const rawId = question.id ?? question.question_id;
  const id = typeof rawId === "string" && rawId.trim().length > 0 ? rawId : `q-${index + 1}`;
  const rawPrompt = question.prompt ?? question.question_text;
  const prompt =
    typeof rawPrompt === "string" && rawPrompt.trim().length > 0
      ? rawPrompt
      : `Question ${index + 1}`;
  const choices = Array.isArray(question.choices)
    ? question.choices.filter((choice): choice is string => typeof choice === "string")
    : [];

  return { id, prompt, choices };
}

export default function TestPage() {
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [testSession, setTestSession] = useState<TestSession | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    initializeTest();
  }, []);

  const initializeTest = async () => {
    try {
      const lessonId = sessionStorage.getItem("erica_lesson_id");
      const lessonSnapshot = sessionStorage.getItem("erica_lesson_snapshot");
      let lessonData: unknown = null;

      if (lessonId) {
        const lessonResponse = await fetch(`/api/lesson/${lessonId}`);
        if (lessonResponse.ok) {
          lessonData = await lessonResponse.json();
        }
      }

      if (!lessonData && lessonSnapshot) {
        try {
          lessonData = JSON.parse(lessonSnapshot);
        } catch {
          // Ignore malformed snapshot and surface the primary missing-lesson error below.
        }
      }

      if (!lessonData || typeof lessonData !== "object") {
        setError("No lesson found. Please complete the learning modules first.");
        setStatus("error");
        return;
      }

      const testResponse = await fetch("/api/test/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lesson: lessonData })
      });

      if (!testResponse.ok) {
        throw new Error("Failed to start test");
      }

      const rawTestData = (await testResponse.json()) as RawTestSessionResponse;
      const normalizedQuestions = Array.isArray(rawTestData.questions)
        ? rawTestData.questions.map((question, index) => normalizeQuestion(question, index))
        : [];

      if (!rawTestData.test_id || normalizedQuestions.length === 0) {
        throw new Error("No test questions were generated for this lesson.");
      }

      setTestSession({
        test_id: rawTestData.test_id,
        questions: normalizedQuestions,
        coverage: {
          module_ids: rawTestData.coverage?.module_ids ?? [],
          topics: rawTestData.coverage?.topics ?? []
        }
      });
      setAnswers({});
      setError(null);
      setStatus("ready");
    } catch (err) {
      console.error("Test initialization error:", err);
      setError(err instanceof Error ? err.message : "Failed to initialize test");
      setStatus("error");
    }
  };

  const handleAnswerChange = (questionId: string, choiceIndex: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: choiceIndex }));
  };

  const handleSubmit = async () => {
    if (!testSession) return;

    const answerArray = testSession.questions.map((q) => ({
      question_id: q.id,
      choice_index: answers[q.id] ?? -1
    }));

    try {
      setError(null);
      const response = await fetch("/api/test/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          test_id: testSession.test_id,
          answers: answerArray
        })
      });

      const result = (await response.json()) as RawTestSubmitResponse;

      if (!response.ok) {
        throw new Error(result.message || "Failed to submit test");
      }

      if (!result.completed) {
        setError(result.message || "Please answer all questions before submitting.");
        return;
      }

      const normalizedResult: StoredTestResult = {
        test_id: result.test_id ?? testSession.test_id,
        score: Number(result.score?.percentage ?? 0),
        correct: Number(result.score?.correct ?? 0),
        total: Number(result.score?.total ?? testSession.questions.length),
        breakdown: Array.isArray(result.breakdown) ? result.breakdown : [],
        feedback: result.feedback
      };

      sessionStorage.setItem("erica_test_result", JSON.stringify(normalizedResult));
      router.push("/summary");
    } catch (err) {
      console.error("Test submission error:", err);
      setError(err instanceof Error ? err.message : "Failed to submit test");
    }
  };

  const answeredCount = testSession
    ? testSession.questions.reduce(
        (count, question) => (typeof answers[question.id] === "number" ? count + 1 : count),
        0
      )
    : 0;
  const totalQuestions = testSession?.questions.length || 0;
  const canSubmit = totalQuestions > 0 && answeredCount === totalQuestions;

  if (status === "loading") {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Preparing your test...</h1>
          <p className="hero-sub">Step 4 of 5: Final Assessment</p>
        </header>
        <section className="onboarding-body">
          <div className="loading-state">
            <div className="spinner" />
            <p>Loading test questions...</p>
          </div>
        </section>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Unable to load test</h1>
          <p className="hero-sub">Step 4 of 5: Final Assessment</p>
        </header>
        <section className="onboarding-body">
          <article className="step-card">
            <p className="error">{error}</p>
            <footer className="footer" style={{ marginTop: "1.5rem" }}>
              <button
                type="button"
                className="button secondary"
                onClick={() => router.push("/learn")}
              >
                ← Back to learning
              </button>
            </footer>
          </article>
        </section>
      </main>
    );
  }

  return (
    <main className="onboarding-shell" style={{ maxWidth: "1000px" }}>
      <header className="hero-band">
        <h1 className="hero-title">Final Assessment</h1>
        <p className="hero-sub">Step 4 of 5: Test your knowledge</p>
        <div className="progress-wrap" aria-hidden="true">
          <div className="progress-bar" style={{ width: "80%" }} />
        </div>
      </header>

      <section className="onboarding-body">
        <article className="step-card">
          <h2 className="step-title">Show what you've learned</h2>
          <p className="step-subtitle">
            Answer all {totalQuestions} questions. Feedback will be provided at the end.
          </p>

          <div className="test-questions">
            {testSession?.questions.map((question, idx) => (
              <div key={question.id} className="test-question">
                <h3 className="question-number">Question {idx + 1}</h3>
                <p className="question-text">{question.prompt}</p>
                <div className="question-choices">
                  {question.choices.map((choice, choiceIdx) => (
                    <label key={choiceIdx} className="choice-label">
                      <input
                        type="radio"
                        name={question.id}
                        checked={answers[question.id] === choiceIdx}
                        onChange={() => handleAnswerChange(question.id, choiceIdx)}
                      />
                      <span>{choice}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="test-progress">
            <p className="helper">
              {answeredCount} of {totalQuestions} questions answered
            </p>
            {error && <p className="error" style={{ marginTop: "0.5rem" }}>{error}</p>}
          </div>
        </article>

        <footer className="footer">
          <button
            type="button"
            className="button secondary"
            onClick={() => router.push("/learn")}
          >
            Back
          </button>
          <button
            type="button"
            className="button primary"
            onClick={handleSubmit}
            disabled={!canSubmit}
          >
            Submit test →
          </button>
        </footer>
      </section>
    </main>
  );
}
