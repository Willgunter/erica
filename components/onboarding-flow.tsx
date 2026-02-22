"use client";

import { useMemo, useState } from "react";
import type { AccessibilitySettings, ProfileInput } from "@/lib/profile";

type StudyTime = "15_min" | "30_min" | "45_min" | "60_min_plus";
type Pacing = "light" | "steady" | "accelerated";
type TeachingStyle = "visual" | "socratic" | "project_based" | "mixed" | "not_sure";
type ContentFormat = "text" | "video" | "interactive" | "audio" | "flashcards";
type ReviewPreference = "spaced_repetition" | "practice_quiz" | "reflection" | "teach_back";

type DraftProfile = {
  subject: string;
  goals: string[];
  studyTime: StudyTime;
  pacing: Pacing;
  teachingStyle: TeachingStyle;
  contentFormats: ContentFormat[];
  reviewPreferences: ReviewPreference[];
  accessibility: AccessibilitySettings;
};

const STEP_TITLES = [
  "Start profile",
  "Time and pacing",
  "Learning preferences",
  "Accessibility"
] as const;

const GOAL_CHOICES = [
  "Pass a class",
  "Prepare for an exam",
  "Build foundational knowledge",
  "Move faster through material",
  "Stay consistent"
] as const;

const CONTENT_CHOICES: Array<{ key: ContentFormat; label: string; detail: string }> = [
  { key: "text", label: "Text", detail: "Short reads and notes" },
  { key: "video", label: "Video", detail: "Explainers and walkthroughs" },
  { key: "interactive", label: "Interactive", detail: "Click-through problem solving" },
  { key: "audio", label: "Audio", detail: "Listen while multitasking" },
  { key: "flashcards", label: "Flashcards", detail: "Fast recall loops" }
];

const REVIEW_CHOICES: Array<{ key: ReviewPreference; label: string; detail: string }> = [
  { key: "spaced_repetition", label: "Spaced repetition", detail: "Review right before you forget" },
  { key: "practice_quiz", label: "Practice quiz", detail: "Frequent low-stakes checks" },
  { key: "reflection", label: "Reflection", detail: "Short recap prompts" },
  { key: "teach_back", label: "Teach-back", detail: "Explain concepts in your own words" }
];

const STUDY_TIME_CHOICES: Array<{ key: StudyTime; label: string; detail: string }> = [
  { key: "15_min", label: "15 minutes", detail: "Micro-session mode" },
  { key: "30_min", label: "30 minutes", detail: "Balanced daily pace" },
  { key: "45_min", label: "45 minutes", detail: "Focused depth" },
  { key: "60_min_plus", label: "60+ minutes", detail: "High-intensity track" }
];

const PACING_CHOICES: Array<{ key: Pacing; label: string; detail: string }> = [
  { key: "light", label: "Light", detail: "Steady confidence building" },
  { key: "steady", label: "Steady", detail: "Default challenge level" },
  { key: "accelerated", label: "Accelerated", detail: "Faster advancement" }
];

const TEACHING_STYLE_CHOICES: Array<{ key: TeachingStyle; label: string; detail: string }> = [
  { key: "visual", label: "Visual", detail: "Diagrams and mapped concepts" },
  { key: "socratic", label: "Socratic", detail: "Guided questions" },
  { key: "project_based", label: "Project-based", detail: "Learn by doing" },
  { key: "mixed", label: "Mixed", detail: "Blend styles" },
  { key: "not_sure", label: "Not sure", detail: "We adapt as we learn" }
];

const ACCESSIBILITY_CHOICES: Array<{ key: keyof AccessibilitySettings; label: string }> = [
  { key: "captions", label: "Captions by default" },
  { key: "highContrast", label: "High contrast visuals" },
  { key: "reduceMotion", label: "Reduced motion" },
  { key: "dyslexiaFriendlyFont", label: "Dyslexia-friendly font" },
  { key: "screenReaderOptimized", label: "Screen reader optimized" }
];

const defaultDraft: DraftProfile = {
  subject: "",
  goals: [],
  studyTime: "30_min",
  pacing: "steady",
  teachingStyle: "not_sure",
  contentFormats: ["text", "interactive"],
  reviewPreferences: ["practice_quiz"],
  accessibility: {
    captions: false,
    highContrast: false,
    reduceMotion: false,
    dyslexiaFriendlyFont: false,
    screenReaderOptimized: false
  }
};

function toggleChoice<T extends string>(values: T[], key: T) {
  if (values.includes(key)) {
    return values.filter((value) => value !== key);
  }
  return [...values, key];
}

export function OnboardingFlow() {
  const totalSteps = STEP_TITLES.length;
  const [stepIndex, setStepIndex] = useState(0);
  const [draft, setDraft] = useState<DraftProfile>(defaultDraft);
  const [customGoal, setCustomGoal] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "saving" | "done">("idle");
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const progress = useMemo(() => ((stepIndex + 1) / totalSteps) * 100, [stepIndex, totalSteps]);

  function addCustomGoal() {
    const value = customGoal.trim();
    if (!value) {
      return;
    }
    if (draft.goals.includes(value)) {
      setCustomGoal("");
      return;
    }
    setDraft((prev) => ({ ...prev, goals: [...prev.goals, value] }));
    setCustomGoal("");
  }

  function validateCurrentStep() {
    if (stepIndex === 0 && draft.subject.trim().length === 0) {
      setError("Choose a subject area so we can start tailoring lessons.");
      return false;
    }
    setError(null);
    return true;
  }

  function goNext() {
    if (!validateCurrentStep()) {
      return;
    }
    setStepIndex((prev) => Math.min(prev + 1, totalSteps - 1));
  }

  function goBack() {
    setError(null);
    setStepIndex((prev) => Math.max(prev - 1, 0));
  }

  async function submitProfile() {
    if (!validateCurrentStep()) {
      return;
    }

    setStatus("saving");
    setError(null);

    const payload: ProfileInput = {
      subject: draft.subject,
      goals: draft.goals,
      studyTime: draft.studyTime,
      pacing: draft.pacing,
      teachingStyle: draft.teachingStyle,
      contentFormats: draft.contentFormats,
      reviewPreferences: draft.reviewPreferences,
      accessibility: draft.accessibility
    };

    const token = typeof window !== "undefined" ? window.localStorage.getItem("supabaseAccessToken") : null;

    try {
      const response = await fetch("/api/profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify(payload)
      });

      const data = (await response.json()) as {
        error?: string;
        profile?: Record<string, unknown>;
      };

      if (!response.ok) {
        throw new Error(data.error ?? "Failed to save profile");
      }

      setResult(data.profile ?? null);
      setStatus("done");
    } catch (submissionError) {
      const message =
        submissionError instanceof Error
          ? submissionError.message
          : "Could not save profile. Try again in a moment.";
      setError(message);
      setStatus("idle");
    }
  }

  return (
    <main className="onboarding-shell">
      <header className="hero-band">
        <h1 className="hero-title">Build your learning profile in under 2 minutes</h1>
        <p className="hero-sub">
          Step {stepIndex + 1} of {totalSteps}: {STEP_TITLES[stepIndex]}
        </p>
        <div className="progress-wrap" aria-hidden="true">
          <div className="progress-bar" style={{ width: `${progress}%` }} />
        </div>
      </header>

      <section className="onboarding-body">
        {stepIndex === 0 && (
          <article className="step-card">
            <h2 className="step-title">What are you studying?</h2>
            <p className="step-subtitle">Give us just enough context to personalize your first lesson path.</p>

            <label className="field">
              <span className="label">Subject</span>
              <input
                className="input"
                value={draft.subject}
                onChange={(event) => setDraft((prev) => ({ ...prev, subject: event.target.value }))}
                placeholder="Examples: Algebra, Biology, AP History"
                maxLength={80}
              />
            </label>

            <div className="field">
              <span className="label">Goals</span>
              <div className="chips" role="list" aria-label="Goal choices">
                {GOAL_CHOICES.map((goal) => {
                  const active = draft.goals.includes(goal);
                  return (
                    <button
                      type="button"
                      key={goal}
                      className={`chip ${active ? "active" : ""}`}
                      onClick={() =>
                        setDraft((prev) => ({
                          ...prev,
                          goals: toggleChoice(prev.goals, goal)
                        }))
                      }
                    >
                      {goal}
                    </button>
                  );
                })}
              </div>

              <div style={{ display: "flex", gap: "0.5rem" }}>
                <input
                  className="input"
                  value={customGoal}
                  onChange={(event) => setCustomGoal(event.target.value)}
                  placeholder="Add your own goal"
                  maxLength={120}
                />
                <button type="button" className="button secondary" onClick={addCustomGoal}>
                  Add
                </button>
              </div>
            </div>
          </article>
        )}

        {stepIndex === 1 && (
          <article className="step-card">
            <h2 className="step-title">How much time can you spend each day?</h2>
            <p className="step-subtitle">We use this to tune lesson size and review cadence.</p>

            <div className="field">
              <span className="label">Study time</span>
              <div className="grid">
                {STUDY_TIME_CHOICES.map((option) => (
                  <button
                    key={option.key}
                    type="button"
                    className={`option ${draft.studyTime === option.key ? "active" : ""}`}
                    onClick={() => setDraft((prev) => ({ ...prev, studyTime: option.key }))}
                  >
                    <span className="top">{option.label}</span>
                    <small>{option.detail}</small>
                  </button>
                ))}
              </div>
            </div>

            <div className="field">
              <span className="label">Pacing</span>
              <div className="grid">
                {PACING_CHOICES.map((option) => (
                  <button
                    key={option.key}
                    type="button"
                    className={`option ${draft.pacing === option.key ? "active" : ""}`}
                    onClick={() => setDraft((prev) => ({ ...prev, pacing: option.key }))}
                  >
                    <span className="top">{option.label}</span>
                    <small>{option.detail}</small>
                  </button>
                ))}
              </div>
            </div>
          </article>
        )}

        {stepIndex === 2 && (
          <article className="step-card">
            <h2 className="step-title">How do you like to learn?</h2>
            <p className="step-subtitle">Choose what feels right now. You can update this anytime.</p>

            <div className="field">
              <span className="label">Teaching style</span>
              <div className="grid">
                {TEACHING_STYLE_CHOICES.map((style) => (
                  <button
                    key={style.key}
                    type="button"
                    className={`option ${draft.teachingStyle === style.key ? "active" : ""}`}
                    onClick={() =>
                      setDraft((prev) => ({
                        ...prev,
                        teachingStyle: style.key
                      }))
                    }
                  >
                    <span className="top">{style.label}</span>
                    <small>{style.detail}</small>
                  </button>
                ))}
              </div>
            </div>

            <div className="field">
              <span className="label">Content formats</span>
              <div className="grid">
                {CONTENT_CHOICES.map((option) => (
                  <button
                    key={option.key}
                    type="button"
                    className={`option ${draft.contentFormats.includes(option.key) ? "active" : ""}`}
                    onClick={() =>
                      setDraft((prev) => ({
                        ...prev,
                        contentFormats: toggleChoice(prev.contentFormats, option.key)
                      }))
                    }
                  >
                    <span className="top">{option.label}</span>
                    <small>{option.detail}</small>
                  </button>
                ))}
              </div>
            </div>

            <div className="field">
              <span className="label">Review preferences</span>
              <div className="grid">
                {REVIEW_CHOICES.map((option) => (
                  <button
                    key={option.key}
                    type="button"
                    className={`option ${draft.reviewPreferences.includes(option.key) ? "active" : ""}`}
                    onClick={() =>
                      setDraft((prev) => ({
                        ...prev,
                        reviewPreferences: toggleChoice(prev.reviewPreferences, option.key)
                      }))
                    }
                  >
                    <span className="top">{option.label}</span>
                    <small>{option.detail}</small>
                  </button>
                ))}
              </div>
            </div>
          </article>
        )}

        {stepIndex === 3 && (
          <article className="step-card">
            <h2 className="step-title">Accessibility and final check</h2>
            <p className="step-subtitle">Select anything that helps us deliver a better experience.</p>

            <div className="checkbox-row">
              {ACCESSIBILITY_CHOICES.map((option) => (
                <label key={option.key} className="checkbox-card">
                  <input
                    type="checkbox"
                    checked={draft.accessibility[option.key]}
                    onChange={() =>
                      setDraft((prev) => ({
                        ...prev,
                        accessibility: {
                          ...prev.accessibility,
                          [option.key]: !prev.accessibility[option.key]
                        }
                      }))
                    }
                  />
                  <span>{option.label}</span>
                </label>
              ))}
            </div>

            <p className="helper">
              Submission requires a signed-in Supabase session token in <code>localStorage.supabaseAccessToken</code>
              or a dev header from your test client.
            </p>

            {result && (
              <div className="code-block" aria-live="polite">
                {JSON.stringify(result, null, 2)}
              </div>
            )}
          </article>
        )}

        {error && <p className="error">{error}</p>}
        {status === "done" && <p className="ok">Profile saved. Personalization is ready.</p>}

        <footer className="footer">
          <button
            type="button"
            className="button secondary"
            onClick={goBack}
            disabled={stepIndex === 0 || status === "saving"}
          >
            Back
          </button>

          {stepIndex < totalSteps - 1 ? (
            <button type="button" className="button primary" onClick={goNext}>
              Next
            </button>
          ) : (
            <button
              type="button"
              className="button primary"
              onClick={submitProfile}
              disabled={status === "saving"}
            >
              {status === "saving" ? "Saving..." : "Save profile"}
            </button>
          )}
        </footer>
      </section>
    </main>
  );
}
