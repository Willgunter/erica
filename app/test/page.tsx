"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { AssessmentQuestion, PracticeTrack } from "@/lib/assessment";
import { inferTrackFromSubject } from "@/lib/assessment-track";

type RawAssessmentStartResponse = {
  attempt_id?: string;
  questions?: AssessmentQuestion[];
};

type RawAssessmentSubmitResponse = {
  attempt_id?: string;
  score?: {
    correct?: number;
    total?: number;
    percentage?: number;
  };
  reviewed_items?: Array<{
    id: string;
    is_correct: boolean;
    question_type: "mcq" | "short_answer" | "open_ended" | "code";
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
};

type ActiveAssessment = {
  attemptId: string;
  questions: AssessmentQuestion[];
};

type ResponseDraft = string | number;

type AttemptStartPayload = {
  lesson_id?: string;
  subject?: string;
  track_override?: PracticeTrack;
};

const SUPABASE_TOKEN_STORAGE_KEY = "supabaseAccessToken";
const DEV_USER_ID_STORAGE_KEY = "supabaseDevUserId";

function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}

function getOrCreateDevUserId() {
  if (typeof window === "undefined") {
    return null;
  }

  const existing = window.localStorage.getItem(DEV_USER_ID_STORAGE_KEY);
  if (existing && isUuid(existing)) {
    return existing;
  }

  if (!window.crypto?.randomUUID) {
    throw new Error("Cannot create local dev identity: browser does not support crypto.randomUUID().");
  }

  const userId = window.crypto.randomUUID();
  window.localStorage.setItem(DEV_USER_ID_STORAGE_KEY, userId);
  return userId;
}

function normalizeLessonData(rawData: unknown): { id?: string; subject?: string } | null {
  if (!rawData || typeof rawData !== "object") {
    return null;
  }

  const data = rawData as { id?: unknown; subject?: unknown };
  return {
    id: typeof data.id === "string" ? data.id : undefined,
    subject: typeof data.subject === "string" ? data.subject : undefined
  };
}

export default function TestPage() {
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");
  const [assessment, setAssessment] = useState<ActiveAssessment | null>(null);
  const [answers, setAnswers] = useState<Record<string, ResponseDraft>>({});
  const [codeLanguages, setCodeLanguages] = useState<Record<string, "javascript" | "python">>({});
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    initializeAssessment();
  }, []);

  const buildHeaders = () => {
    const token = window.localStorage.getItem(SUPABASE_TOKEN_STORAGE_KEY);
    const headers: Record<string, string> = {
      "Content-Type": "application/json"
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    if (process.env.NODE_ENV !== "production") {
      const devUserId = getOrCreateDevUserId();
      if (devUserId) {
        headers["x-dev-user-id"] = devUserId;
      }
    }

    return headers;
  };

  const initializeAssessment = async () => {
    try {
      const lessonId = sessionStorage.getItem("erica_lesson_id");
      const lessonSnapshot = sessionStorage.getItem("erica_lesson_snapshot");
      const normalizedLesson = normalizeLessonData(
        lessonSnapshot ? JSON.parse(lessonSnapshot) : null
      );
      const resolvedLessonId = lessonId || normalizedLesson?.id;

      if (!resolvedLessonId) {
        setError("No lesson found. Please complete the learning modules first.");
        setStatus("error");
        return;
      }

      const subject =
        normalizedLesson?.subject && normalizedLesson.subject.trim().length > 0
          ? normalizedLesson.subject.trim()
          : "General learning";

      const payload: AttemptStartPayload = {
        lesson_id: resolvedLessonId,
        subject
      };

      payload.track_override = inferTrackFromSubject(subject);

      const response = await fetch("/api/assessment/start", {
        method: "POST",
        headers: buildHeaders(),
        body: JSON.stringify(payload)
      });
      const rawStartData = (await response.json()) as RawAssessmentStartResponse & { error?: string };

      if (!response.ok) {
        const failure = rawStartData.error;
        throw new Error(failure ?? "Failed to start the assessment");
      }

      if (!rawStartData.attempt_id || !Array.isArray(rawStartData.questions)) {
        throw new Error("Assessment started without questions.");
      }

      setAssessment({
        attemptId: rawStartData.attempt_id,
        questions: rawStartData.questions
      });
      setAnswers({});
      setError(null);
      setStatus("ready");
    } catch (err) {
      console.error("Assessment initialization error:", err);
      setError(err instanceof Error ? err.message : "Failed to initialize assessment");
      setStatus("error");
    }
  };

  const updateMcqAnswer = (questionId: string, choiceIndex: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: choiceIndex }));
  };

  const updateTextAnswer = (questionId: string, text: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: text }));
  };

  const updateCodeLanguage = (questionId: string, language: "javascript" | "python") => {
    setCodeLanguages((prev) => ({ ...prev, [questionId]: language }));
  };

  const handleSubmit = async () => {
    if (!assessment || isSubmitting) return;

    const responsePayload = {
      attempt_id: assessment.attemptId,
      responses: assessment.questions.map((question) => {
        const answer = answers[question.id];
        if (question.type === "mcq") {
          return {
            question_id: question.id,
            question_type: "mcq" as const,
            selected_index: typeof answer === "number" ? answer : -1
          };
        }

        if (question.type === "short_answer" || question.type === "open_ended") {
          return {
            question_id: question.id,
            question_type: question.type,
            text_response: typeof answer === "string" ? answer : ""
          };
        }

        return {
          question_id: question.id,
          question_type: "code" as const,
          code_submission: typeof answer === "string" ? answer : "",
          language: codeLanguages[question.id] ?? question.default_language
        };
      })
    };

    try {
      setError(null);
      setIsSubmitting(true);
      const response = await fetch("/api/assessment/submit", {
        method: "POST",
        headers: buildHeaders(),
        body: JSON.stringify(responsePayload)
      });

      const result = (await response.json()) as RawAssessmentSubmitResponse;

      if (!response.ok) {
        const failure = (result as { error?: string }).error;

        if (response.status === 409 && failure === "Attempt already submitted") {
          setError("This assessment was already submitted. Redirecting to your results.");
          router.push("/summary");
          return;
        }

        throw new Error(failure ?? "Failed to submit assessment");
      }

      const normalizedResult: StoredTestResult = {
        test_id: result.attempt_id ?? assessment.attemptId,
        score: Number(result.score?.percentage ?? 0),
        correct: Number(result.score?.correct ?? 0),
        total: Number(result.score?.total ?? assessment.questions.length),
        breakdown: Array.isArray(result.reviewed_items)
          ? result.reviewed_items.map((item) => ({
              question_id: item.id,
              correct: Boolean(item.is_correct),
              selected: item.question_type === "mcq" ? 1 : 0,
              correct_answer: item.question_type === "mcq" ? 1 : 0
            }))
          : []
      };

      sessionStorage.setItem("erica_test_result", JSON.stringify(normalizedResult));
      router.push("/summary");
    } catch (err) {
      console.error("Assessment submission error:", err);
      setError(err instanceof Error ? err.message : "Failed to submit assessment");
    } finally {
      setIsSubmitting(false);
    }
  };

  const answeredCount = assessment
    ? assessment.questions.reduce((count, question) => {
        const answer = answers[question.id];
        if (question.type === "mcq") {
          return typeof answer === "number" ? count + 1 : count;
        }

        return typeof answer === "string" && answer.trim().length > 0 ? count + 1 : count;
      }, 0)
    : 0;
  const totalQuestions = assessment?.questions.length || 0;
  const canSubmit = totalQuestions > 0 && answeredCount === totalQuestions;

  const questionTypeLabel = (type: AssessmentQuestion["type"]) => {
    if (type === "mcq") return "Multiple choice";
    if (type === "short_answer") return "Short answer";
    if (type === "open_ended") return "Open response";
    return "Code challenge";
  };

  if (status === "loading") {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Preparing your assessment...</h1>
          <p className="hero-sub">Step 4 of 5: Final Assessment</p>
        </header>
        <section className="onboarding-body">
          <div className="loading-state">
            <div className="spinner" />
            <p>Loading assessment questions...</p>
          </div>
        </section>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Unable to load assessment</h1>
          <p className="hero-sub">Step 4 of 5: Final Assessment</p>
        </header>
        <section className="onboarding-body">
          <article className="step-card">
            <p className="error">{error}</p>
            <footer className="footer" style={{ marginTop: "1.5rem" }}>
              <button type="button" className="button secondary" onClick={() => router.push("/profile")}>
                Back to profile
              </button>
              <button type="button" className="button secondary" onClick={() => router.push("/learn")}>
                ← Back to learn
              </button>
              <button
                type="button"
                className="button primary"
                onClick={() => {
                  setStatus("loading");
                  initializeAssessment();
                }}
              >
                Try again
              </button>
            </footer>
          </article>
        </section>
      </main>
    );
  }

  return (
    <main className="onboarding-shell">
      <header className="hero-band">
        <h1 className="hero-title">Final Assessment</h1>
        <p className="hero-sub">Step 4 of 5: Final Assessment</p>
      </header>

      <section className="onboarding-body">
        <article className="step-card">
          <p className="step-subtitle">
            Answer all {totalQuestions} questions to complete your assessment. Biology tracks use mixed MCQ + written
            response, while computer science uses MCQ + coding.
          </p>

          {error && <p className="error" style={{ marginTop: "0.8rem" }}>{error}</p>}

          <div className="test-questions">
            {assessment?.questions.map((question, index) => (
              <div key={question.id} className="test-question">
                <p className="question-number">
                  Question {index + 1} · {questionTypeLabel(question.type)}
                </p>
                <p className="question-text">{question.prompt}</p>

                {question.type === "mcq" && (
                  <div className="question-choices">
                    {(question.choices || []).map((choice, choiceIndex) => (
                      <label className="choice-label" key={`${question.id}-${choiceIndex}`}>
                        <input
                          type="radio"
                          name={question.id}
                          checked={answers[question.id] === choiceIndex}
                          onChange={() => updateMcqAnswer(question.id, choiceIndex)}
                        />
                        <span>{choice}</span>
                      </label>
                    ))}
                  </div>
                )}

                {(question.type === "short_answer" || question.type === "open_ended") && (
                  <textarea
                    className="written-input"
                    rows={5}
                    value={typeof answers[question.id] === "string" ? answers[question.id] : ""}
                    onChange={(event) => updateTextAnswer(question.id, event.target.value)}
                    placeholder={
                      question.type === "short_answer" ? "Write 2-3 sentences." : "Write your detailed response."
                    }
                  />
                )}

                {question.type === "code" && (
                  <>
                    <textarea
                      className="code-editor"
                      rows={10}
                      value={typeof answers[question.id] === "string" ? answers[question.id] : ""}
                      onChange={(event) => updateTextAnswer(question.id, event.target.value)}
                      placeholder={`Write ${question.default_language?.toUpperCase() ?? "code"} solution...`}
                    />
                    {Array.isArray(question.allowed_languages) && question.allowed_languages.length > 1 && (
                      <div style={{ marginTop: "0.75rem" }}>
                        <label className="label" style={{ display: "block", marginBottom: "0.35rem" }}>
                          Language
                        </label>
                        <select
                          className="input"
                          value={codeLanguages[question.id] ?? question.default_language}
                          onChange={(event) =>
                            updateCodeLanguage(
                              question.id,
                              event.target.value as "javascript" | "python"
                            )
                          }
                        >
                          <option value="javascript">JavaScript</option>
                          <option value="python">Python</option>
                        </select>
                      </div>
                    )}
                  </>
                )}
              </div>
            ))}
          </div>

          <div className="test-progress">
            <p style={{ margin: 0 }}>
              Progress: {answeredCount} / {totalQuestions} answered
            </p>
          </div>

          <footer className="footer" style={{ marginTop: "1.5rem", justifyContent: "flex-end", gap: "0.75rem" }}>
            <button type="button" className="button secondary" onClick={() => router.push("/profile")}>
              Back to profile
            </button>
            <button type="button" className="button secondary" onClick={() => router.push("/learn")}>
              ← Back to learn
            </button>
            <button
              type="button"
              className="button primary"
              onClick={handleSubmit}
              disabled={!canSubmit || isSubmitting}
            >
              {isSubmitting ? "Submitting..." : "Submit Assessment"}
            </button>
          </footer>
        </article>
      </section>
    </main>
  );
}
