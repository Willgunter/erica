"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type TestResult = {
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
};

export default function SummaryPage() {
  const router = useRouter();
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const resultJson = sessionStorage.getItem("erica_test_result");
    if (resultJson) {
      setTestResult(JSON.parse(resultJson));
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Loading your results...</h1>
        </header>
      </main>
    );
  }

  if (!testResult) {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">No test results found</h1>
        </header>
        <section className="onboarding-body">
          <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
            <button
              type="button"
              className="button secondary"
              onClick={() => router.push("/profile")}
            >
              Back to profile
            </button>
            <button
              type="button"
              className="button primary"
              onClick={() => router.push("/learn")}
            >
              Start a new lesson
            </button>
          </div>
        </section>
      </main>
    );
  }

  const percentage = Math.round((testResult.correct / testResult.total) * 100);

  return (
    <main className="onboarding-shell" style={{ maxWidth: "1000px" }}>
      <header className="hero-band">
        <h1 className="hero-title">Lesson Complete! 🎉</h1>
        <p className="hero-sub">Step 5 of 5: Statistical Summary</p>
        <div className="progress-wrap" aria-hidden="true">
          <div className="progress-bar" style={{ width: "100%" }} />
        </div>
      </header>

      <section className="onboarding-body">
        <article className="step-card">
          <div className="summary-score">
            <div className="score-circle">
              <svg width="160" height="160">
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  fill="none"
                  stroke="var(--line)"
                  strokeWidth="12"
                />
                <circle
                  cx="80"
                  cy="80"
                  r="70"
                  fill="none"
                  stroke="var(--accent-2)"
                  strokeWidth="12"
                  strokeDasharray={`${(percentage / 100) * 440} 440`}
                  strokeDashoffset="0"
                  transform="rotate(-90 80 80)"
                  style={{ transition: "stroke-dasharray 1s ease" }}
                />
              </svg>
              <div className="score-label">
                <div className="score-number">{percentage}%</div>
                <div className="score-text">Score</div>
              </div>
            </div>
          </div>

          <div className="summary-stats">
            <div className="stat-card">
              <div className="stat-number">{testResult.correct}</div>
              <div className="stat-label">Correct Answers</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{testResult.total - testResult.correct}</div>
              <div className="stat-label">To Review</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{testResult.total}</div>
              <div className="stat-label">Total Questions</div>
            </div>
          </div>

          <div className="summary-message">
            {percentage >= 80 ? (
              <>
                <h3 className="message-title">Excellent work! 🌟</h3>
                <p className="message-text">
                  You've shown strong mastery of the material. Keep up the great work!
                </p>
              </>
            ) : percentage >= 60 ? (
              <>
                <h3 className="message-title">Good effort! 📚</h3>
                <p className="message-text">
                  You're on the right track. Review the areas you missed and you'll nail it next time.
                </p>
              </>
            ) : (
              <>
                <h3 className="message-title">Keep learning! 💪</h3>
                <p className="message-text">
                  Don't worry - learning takes time. Review the material and try again when you're ready.
                </p>
              </>
            )}
          </div>

          <div className="summary-actions">
            <h3 className="section-heading">What's next?</h3>
            <div className="action-grid">
              <button
                type="button"
                className="action-card"
                onClick={() => router.push("/profile")}
              >
                <span className="action-icon">👤</span>
                <span className="action-title">Back to profile</span>
              </button>
              <button
                type="button"
                className="action-card"
                onClick={() => {
                  sessionStorage.clear();
                  router.push("/upload");
                }}
              >
                <span className="action-icon">📚</span>
                <span className="action-title">Start new lesson</span>
              </button>
              <button
                type="button"
                className="action-card"
                onClick={() => router.push("/learn")}
              >
                <span className="action-icon">🔄</span>
                <span className="action-title">Replay this lesson</span>
              </button>
            </div>
          </div>
        </article>
      </section>
    </main>
  );
}
