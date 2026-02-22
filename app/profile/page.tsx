"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type LessonStatus = "completed" | "in_progress" | "queued";

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

type LessonOverview = {
  id: string;
  className: string;
  instructor: string;
  status: LessonStatus;
  needsReview: boolean;
  lastActivity: string;
  progressPct: number;
  nextMilestone: string;
  quizScore: string;
};

const QUIZ_SUMMARY_STORAGE_KEY = "erica_latest_quiz_summary";
const LESSON_HISTORY_STORAGE_KEY = "erica_profile_lesson_history";

const BASE_LESSONS: LessonOverview[] = [
  {
    id: "lesson-physics-101",
    className: "Physics: Kinematics",
    instructor: "Ms. Patel",
    status: "in_progress",
    needsReview: true,
    lastActivity: "2026-02-19T16:00:00.000Z",
    progressPct: 62,
    nextMilestone: "Projectile motion challenge set",
    quizScore: "6/10"
  },
  {
    id: "lesson-algebra-201",
    className: "Algebra II: Quadratics",
    instructor: "Mr. Sanchez",
    status: "completed",
    needsReview: false,
    lastActivity: "2026-02-16T18:30:00.000Z",
    progressPct: 100,
    nextMilestone: "Ready for advanced polynomials",
    quizScore: "9/10"
  },
  {
    id: "lesson-bio-cell",
    className: "Biology: Cell Respiration",
    instructor: "Dr. Kim",
    status: "queued",
    needsReview: false,
    lastActivity: "2026-02-20T12:15:00.000Z",
    progressPct: 15,
    nextMilestone: "Complete Module 2 checkpoint",
    quizScore: "Not taken"
  },
  {
    id: "lesson-history-ww1",
    className: "World History: WWI Causes",
    instructor: "Ms. Howard",
    status: "completed",
    needsReview: true,
    lastActivity: "2026-02-14T10:10:00.000Z",
    progressPct: 100,
    nextMilestone: "Review alliance timeline",
    quizScore: "7/10"
  }
];

function parseQuizSummary(raw: string | null): StoredQuizSummary | null {
  if (!raw) {
    return null;
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") {
      return null;
    }

    const summary = parsed as Partial<StoredQuizSummary>;
    return {
      className: typeof summary.className === "string" ? summary.className : "General Learning",
      completedAt: typeof summary.completedAt === "string" ? summary.completedAt : new Date().toISOString(),
      correctCount: typeof summary.correctCount === "number" ? summary.correctCount : 0,
      incorrectCount: typeof summary.incorrectCount === "number" ? summary.incorrectCount : 0,
      totalCount: typeof summary.totalCount === "number" ? summary.totalCount : 10,
      percentage: typeof summary.percentage === "number" ? summary.percentage : 0,
      needsReview: Boolean(summary.needsReview),
      focusAreas: Array.isArray(summary.focusAreas)
        ? summary.focusAreas.filter((item): item is string => typeof item === "string")
        : []
    };
  } catch {
    return null;
  }
}

function parseQuizHistory(raw: string | null): StoredQuizSummary[] {
  if (!raw) {
    return [];
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed
      .map((item) => parseQuizSummary(JSON.stringify(item)))
      .filter((item): item is StoredQuizSummary => item !== null);
  } catch {
    return [];
  }
}

function formatDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return "Unknown";
  }
  return date.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function statusLabel(status: LessonStatus): string {
  if (status === "in_progress") {
    return "In Progress";
  }
  if (status === "queued") {
    return "Queued";
  }
  return "Completed";
}

export default function ProfilePage() {
  const router = useRouter();
  const [latestSummary, setLatestSummary] = useState<StoredQuizSummary | null>(null);
  const [quizHistory, setQuizHistory] = useState<StoredQuizSummary[]>([]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const latest = parseQuizSummary(window.sessionStorage.getItem(QUIZ_SUMMARY_STORAGE_KEY));
    const history = parseQuizHistory(window.sessionStorage.getItem(LESSON_HISTORY_STORAGE_KEY));
    setLatestSummary(latest);
    setQuizHistory(history);
  }, []);

  const lessons = useMemo(() => {
    const seeded = [...BASE_LESSONS];
    if (!latestSummary) {
      return seeded;
    }

    const latestLesson: LessonOverview = {
      id: `latest-${latestSummary.completedAt}`,
      className: latestSummary.className,
      instructor: "Erica Tutor",
      status: "completed",
      needsReview: latestSummary.needsReview,
      lastActivity: latestSummary.completedAt,
      progressPct: 100,
      nextMilestone: latestSummary.needsReview
        ? "Schedule targeted review session"
        : "Advance to next unit",
      quizScore: `${latestSummary.correctCount}/${latestSummary.totalCount}`
    };

    return [latestLesson, ...seeded];
  }, [latestSummary]);

  const lessonsNeedingReview = useMemo(
    () => lessons.filter((lesson) => lesson.needsReview).length,
    [lessons]
  );
  const completedLessons = useMemo(
    () => lessons.filter((lesson) => lesson.status === "completed").length,
    [lessons]
  );

  return (
    <main className="onboarding-shell">
      <header className="hero-band">
        <h1 className="hero-title">Student profile</h1>
        <p className="hero-sub">Post-lesson dashboard and course progress</p>
        <div className="progress-wrap" aria-hidden="true">
          <div className="progress-bar" style={{ width: "100%" }} />
        </div>
      </header>

      <section className="onboarding-body profile-body">
        <article className="profile-grid">
          <div className="profile-card">
            <p className="label">Student snapshot</p>
            <p className="profile-name">Jordan Rivera</p>
            <p className="profile-line">Track: STEM Acceleration</p>
            <p className="profile-line">Goal: Raise quiz accuracy above 85%</p>
            <p className="profile-line">Current streak: 6 study days</p>
          </div>
          <div className="profile-card">
            <p className="label">Performance at a glance</p>
            <p className="profile-line">Completed lessons: {completedLessons}</p>
            <p className="profile-line">Needs review: {lessonsNeedingReview}</p>
            <p className="profile-line">Practice sessions logged: {quizHistory.length}</p>
            <p className="profile-line">Estimated mastery: 78%</p>
          </div>
        </article>

        {latestSummary && (
          <article className="latest-summary-card">
            <h2 className="step-title">Latest quiz summary</h2>
            <p className="step-subtitle">
              {latestSummary.className} • {formatDate(latestSummary.completedAt)}
            </p>
            <div className="quiz-summary-grid">
              <div className="summary-stat">
                <p className="label">Correct</p>
                <p className="summary-value">{latestSummary.correctCount}</p>
              </div>
              <div className="summary-stat">
                <p className="label">Incorrect</p>
                <p className="summary-value">{latestSummary.incorrectCount}</p>
              </div>
              <div className="summary-stat">
                <p className="label">Accuracy</p>
                <p className="summary-value">{latestSummary.percentage}%</p>
              </div>
            </div>
            {latestSummary.focusAreas.length > 0 && (
              <p className="helper">Focus areas: {latestSummary.focusAreas.join(" | ")}</p>
            )}
          </article>
        )}

        <article className="step-card">
          <h2 className="step-title">All lessons</h2>
          <p className="step-subtitle">
            Includes class name, review status, and progress for each course.
          </p>

          <ul className="lesson-list">
            {lessons.map((lesson) => (
              <li key={lesson.id} className="lesson-card">
                <div className="lesson-top">
                  <div>
                    <p className="lesson-name">{lesson.className}</p>
                    <p className="lesson-meta">
                      Instructor: {lesson.instructor} • Last activity: {formatDate(lesson.lastActivity)}
                    </p>
                  </div>
                  <div className="lesson-badges">
                    <span className={`status-badge status-${lesson.status}`}>
                      {statusLabel(lesson.status)}
                    </span>
                    <span className={`review-badge${lesson.needsReview ? " review-needed" : " review-good"}`}>
                      {lesson.needsReview ? "Needs review" : "On track"}
                    </span>
                  </div>
                </div>

                <div className="progress-row">
                  <div className="course-progress-track" aria-hidden="true">
                    <div className="course-progress-fill" style={{ width: `${lesson.progressPct}%` }} />
                  </div>
                  <p className="progress-text">{lesson.progressPct}% complete</p>
                </div>

                <p className="lesson-meta">Quiz score: {lesson.quizScore}</p>
                <p className="lesson-meta">Next milestone: {lesson.nextMilestone}</p>
              </li>
            ))}
          </ul>
        </article>

        <footer className="footer">
          <button type="button" className="button secondary" onClick={() => router.push("/learn")}>
            Back to learning
          </button>
          <button type="button" className="button primary" onClick={() => router.push("/upload")}>
            Start another lesson
          </button>
        </footer>
      </section>
    </main>
  );
}
