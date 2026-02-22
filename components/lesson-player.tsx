"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { KnowledgeCheck } from "./knowledge-check";

type Module = {
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
};

type MediaAsset = {
  asset_id: string;
  module_id: string;
  asset_type: "video" | "audio";
  storage_url: string | null;
  status: string;
};

type Lesson = {
  id: string;
  modules: Module[];
  media_assets: MediaAsset[];
  profile: any;
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

type LessonPlayerProps = {
  lesson: Lesson;
  profile: Profile;
};

type ViewMode = "content" | "knowledge-check";

export function LessonPlayer({ lesson, profile }: LessonPlayerProps) {
  const router = useRouter();
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [viewMode, setViewMode] = useState<ViewMode>("content");
  const [completedSteps, setCompletedSteps] = useState<Set<string>>(new Set());
  const [checkpointSessions, setCheckpointSessions] = useState<string[]>([]);

  const currentModule = lesson.modules[currentModuleIndex];
  const currentStep = currentModule?.steps[currentStepIndex];
  const totalModules = lesson.modules.length;
  const totalStepsInModule = currentModule?.steps.length || 0;

  const progressPercent = Math.round(
    ((currentModuleIndex * 100 + (currentStepIndex / totalStepsInModule) * 100) / totalModules)
  );

  const hasVideo = profile?.learning_preferences?.content_formats?.includes("visual") || profile?.learning_preferences?.content_formats?.includes("video") || false;
  const hasAudio = profile?.learning_preferences?.content_formats?.includes("auditory") || profile?.learning_preferences?.content_formats?.includes("audio") || false;

  const moduleAssets = lesson.media_assets.filter(
    (asset) => asset.module_id === currentModule?.module_id
  );

  const videoAsset = moduleAssets.find((a) => a.asset_type === "video");
  const audioAsset = moduleAssets.find((a) => a.asset_type === "audio");

  const handleStepComplete = () => {
    if (currentStep) {
      setCompletedSteps((prev) => new Set([...prev, currentStep.step_id]));
    }

    if (currentStepIndex < totalStepsInModule - 1) {
      setCurrentStepIndex((prev) => prev + 1);
    } else {
      setViewMode("knowledge-check");
    }
  };

  const handleCheckpointComplete = (sessionId: string) => {
    setCheckpointSessions((prev) => [...prev, sessionId]);

    if (currentModuleIndex < totalModules - 1) {
      setCurrentModuleIndex((prev) => prev + 1);
      setCurrentStepIndex(0);
      setViewMode("content");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      sessionStorage.setItem("erica_lesson_id", lesson.id);
      sessionStorage.setItem("erica_checkpoint_sessions", JSON.stringify(checkpointSessions));
      router.push("/test");
    }
  };

  if (!currentModule) {
    return (
      <main className="onboarding-shell">
        <header className="hero-band">
          <h1 className="hero-title">Lesson complete!</h1>
        </header>
      </main>
    );
  }

  if (viewMode === "knowledge-check") {
    return (
      <KnowledgeCheck
        lesson={lesson}
        module={currentModule}
        checkpoint={currentModule.checkpoint}
        onComplete={handleCheckpointComplete}
        progress={progressPercent}
        moduleNumber={currentModuleIndex + 1}
        totalModules={totalModules}
      />
    );
  }

  return (
    <main className="lesson-container">
      <aside className="lesson-sidebar">
        <div className="sidebar-header">
          <h2 className="sidebar-title">Your Lesson</h2>
          <p className="sidebar-subtitle">{lesson.profile.subject}</p>
        </div>

        <div className="module-list">
          {lesson.modules.map((module, moduleIdx) => {
            const isActive = moduleIdx === currentModuleIndex;
            const isCompleted = moduleIdx < currentModuleIndex;

            return (
              <div
                key={module.module_id}
                className={`module-item ${isActive ? "active" : ""} ${isCompleted ? "completed" : ""}`}
              >
                <div className="module-header">
                  <span className="module-number">{moduleIdx + 1}</span>
                  <span className="module-title">{module.title}</span>
                  {isCompleted && <span className="check-mark">✓</span>}
                </div>

                {isActive && (
                  <div className="step-list">
                    {module.steps.map((step, stepIdx) => {
                      const isStepActive = stepIdx === currentStepIndex;
                      const isStepCompleted = completedSteps.has(step.step_id);

                      return (
                        <div
                          key={step.step_id}
                          className={`step-item ${isStepActive ? "active" : ""} ${isStepCompleted ? "completed" : ""}`}
                        >
                          <span className="step-icon">{isStepCompleted ? "✓" : "○"}</span>
                          <span className="step-title">{step.title}</span>
                        </div>
                      );
                    })}
                    <div className="step-item checkpoint">
                      <span className="step-icon">★</span>
                      <span className="step-title">Knowledge Check</span>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="sidebar-footer">
          <button
            type="button"
            className="button secondary"
            onClick={() => router.push("/upload")}
            style={{ width: "100%" }}
          >
            Exit lesson
          </button>
        </div>
      </aside>

      <section className="lesson-content">
        <header className="content-header">
          <div className="progress-wrap">
            <div className="progress-bar" style={{ width: `${progressPercent}%` }} />
          </div>
          <div className="breadcrumb">
            Module {currentModuleIndex + 1} of {totalModules} · Step {currentStepIndex + 1} of{" "}
            {totalStepsInModule}
          </div>
        </header>

        <article className="content-main">
          <div className="content-header-section">
            <h1 className="content-title">{currentStep?.title}</h1>
            <p className="content-objective">{currentModule.objective}</p>
          </div>

          {hasVideo && videoAsset && videoAsset.storage_url && (
            <div className="media-container">
              <video
                controls
                className="media-player"
                src={videoAsset.storage_url}
                style={{ width: "100%", borderRadius: "12px" }}
              >
                Your browser does not support video playback.
              </video>
            </div>
          )}

          {hasAudio && audioAsset && audioAsset.storage_url && !hasVideo && (
            <div className="media-container">
              <audio
                controls
                className="media-player"
                src={audioAsset.storage_url}
                style={{ width: "100%" }}
              >
                Your browser does not support audio playback.
              </audio>
            </div>
          )}

          {(!hasVideo && !hasAudio) || (!videoAsset?.storage_url && !audioAsset?.storage_url) ? (
            <div className="text-content">
              <div className="instruction-box">
                <p>{currentStep?.instruction}</p>
              </div>
            </div>
          ) : (
            <div className="text-content">
              <h3 className="section-heading">Instructions</h3>
              <p>{currentStep?.instruction}</p>
            </div>
          )}

          {currentStep?.kind === "practice" && (
            <div className="practice-zone">
              <h3 className="section-heading">Practice Area</h3>
              <textarea
                className="practice-input"
                placeholder="Work through the practice here... Erica will guide you if needed."
                rows={6}
              />
            </div>
          )}

          {currentStep?.kind === "challenge" && (
            <div className="practice-zone">
              <h3 className="section-heading">Challenge Zone</h3>
              <textarea
                className="practice-input"
                placeholder="Solve the challenge here..."
                rows={8}
              />
            </div>
          )}
        </article>

        <footer className="content-footer">
          {currentStepIndex > 0 && (
            <button
              type="button"
              className="button secondary"
              onClick={() => setCurrentStepIndex((prev) => prev - 1)}
            >
              ← Previous
            </button>
          )}
          <div style={{ flex: 1 }} />
          <button
            type="button"
            className="button primary"
            onClick={handleStepComplete}
          >
            {currentStepIndex < totalStepsInModule - 1 ? "Continue →" : "Start Knowledge Check →"}
          </button>
        </footer>
      </section>
    </main>
  );
}
