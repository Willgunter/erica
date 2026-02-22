"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { LessonPlayer } from "@/components/lesson-player";

type Lesson = {
  id: string;
  status: "generating" | "completed" | "failed";
  modules: Array<{
    module_id: string;
    title: string;
    objective: string;
    teaching_style: string;
    steps: Array<{
      step_id: string;
      kind: string;
      title: string;
      instruction: string;
      estimated_minutes: number;
    }>;
    checkpoint: {
      checkpoint_id: string;
      module_id: string;
      marker: string;
      questions: string[];
    };
  }>;
  media_assets: Array<{
    asset_id: string;
    module_id: string;
    asset_type: "video" | "audio";
    storage_url: string | null;
    status: string;
  }>;
  profile: any;
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

      if (lessonData.status === "completed") {
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

    const headers: Record<string, string> = {
      "Content-Type": "application/json"
    };
    if (token) headers["Authorization"] = `Bearer ${token}`;
    if (devUserId) headers["x-dev-user-id"] = devUserId;

    const response = await fetch("/api/profile", { headers });
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

    const payload = {
      profile: {
        user_id: profileData.user_id,
        subject: profileData.subject,
        goals: profileData.goals,
        study_time_minutes: studyTimeMap[profileData.study_time] || 30,
        pacing: pacingMap[profileData.pacing] || "medium",
        teaching_style: profileData.learning_preferences.teaching_style || "not_sure",
        content_formats: profileData.learning_preferences.content_formats,
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

      const data = await response.json();
      setLesson(data);

      if (data.status === "completed") {
        setStatus("ready");
      } else if (data.status === "failed") {
        setError("Lesson generation failed. Please try again.");
        setStatus("error");
      } else {
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
