"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import type { PracticeTrack } from "@/lib/assessment";

type LessonStatus = "completed" | "in_progress" | "queued";

type SectionScore = {
  label: string;
  correct: number;
  total: number;
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
  practiceTrack: PracticeTrack;
  examStyle: string;
  sectionScores: SectionScore[];
  recommendations: string[];
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

type TrackStat = {
  track: PracticeTrack;
  attempts: number;
  average: number;
};

type FormatStat = {
  label: string;
  correct: number;
  total: number;
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

function parseSectionScores(value: unknown): SectionScore[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .filter((entry): entry is SectionScore => typeof entry === "object" && entry !== null)
    .map((entry) => ({
      label: typeof entry.label === "string" ? entry.label : "Section",
      correct: typeof entry.correct === "number" ? entry.correct : 0,
      total: typeof entry.total === "number" ? entry.total : 0
    }));
}

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
      totalCount: typeof summary.totalCount === "number" ? summary.totalCount : 0,
      percentage: typeof summary.percentage === "number" ? summary.percentage : 0,
      needsReview: Boolean(summary.needsReview),
      focusAreas: Array.isArray(summary.focusAreas)
        ? summary.focusAreas.filter((item): item is string => typeof item === "string")
        : [],
      practiceTrack:
        summary.practiceTrack === "computer_science" ||
        summary.practiceTrack === "biology" ||
        summary.practiceTrack === "general"
          ? summary.practiceTrack
          : "general",
      examStyle: typeof summary.examStyle === "string" ? summary.examStyle : "Multiple choice",
      sectionScores: parseSectionScores(summary.sectionScores),
      recommendations: Array.isArray(summary.recommendations)
        ? summary.recommendations.filter((item): item is string => typeof item === "string")
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
      .map((entry) => parseQuizSummary(JSON.stringify(entry)))
      .filter((entry): entry is StoredQuizSummary => entry !== null);
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

function trackLabel(track: PracticeTrack): string {
  if (track === "computer_science") {
    return "Computer science";
  }
  if (track === "biology") {
    return "Biology";
  }
  return "General learning";
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
      nextMilestone: latestSummary.needsReview ? "Schedule targeted review session" : "Advance to next unit",
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

  const trendSeries = useMemo(() => {
    return [...quizHistory].slice(0, 8).reverse();
  }, [quizHistory]);

  const averageAccuracy = useMemo(() => {
    if (quizHistory.length === 0) {
      return 0;
    }

    const total = quizHistory.reduce((sum, entry) => sum + entry.percentage, 0);
    return Number((total / quizHistory.length).toFixed(1));
  }, [quizHistory]);

  const trackStats = useMemo<TrackStat[]>(() => {
    const acc = new Map<PracticeTrack, { attempts: number; totalPct: number }>();

    for (const entry of quizHistory) {
      const current = acc.get(entry.practiceTrack) ?? { attempts: 0, totalPct: 0 };
      current.attempts += 1;
      current.totalPct += entry.percentage;
      acc.set(entry.practiceTrack, current);
    }

    return Array.from(acc.entries())
      .map(([track, value]) => ({
        track,
        attempts: value.attempts,
        average: Number((value.totalPct / value.attempts).toFixed(1))
      }))
      .sort((a, b) => b.attempts - a.attempts);
  }, [quizHistory]);

  const formatStats = useMemo<FormatStat[]>(() => {
    const acc = new Map<string, { correct: number; total: number }>();

    for (const entry of quizHistory) {
      for (const section of entry.sectionScores) {
        const current = acc.get(section.label) ?? { correct: 0, total: 0 };
        current.correct += section.correct;
        current.total += section.total;
        acc.set(section.label, current);
      }
    }

    return Array.from(acc.entries())
      .map(([label, value]) => ({
        label,
        correct: value.correct,
        total: value.total
      }))
      .sort((a, b) => b.total - a.total);
  }, [quizHistory]);

  const topFocusAreas = useMemo(() => {
    const counts = new Map<string, number>();
    for (const entry of quizHistory) {
      for (const area of entry.focusAreas) {
        counts.set(area, (counts.get(area) ?? 0) + 1);
      }
    }

    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([topic, count]) => ({ topic, count }));
  }, [quizHistory]);

  const remediationPlan = useMemo(() => {
    if (topFocusAreas.length === 0) {
      return [];
    }

    return topFocusAreas.map((area) => ({
      topic: area.topic,
      note: `Missed in ${area.count} recent ${area.count === 1 ? "attempt" : "attempts"}`
    }));
  }, [topFocusAreas]);

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
            <p className="profile-line">Average accuracy: {averageAccuracy}%</p>
          </div>
        </article>

        {latestSummary && (
          <article className="latest-summary-card">
            <h2 className="step-title">Latest quiz summary</h2>
            <p className="step-subtitle">
              {latestSummary.className} • {formatDate(latestSummary.completedAt)}
            </p>
            <p className="helper">Format: {latestSummary.examStyle}</p>
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

            {latestSummary.recommendations.length > 0 && (
              <ul className="stub-list compact-list">
                {latestSummary.recommendations.map((recommendation, index) => (
                  <li key={`${recommendation}-${index}`}>{recommendation}</li>
                ))}
              </ul>
            )}
          </article>
        )}

        <article className="latest-summary-card">
          <h2 className="step-title">Performance trend</h2>
          <p className="step-subtitle">Last {trendSeries.length} assessments by completion date.</p>

          {trendSeries.length === 0 ? (
            <p className="helper">No adaptive assessment history yet. Complete a quiz to populate analytics.</p>
          ) : (
            <div className="trend-list">
              {trendSeries.map((entry) => (
                <div key={`${entry.completedAt}-${entry.className}`} className="trend-row">
                  <div className="trend-head">
                    <span>{formatDate(entry.completedAt)}</span>
                    <span>{entry.percentage}%</span>
                  </div>
                  <div className="course-progress-track">
                    <div className="course-progress-fill" style={{ width: `${Math.min(100, entry.percentage)}%` }} />
                  </div>
                  <p className="progress-text">
                    {trackLabel(entry.practiceTrack)} • {entry.examStyle}
                  </p>
                </div>
              ))}
            </div>
          )}

          {trackStats.length > 0 && (
            <div className="analytics-grid">
              {trackStats.map((stat) => (
                <div key={stat.track} className="summary-stat">
                  <p className="label">{trackLabel(stat.track)}</p>
                  <p className="profile-line">Attempts: {stat.attempts}</p>
                  <p className="profile-line">Avg accuracy: {stat.average}%</p>
                </div>
              ))}
            </div>
          )}

          {formatStats.length > 0 && (
            <div className="section-score-list">
              {formatStats.map((stat) => {
                const pct = stat.total > 0 ? Number(((stat.correct / stat.total) * 100).toFixed(1)) : 0;
                return (
                  <div key={stat.label} className="section-score-item">
                    <p className="label">{stat.label}</p>
                    <p className="profile-line">
                      {stat.correct}/{stat.total} correct ({pct}%)
                    </p>
                  </div>
                );
              })}
            </div>
          )}
        </article>

        {remediationPlan.length > 0 && (
          <article className="latest-summary-card">
            <h2 className="step-title">Remediation pathways</h2>
            <p className="step-subtitle">Targeted restart options for the most frequent misses.</p>

            <ul className="lesson-list compact-list">
              {remediationPlan.map((item) => (
                <li key={item.topic} className="lesson-card remediation-card">
                  <p className="lesson-name">{item.topic}</p>
                  <p className="lesson-meta">{item.note}</p>
                  <button
                    type="button"
                    className="button secondary"
                    onClick={() => router.push("/learn")}
                  >
                    Start targeted practice
                  </button>
                </li>
              ))}
            </ul>
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
                    <p className="lesson-meta">Instructor: {lesson.instructor}</p>
                    <p className="lesson-meta">Last activity: {formatDate(lesson.lastActivity)}</p>
                  </div>
                  <div className="lesson-badges">
                    <span className={`status-badge status-${lesson.status}`}>{statusLabel(lesson.status)}</span>
                    <span className={`review-badge ${lesson.needsReview ? "review-needed" : "review-good"}`}>
                      {lesson.needsReview ? "Needs review" : "On track"}
                    </span>
                  </div>
                </div>

                <div className="progress-row" aria-hidden="true">
                  <div className="course-progress-track">
                    <div className="course-progress-fill" style={{ width: `${lesson.progressPct}%` }} />
                  </div>
                  <p className="progress-text">
                    Progress: {lesson.progressPct}% • Quiz: {lesson.quizScore}
                  </p>
                  <p className="progress-text">Next: {lesson.nextMilestone}</p>
                </div>
              </li>
            ))}
          </ul>
        </article>

        <footer className="footer">
          <button type="button" className="button secondary" onClick={() => router.push("/learn") }>
            Back to Learn
          </button>
          <button type="button" className="button primary" onClick={() => router.push("/upload") }>
            Upload new lesson
          </button>
        </footer>
      </section>
    </main>
  );
}
