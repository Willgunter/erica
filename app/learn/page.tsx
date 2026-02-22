"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { LessonPlayer } from "@/components/lesson-player";

type Lesson = {
  id: string;
  title?: string;
  subject?: string;
  status: "generating" | "completed" | "failed";
  modules: Array<{
    module_id: string;
    title: string;
    objective: string;
    teaching_style: string;
    pacing?: string;
    concept_explanation?: string;
    key_insight?: string;
    flashcards?: Array<{ front: string; back: string }>;
    exam_questions?: Array<{ question: string; answer: string; hints: string[] }>;
    steps: Array<{
      step_id: string;
      kind: string;
      title: string;
      instruction: string;
      media_ref?: string | null;
    }>;
    checkpoint: {
      checkpoint_id: string;
      module_id?: string;
      marker?: string;
      questions: string[];
    };
    estimated_minutes: number;
  }>;
  media_assets: Array<{
    asset_id: string;
    module_id: string;
    kind?: "visual" | "audio";
    asset_type?: "video" | "audio";
    storage_url?: string | null;
    url?: string | null;
    status: string;
  }>;
  profile?: any;
  estimated_duration: number;
};

type Profile = {
  user_id: string;
  subject: string;
  goals: string[];
  study_time: string;
  pacing: string;
  accessibility: any;
  learning_preferences: {
    teaching_style: string | null;
    content_formats: string[];
    review_preferences: string[];
  };
};

const SUPABASE_TOKEN_STORAGE_KEY = "supabaseAccessToken";
const DEV_USER_ID_STORAGE_KEY = "supabaseDevUserId";

function getTrackConfig(track: PracticeTrack): TrackConfig {
  return TRACK_CONFIGS.find((item) => item.track === track) ?? TRACK_CONFIGS[2];
}

function formatDuration(seconds: number): string {
  const safe = Math.max(0, seconds);
  const minutes = Math.floor(safe / 60);
  const remaining = safe % 60;
  return `${minutes}:${remaining.toString().padStart(2, "0")}`;
}

function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}

function createBrowserSupabaseClient() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error("Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY.");
  }

  return createClient(supabaseUrl, supabaseAnonKey);
}

async function ensureSupabaseAccessToken() {
  if (typeof window === "undefined") {
    return null;
  }

  const supabase = createBrowserSupabaseClient();
  const existingToken = window.localStorage.getItem(SUPABASE_TOKEN_STORAGE_KEY);
  if (existingToken) {
    const { data: userData, error: userError } = await supabase.auth.getUser(existingToken);
    if (!userError && userData.user) {
      return existingToken;
    }

    window.localStorage.removeItem(SUPABASE_TOKEN_STORAGE_KEY);
  }

  const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
  if (sessionError) {
    throw new Error(sessionError.message);
  }

  const sessionToken = sessionData.session?.access_token ?? null;
  if (sessionToken) {
    window.localStorage.setItem(SUPABASE_TOKEN_STORAGE_KEY, sessionToken);
    return sessionToken;
  }

  if (process.env.NODE_ENV === "production") {
    return null;
  }

  const { data: anonymousData, error: anonymousError } = await supabase.auth.signInAnonymously();
  if (anonymousError || !anonymousData.session?.access_token) {
    throw new Error(
      "Could not create a local Supabase session. Enable Anonymous sign-ins or sign in with a real user."
    );
  }

  const token = anonymousData.session.access_token;
  window.localStorage.setItem(SUPABASE_TOKEN_STORAGE_KEY, token);
  return token;
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

async function buildAuthHeaders(): Promise<Record<string, string>> {
  try {
    const token = await ensureSupabaseAccessToken();
    if (token) {
      return {
        Authorization: `Bearer ${token}`
      };
    }
  } catch (error) {
    if (process.env.NODE_ENV === "production") {
      throw error;
    }
  }

  const devUserId = getOrCreateDevUserId();
  if (!devUserId) {
    throw new Error("No authenticated Supabase session. Sign in before running assessment API calls.");
  }

  return {
    "x-dev-user-id": devUserId
  };
}

function runJavascriptPreview(submission: string, question: CodeQuestion): CodeCheckResult {
  try {
    const factory = new Function(
      `${submission}\nreturn typeof ${question.function_name} === \"function\" ? ${question.function_name} : null;`
    );
    const candidate = factory();

    if (typeof candidate !== "function") {
      return {
        passedCount: 0,
        totalCount: question.visible_tests.length,
        details: [
          {
            label: "function export",
            passed: false,
            message: `Could not find function ${question.function_name}(...) in submission.`
          }
        ]
      };
    }

    let passedCount = 0;
    const details = question.visible_tests.map((testCase) => {
      try {
        const output = candidate([...testCase.input]);
        const passed = output === testCase.expected;
        if (passed) {
          passedCount += 1;
        }

        return {
          label: testCase.label,
          passed,
          message: passed
            ? `Passed (${String(output)})`
            : `Expected ${String(testCase.expected)}, got ${String(output)}`
        };
      } catch (error) {
        return {
          label: testCase.label,
          passed: false,
          message: `Runtime error: ${(error as Error).message}`
        };
      }
    });

    return {
      passedCount,
      totalCount: question.visible_tests.length,
      details
    };
  } catch (error) {
    return {
      passedCount: 0,
      totalCount: question.visible_tests.length,
      details: [
        {
          label: "compile",
          passed: false,
          message: `Code did not compile in preview checker: ${(error as Error).message}`
        }
      ]
    };
  }
}

function mapSubmitResponse(payload: AssessmentSubmitResponse): QuizResult {
  return {
    correctCount: payload.score.correct,
    totalCount: payload.score.total,
    percentage: payload.score.percentage,
    reviewedItems: payload.reviewed_items.map((item) => ({
      id: item.id,
      prompt: item.prompt,
      userResponse: item.user_response,
      expected: item.expected,
      isCorrect: item.is_correct,
      explanation: item.explanation,
      manualReviewRequired: Boolean(item.manual_review_required)
    })),
    sectionScores: payload.section_scores.map((section) => ({
      label: section.label,
      correct: section.correct,
      total: section.total
    })),
    needsReview: payload.needs_review,
    focusAreas: payload.focus_areas,
    recommendations: payload.recommendations
  };
}

export default function LearnPage() {
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "generating" | "ready" | "error">("loading");
  const [error, setError] = useState<string | null>(null);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    initializeLesson();
  }, []);

  const initializeLesson = async () => {
    try {
      const chunksJson = sessionStorage.getItem("erica_content_chunks");
      if (!chunksJson) {
        setError("No content uploaded. Please go back and upload your lesson materials.");
        setStatus("error");
        return;
      }

      const chunks = JSON.parse(chunksJson);
      const profileData = await fetchProfile();
      
      if (!profileData) {
        setError("No profile found. Please complete onboarding first.");
        setStatus("error");
        return;
      }

      setProfile(profileData);
      setStatus("generating");

      const lessonData = await generateLesson(profileData, chunks);
      setLesson(lessonData);
      
      if (lessonData.id) {
        sessionStorage.setItem("erica_lesson_id", lessonData.id);
        sessionStorage.setItem(
          "erica_lesson_snapshot",
          JSON.stringify({
            id: lessonData.id,
            subject: lessonData.subject || profileData.subject || "General learning"
          })
        );
      }

      if (lessonData.modules && lessonData.modules.length > 0) {
        setStatus("ready");
        if (lessonData.status !== "completed") {
          pollLessonStatus(lessonData.id);
        }
      } else if (lessonData.status === "completed") {
        setStatus("ready");
      } else {
        pollLessonStatus(lessonData.id);
      }
    } catch (err) {
      console.error("Lesson initialization error:", err);
      setError(err instanceof Error ? err.message : "Failed to initialize lesson");
      setStatus("error");
    }
  };

  const fetchProfile = async (): Promise<Profile | null> => {
    const devUserId = window.localStorage.getItem("supabaseDevUserId");
    const token = window.localStorage.getItem("supabaseAccessToken");

    const makeRequest = async (useToken: string | null, useDevUserId: string | null) => {
      const headers: Record<string, string> = {
        "Content-Type": "application/json"
      };
      if (useToken) headers["Authorization"] = `Bearer ${useToken}`;
      if (useDevUserId) headers["x-dev-user-id"] = useDevUserId;

      return fetch("/api/profile", { headers });
    };

    let response = await makeRequest(token, devUserId);
    
    if (response.status === 401 && !devUserId) {
      const fallbackDevUserId = window.localStorage.getItem("supabaseDevUserId");
      if (fallbackDevUserId) {
        response = await makeRequest(null, fallbackDevUserId);
      }
    }

    if (!response.ok) return null;

    const data = await response.json();
    return data.profile || null;
  };

  const generateLesson = async (profileData: Profile, chunks: any[]): Promise<Lesson> => {
    const studyTimeMap: Record<string, number> = {
      "15_min": 15,
      "30_min": 30,
      "45_min": 45,
      "60_min_plus": 60
    };

    const pacingMap: Record<string, string> = {
      "light": "slow",
      "steady": "medium",
      "accelerated": "fast"
    };
    const requestedFormats = Array.from(
      new Set([...(profileData.learning_preferences.content_formats || []), "video"])
    );

    const payload = {
      profile: {
        user_id: profileData.user_id,
        subject: profileData.subject,
        goals: profileData.goals,
        study_time_minutes: studyTimeMap[profileData.study_time] || 30,
        pacing: pacingMap[profileData.pacing] || "medium",
        teaching_style: profileData.learning_preferences.teaching_style || "not_sure",
        content_formats: requestedFormats,
        review_preferences: profileData.learning_preferences.review_preferences || [],
        accessibility: profileData.accessibility,
        uncertainty_flags: []
      },
      content_chunks: chunks.map((chunk, idx) => ({
        id: `chunk-${idx}`,
        source_id: chunk.source || "uploaded",
        chunk_index: idx,
        text: chunk.text,
        metadata: {}
      }))
    };

    const response = await fetch("/api/lesson/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Failed to generate lesson");
    }

    const data = await response.json();
    return data.lesson;
  };

  const pollLessonStatus = async (lessonId: string) => {
    const maxAttempts = 60;
    let attempts = 0;

    const poll = async () => {
      if (attempts >= maxAttempts) {
        setError("Lesson generation is taking longer than expected. Please refresh.");
        setStatus("error");
        return;
      }

      attempts++;
      const response = await fetch(`/api/lesson/${lessonId}`);
      if (!response.ok) {
        setTimeout(poll, 2000);
        return;
      }

      const data = (await response.json()) as Lesson;
      setLesson(data);
      sessionStorage.setItem(
        "erica_lesson_snapshot",
        JSON.stringify({
          id: data.id,
          subject: data.subject || profile?.subject || "General learning"
        })
      );

      if (data.status === "completed") {
        setStatus("ready");
      } else if (data.status === "failed") {
        setError("Lesson generation failed. Please try again.");
        setStatus("error");
      } else {
        // Keep the lesson usable while continuing to stream media asset updates.
        if (data.modules && data.modules.length > 0) {
          setStatus("ready");
        }
        setTimeout(poll, 2000);
      }
    };

    setTimeout(poll, 2000);
  };

  if (status === "loading") {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Preparing your lesson...</h1>
          <p className="hero-sub">Step 3 of 5: Learning</p>
        </header>
        <section className="onboarding-body">
          <div className="loading-state">
            <div className="spinner" />
            <p>Loading your content...</p>
            <button
              type="button"
              className="button secondary"
              style={{ marginTop: "1rem" }}
              onClick={() => router.push("/profile")}
            >
              Back to profile
            </button>
          </div>
        </section>
      </main>
    );
  }

  if (status === "generating") {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Erica is building your personalized lesson</h1>
          <p className="hero-sub">Step 3 of 5: Learning</p>
          <div className="progress-wrap" aria-hidden="true">
            <div className="progress-bar progress-animated" style={{ width: "60%" }} />
          </div>
        </header>
        <section className="onboarding-body">
          <div className="loading-state">
            <div className="spinner" />
            <p className="step-subtitle">
              Analyzing your content, personalizing to your learning style, and preparing{" "}
              {lesson?.modules.length || "several"} modules...
            </p>
            <p className="helper" style={{ textAlign: "center", marginTop: "1rem" }}>
              This usually takes 10-30 seconds.
            </p>
            <button
              type="button"
              className="button secondary"
              style={{ marginTop: "1rem" }}
              onClick={() => router.push("/profile")}
            >
              Back to profile
            </button>
          </div>
        </section>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Something went wrong</h1>
          <p className="hero-sub">Step 3 of 5: Learning</p>
        </header>
        <section className="onboarding-body">
          <article className="step-card">
            <p className="error">{error}</p>
            <footer className="footer" style={{ marginTop: "1.5rem" }}>
              <button
                type="button"
                className="button secondary"
                onClick={() => router.push("/upload")}
              >
                ← Back to upload
              </button>
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
                onClick={() => window.location.reload()}
              >
                Try again
              </button>
            </footer>
          </article>
        </section>
      </main>
    );
  }

  if (status === "ready" && lesson && profile) {
    return <LessonPlayer lesson={lesson} profile={profile} />;
  }

  return null;
}
