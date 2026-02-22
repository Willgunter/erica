"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Question = {
  question_id: string;
  question_text: string;
  choices: string[];
  correct_answer: number;
};

type TestSession = {
  test_id: string;
  questions: Question[];
  coverage: {
    module_ids: string[];
    topics: string[];
  };
};

export default function TestPage() {
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "ready" | "submitted" | "error">("loading");
  const [testSession, setTestSession] = useState<TestSession | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    initializeTest();
  }, []);

  const initializeTest = async () => {
    try {
      const lessonId = sessionStorage.getItem("erica_lesson_id");
      if (!lessonId) {
        setError("No lesson found. Please complete the learning modules first.");
        setStatus("error");
        return;
      }

      const lessonResponse = await fetch(`/api/lesson/${lessonId}`);
      if (!lessonResponse.ok) {
        throw new Error("Failed to load lesson");
      }

      const lessonData = await lessonResponse.json();

      const testResponse = await fetch("/api/test/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lesson: lessonData })
      });

      if (!testResponse.ok) {
        throw new Error("Failed to start test");
      }

      const testData = await testResponse.json();
      setTestSession(testData);
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
      question_id: q.question_id,
      selected_answer: answers[q.question_id] ?? -1
    }));

    try {
      const response = await fetch("/api/test/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          test_id: testSession.test_id,
          answers: answerArray
        })
      });

      if (!response.ok) {
        throw new Error("Failed to submit test");
      }

      const result = await response.json();
      sessionStorage.setItem("erica_test_result", JSON.stringify(result));
      router.push("/summary");
    } catch (err) {
      console.error("Test submission error:", err);
      setError(err instanceof Error ? err.message : "Failed to submit test");
    }
  };

  const answeredCount = Object.keys(answers).length;
  const totalQuestions = testSession?.questions.length || 0;
  const canSubmit = answeredCount === totalQuestions;

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
              <div key={question.question_id} className="test-question">
                <h3 className="question-number">Question {idx + 1}</h3>
                <p className="question-text">{question.question_text}</p>
                <div className="question-choices">
                  {question.choices.map((choice, choiceIdx) => (
                    <label key={choiceIdx} className="choice-label">
                      <input
                        type="radio"
                        name={question.question_id}
                        checked={answers[question.question_id] === choiceIdx}
                        onChange={() => handleAnswerChange(question.question_id, choiceIdx)}
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
