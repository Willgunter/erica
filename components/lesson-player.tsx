"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { KnowledgeCheck } from "./knowledge-check";

interface Flashcard {
  front: string;
  back: string;
}

interface LessonModule {
  module_id: string;
  title: string;
  objective: string;
  teaching_style: string;
  pacing: string;
  concept_explanation?: string;
  key_insight?: string;
  flashcards?: Flashcard[];
  steps: Array<{
    step_id: string;
    kind: string;
    title: string;
    instruction: string;
    media_ref: string | null;
  }>;
  checkpoint: {
    checkpoint_id: string;
    questions: string[];
  };
  estimated_minutes: number;
}

interface MediaAsset {
  asset_id: string;
  module_id: string;
  kind?: "visual" | "audio";
  asset_type?: "video" | "audio";
  status: "pending" | "processing" | "ready" | "completed" | "failed";
  url?: string | null;
  storage_url?: string | null;
  content_type?: string | null;
  metadata?: {
    renderer?: string;
    [key: string]: unknown;
  } | null;
}

interface Lesson {
  id: string;
  title: string;
  subject: string;
  modules: LessonModule[];
  media_assets: MediaAsset[];
  estimated_duration: number;
  status: string;
}

interface Profile {
  content_formats?: string[];
  teaching_style?: string;
}

interface LessonPlayerProps {
  lesson: Lesson;
  profile?: Profile;
}

type LearningMode = "flashcards" | "concept" | "listen" | "watch";
type ViewMode = "content" | "knowledge-check";
type ReadyAssetFilter = { renderer?: string };

const LEARN_MODE_SUBJECT_LABEL = "bio";
const LEARN_MODE_SIDEBAR_TITLE =
  "Understanding Quadratic Equations' Structure, Completing the Square Derivation Process";
const LEARN_MODE_MODULE_TITLES = [
  "Understanding Quadratic Equations' Structure",
  "Completing the Square Derivation Process",
  "Applying the Quadratic Formula",
  "Parabola Intercepts and Discriminant Meaning",
] as const;
const LEARN_MODE_MODULE_DURATIONS = [12, 15, 12, 18] as const;
const LEARN_MODE_MAIN_OBJECTIVE = "Understand and apply understanding quadratic equations' structure";

function resolveMediaSource(mediaUrl: string | null | undefined): string {
  if (!mediaUrl) return "";
  if (mediaUrl.startsWith("local://")) {
    return `/api/lesson-assets?storage_url=${encodeURIComponent(mediaUrl)}`;
  }
  return mediaUrl;
}

function FlashcardDeck({ cards }: { cards: Flashcard[] }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [mastered, setMastered] = useState<Set<number>>(new Set());
  const safeCards = (cards || []).filter(
    (card): card is Flashcard =>
      Boolean(
        card &&
          typeof card.front === "string" &&
          typeof card.back === "string" &&
          (card.front.trim() || card.back.trim()),
      ),
  );

  useEffect(() => {
    setIndex(0);
    setFlipped(false);
    setMastered(new Set());
  }, [safeCards.length]);

  useEffect(() => {
    if (safeCards.length > 0 && index >= safeCards.length) {
      setIndex(0);
      setFlipped(false);
    }
  }, [index, safeCards.length]);

  if (safeCards.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "2rem", color: "var(--ink-soft)" }}>
        No flashcards for this module yet.
      </div>
    );
  }

  const card = safeCards[index] || safeCards[0];

  const handleNext = (didMaster: boolean) => {
    if (didMaster) setMastered((prev) => new Set([...prev, index]));
    setFlipped(false);
    setTimeout(() => setIndex((i) => (i + 1) % safeCards.length), 120);
  };

  const handlePrev = () => {
    setFlipped(false);
    setTimeout(() => setIndex((i) => (i - 1 + safeCards.length) % safeCards.length), 120);
  };

  return (
    <div className="flashcard-deck">
      <div className="flashcard-meta">
        <span>{index + 1} / {safeCards.length}</span>
        <span>{mastered.size} mastered</span>
      </div>

      <div
        className={`flashcard ${flipped ? "flipped" : ""}`}
        onClick={() => setFlipped(!flipped)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && setFlipped(!flipped)}
        aria-label={flipped ? "Back of card — click to flip" : "Front of card — click to reveal"}
      >
        <div className="flashcard-inner">
          <div className="flashcard-face flashcard-front">
            <div className="flashcard-label">TERM</div>
            <div className="flashcard-text">{card.front}</div>
            <div className="flashcard-hint">Click to reveal</div>
          </div>
          <div className="flashcard-face flashcard-back">
            <div className="flashcard-label">ANSWER</div>
            <div className="flashcard-text">{card.back}</div>
          </div>
        </div>
      </div>

      {flipped && (
        <div className="flashcard-actions">
          <button className="fc-btn fc-btn-hard" onClick={() => handleNext(false)}>
            Still learning
          </button>
          <button className="fc-btn fc-btn-easy" onClick={() => handleNext(true)}>
            Got it! ✓
          </button>
        </div>
      )}

      {!flipped && (
        <div className="flashcard-nav">
          <button className="fc-nav-btn" onClick={handlePrev}>← Prev</button>
          <button className="fc-nav-btn" onClick={() => setFlipped(true)}>Reveal</button>
          <button className="fc-nav-btn" onClick={() => handleNext(false)}>Next →</button>
        </div>
      )}

      <div className="flashcard-progress-track">
        <div
          className="flashcard-progress-fill"
          style={{ width: `${(mastered.size / safeCards.length) * 100}%` }}
        />
      </div>
    </div>
  );
}

function ConceptView({ module }: { module: LessonModule }) {
  const explanation = module.concept_explanation || module.steps[0]?.instruction || "No explanation available.";
  const keyInsight = module.key_insight;

  return (
    <div className="concept-view">
      {keyInsight && (
        <div className="key-insight-box">
          <div className="key-insight-label">💡 Key Insight</div>
          <p className="key-insight-text">{keyInsight}</p>
        </div>
      )}
      <div className="instruction-box" style={{ marginTop: "1.2rem" }}>
        <p style={{ margin: 0, lineHeight: 1.8, fontSize: "1rem" }}>{explanation}</p>
      </div>
    </div>
  );
}

export function LessonPlayer({ lesson, profile }: LessonPlayerProps) {
  const HARDCODED_WATCH_VIDEO_URL = "/api/watch-video";
  const pathname = usePathname();
  const router = useRouter();
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [viewMode, setViewMode] = useState<ViewMode>("content");
  const [learningMode, setLearningMode] = useState<LearningMode>("flashcards");
  const [completedModules, setCompletedModules] = useState<Set<string>>(new Set());
  const [isVerifyingSkipCode, setIsVerifyingSkipCode] = useState(false);
  const [isGeneratingQuickWatch, setIsGeneratingQuickWatch] = useState(false);
  const [quickWatchError, setQuickWatchError] = useState<string | null>(null);
  const [quickWatchVideoUrl, setQuickWatchVideoUrl] = useState<string | null>(null);

  const currentModule = lesson.modules[currentModuleIndex];
  const isStudentLearnMode = pathname?.startsWith("/learn") ?? false;
  const getDisplayModuleTitle = (index: number, fallback: string) =>
    isStudentLearnMode ? LEARN_MODE_MODULE_TITLES[index] ?? fallback : fallback;
  const getDisplayModuleMinutes = (index: number, fallback: number) =>
    isStudentLearnMode ? LEARN_MODE_MODULE_DURATIONS[index] ?? fallback : fallback;
  const displayedSidebarTitle = isStudentLearnMode ? LEARN_MODE_SIDEBAR_TITLE : lesson.title;
  const displayedSubject = isStudentLearnMode ? LEARN_MODE_SUBJECT_LABEL : lesson.subject;
  const displayedMainHeaderTitle = currentModule
    ? getDisplayModuleTitle(currentModuleIndex, currentModule.title)
    : "";
  const displayedMainHeaderObjective =
    isStudentLearnMode && currentModuleIndex === 0
      ? LEARN_MODE_MAIN_OBJECTIVE
      : currentModule?.objective;
  const displayedMainHeaderMinutes = currentModule
    ? getDisplayModuleMinutes(currentModuleIndex, currentModule.estimated_minutes)
    : 0;

  const totalModules = lesson.modules.length;
  const overallProgress = totalModules > 0
    ? Math.round(((completedModules.size + (viewMode === "knowledge-check" ? 0.5 : 0)) / totalModules) * 100)
    : 0;

  const getModuleAssets = (moduleId: string) =>
    lesson.media_assets?.filter((a) => a.module_id === moduleId) || [];

  const getReadyAsset = (
    moduleId: string,
    kind: "visual" | "audio",
    filter: ReadyAssetFilter = {},
  ) => {
    const assets = getModuleAssets(moduleId);
    const asset = assets.find((a) => {
      const aKind = a.kind || (a.asset_type === "video" ? "visual" : a.asset_type === "audio" ? "audio" : null);
      const aUrl = a.url || a.storage_url;
      const aStatus = a.status;
      const isReady = aStatus === "ready" || aStatus === "completed";
      const hasRendererMatch = !filter.renderer || a.metadata?.renderer === filter.renderer;
      return aKind === kind && isReady && aUrl && hasRendererMatch;
    });
    if (!asset) return null;
    return { ...asset, url: asset.url || asset.storage_url };
  };

  const getPreferredVideoAsset = (moduleId: string) =>
    getReadyAsset(moduleId, "visual", { renderer: "manim" }) ?? getReadyAsset(moduleId, "visual");

  const hasAudio = currentModule ? !!getReadyAsset(currentModule.module_id, "audio") : false;

  const watchQuickPrompt = "Create a 2 second, simple visual summary for this topic using basic shapes and one core idea.";

  const clearQuickWatchState = () => {
    setQuickWatchError(null);
    setQuickWatchVideoUrl(null);
  };

  const handleGenerateQuickWatchVideo = async () => {
    if (!currentModule || !currentModule.module_id || isGeneratingQuickWatch) return;

    setIsGeneratingQuickWatch(true);
    setLearningMode("watch");
    setQuickWatchVideoUrl(null);
    setQuickWatchError("Generating 2s clip...");
    setViewMode("content");
    try {
      const response = await fetch(`/api/lesson/${lesson.id}/generate-short-video`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          module_id: currentModule.module_id,
          prompt: watchQuickPrompt,
        }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(typeof data.error === "string" ? data.error : "Unable to start quick video generation.");
      }

      const generatedAsset = data?.asset;
      const generatedUrl = generatedAsset?.storage_url || generatedAsset?.url;
      if (typeof generatedUrl === "string" && generatedUrl) {
        setQuickWatchVideoUrl(resolveMediaSource(generatedUrl));
        setQuickWatchError(null);
        return;
      }

      const lessonAsset = Array.isArray(data?.lesson?.media_assets)
        ? data.lesson.media_assets.find(
            (asset: any) =>
              asset?.module_id === currentModule.module_id &&
              asset?.asset_type === "video" &&
              (asset?.status === "ready" || asset?.status === "completed")
          )
        : null;
      if (lessonAsset?.storage_url || lessonAsset?.url) {
        setQuickWatchVideoUrl(
          resolveMediaSource(lessonAsset.storage_url || lessonAsset.url || null)
        );
        setQuickWatchError(null);
        return;
      }

      setQuickWatchError("Quick video generated but the URL isn't available yet. Polling lessons will update when ready.");
    } catch (error) {
      setQuickWatchError(error instanceof Error ? error.message : "Could not generate quick watch video.");
    } finally {
      setIsGeneratingQuickWatch(false);
    }
  };

  const handleLearningModeSelect = (mode: LearningMode) => {
    setLearningMode(mode);
    setViewMode("content");
    if (mode === "watch") {
      setQuickWatchVideoUrl(HARDCODED_WATCH_VIDEO_URL);
      setQuickWatchError(null);
    }
  };

  useEffect(() => {
    clearQuickWatchState();
  }, [currentModule?.module_id]);

  const goToFinalTest = () => {
    if (typeof window !== "undefined") {
      window.sessionStorage.setItem("erica_lesson_id", lesson.id);
      window.sessionStorage.setItem("erica_lesson_snapshot", JSON.stringify(lesson));
    }
    router.push("/test");
  };

  const handleCheckpointComplete = (_sessionId: string) => {
    setCompletedModules((prev) => new Set([...prev, currentModule.module_id]));

    const nextIndex = currentModuleIndex + 1;
    if (nextIndex < lesson.modules.length) {
      setCurrentModuleIndex(nextIndex);
      setLearningMode("flashcards");
      setViewMode("content");
    } else {
      setViewMode("content");
      goToFinalTest();
    }
  };

  const handleModuleSelect = (index: number) => {
    setCurrentModuleIndex(index);
    setLearningMode("flashcards");
    setViewMode("content");
  };

  const requestSkipToFinalTest = async () => {
    if (isVerifyingSkipCode || typeof window === "undefined") return;

    const confirmed = window.confirm(
      "Skip the remaining modules and go directly to the final test? This is intended for demo use only."
    );
    if (!confirmed) return;

    const code = window.prompt("Enter demo confirmation code");
    if (!code) return;

    setIsVerifyingSkipCode(true);
    try {
      const response = await fetch("/api/test/skip-verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await response.json();

      if (!response.ok || !data.ok) {
        window.alert(typeof data.error === "string" ? data.error : "Invalid demo confirmation code.");
        return;
      }

      goToFinalTest();
    } catch {
      window.alert("Unable to verify demo confirmation code right now.");
    } finally {
      setIsVerifyingSkipCode(false);
    }
  };

  const isOnFinalModule = currentModuleIndex === lesson.modules.length - 1;

  if (viewMode === "knowledge-check" && currentModule) {
    return (
      <KnowledgeCheck
        lesson={{ id: lesson.id }}
        module={{
          module_id: currentModule.module_id,
          title: getDisplayModuleTitle(currentModuleIndex, currentModule.title),
          objective:
            isStudentLearnMode && currentModuleIndex === 0
              ? LEARN_MODE_MAIN_OBJECTIVE
              : currentModule.objective,
        }}
        checkpoint={currentModule.checkpoint}
        isLastModule={isOnFinalModule}
        showSkipToFinalTest={!isOnFinalModule}
        isVerifyingSkipCode={isVerifyingSkipCode}
        onRequestSkipToFinalTest={requestSkipToFinalTest}
        onComplete={handleCheckpointComplete}
      />
    );
  }

  const isAllComplete = completedModules.size === lesson.modules.length;

  const learnModeTabs: { id: LearningMode; label: string; disabled?: boolean }[] = [
    { id: "flashcards", label: "Flashcards" },
    { id: "concept", label: "Concept" },
    { id: "listen", label: "Listen", disabled: !hasAudio },
    { id: "watch", label: "Watch" },
  ];
  const defaultTabs: { id: LearningMode; label: string; disabled?: boolean }[] = [
    { id: "flashcards", label: "📇 Flashcards" },
    { id: "concept", label: "📖 Concept" },
    { id: "listen", label: "🎧 Listen", disabled: !hasAudio },
    { id: "watch", label: "🎬 Watch" },
  ];
  const tabs = isStudentLearnMode ? learnModeTabs : defaultTabs;
  const sidebarStepItems = isStudentLearnMode
    ? [
        { id: "flashcards" as LearningMode, label: "Flashcards", icon: "📇" },
        { id: "concept" as LearningMode, label: "Concept", icon: "📖" },
        { id: "watch" as LearningMode, label: "Watch", icon: "🎬" },
      ]
    : tabs.filter((t) => !t.disabled).map((t) => ({
        id: t.id,
        icon: t.label.split(" ")[0],
        label: t.label.split(" ").slice(1).join(" "),
      }));

  return (
    <div className="lesson-container">
      {/* Sidebar */}
      <div className="lesson-sidebar">
        <div className="sidebar-header">
          <h2 className="sidebar-title">{displayedSidebarTitle}</h2>
          <p className="sidebar-subtitle">{displayedSubject}</p>
        </div>

        <div className="module-list">
          {lesson.modules.map((mod, idx) => {
            const isActive = idx === currentModuleIndex;
            const isDone = completedModules.has(mod.module_id);
            const displayModuleTitle = getDisplayModuleTitle(idx, mod.title);
            const displayModuleMinutes = getDisplayModuleMinutes(idx, mod.estimated_minutes);

            return (
              <div
                key={mod.module_id}
                className={`module-item ${isActive ? "active" : ""} ${isDone ? "completed" : ""}`}
              >
                <div className="module-header" onClick={() => handleModuleSelect(idx)}>
                  <div className="module-number">{isDone ? "✓" : idx + 1}</div>
                  <div className="module-title">{displayModuleTitle}</div>
                  <div style={{ fontSize: "0.75rem", color: "var(--ink-soft)" }}>
                    {displayModuleMinutes}m
                  </div>
                </div>
                {isActive && (
                  <div className="step-list">
                    {sidebarStepItems.map((t) => (
                      <div
                        key={t.id}
                        className={`step-item ${learningMode === t.id && viewMode === "content" ? "active" : ""}`}
                        style={{ cursor: "pointer" }}
                        onClick={() => handleLearningModeSelect(t.id)}
                      >
                        <span className="step-icon">{t.icon}</span>
                        {t.label}
                      </div>
                    ))}
                    <div
                      className={`step-item checkpoint ${viewMode === "knowledge-check" ? "active" : ""}`}
                    >
                      <span className="step-icon">🥊</span>
                      AI Spar
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="sidebar-footer">
          <div style={{ fontSize: "0.8rem", color: "var(--ink-soft)", marginBottom: "0.4rem" }}>
            Overall Progress
          </div>
          <div style={{ background: "#e7ddd0", borderRadius: "999px", height: "8px", overflow: "hidden" }}>
            <div style={{ width: `${overallProgress}%`, height: "100%", background: "linear-gradient(90deg, var(--accent-2), var(--accent))", transition: "width 0.5s ease" }} />
          </div>
          <div style={{ marginTop: "0.3rem", fontSize: "0.8rem", color: "var(--ink-soft)" }}>
            {overallProgress}% complete
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="lesson-content">
        <div className="content-header">
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <h1 style={{ margin: 0, fontSize: "1.2rem", fontWeight: 700 }}>{displayedMainHeaderTitle}</h1>
            <div style={{ fontSize: "0.85rem", color: "var(--ink-soft)" }}>
              {displayedSubject} · {displayedMainHeaderMinutes}min
            </div>
          </div>
          <p className="breadcrumb" style={{ marginTop: "0.3rem" }}>{displayedMainHeaderObjective}</p>

          {/* Mode tabs */}
          {!isAllComplete && (
            <div className="mode-tabs">
              {tabs.map((tab) => (
                <div
                  key={tab.id}
                  style={{ display: "inline-flex", alignItems: "center", gap: "0.4rem", flexWrap: "wrap" }}
                >
                  <button
                    className={`mode-tab ${learningMode === tab.id ? "active" : ""}`}
                    onClick={() => !tab.disabled && handleLearningModeSelect(tab.id)}
                    disabled={tab.disabled}
                    title={tab.disabled ? "Not available for this module" : undefined}
                  >
                    {tab.label}
                  </button>
                  {tab.id === "watch" && (
                    <button
                      className="button secondary"
                      onClick={handleGenerateQuickWatchVideo}
                      disabled={isGeneratingQuickWatch}
                      title="Generate a very short Gemini-based sample watch clip"
                      style={{ padding: "0.35rem 0.7rem", fontSize: "0.76rem" }}
                    >
                      {isGeneratingQuickWatch ? "Generating 2s clip..." : "Generate 2s clip"}
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {isAllComplete ? (
          <div className="content-main">
            <div style={{ textAlign: "center", padding: "4rem 1rem" }}>
              <div style={{ fontSize: "5rem", marginBottom: "1rem" }}>🎓</div>
              <h2 style={{ margin: "0 0 0.8rem" }}>Lesson Complete!</h2>
              <p style={{ color: "var(--ink-soft)", fontSize: "1.05rem", marginBottom: "2rem" }}>
                You&apos;ve worked through all {lesson.modules.length} modules. Amazing effort!
              </p>
              <div style={{ display: "flex", gap: "0.7rem", justifyContent: "center", flexWrap: "wrap" }}>
                <button
                  className="button secondary"
                  onClick={() => router.push("/profile")}
                  style={{ fontSize: "1.1rem", padding: "0.8rem 2rem" }}
                >
                  Back to Profile
                </button>
                <button
                  className="button primary"
                  onClick={goToFinalTest}
                  style={{ fontSize: "1.1rem", padding: "0.8rem 2rem" }}
                >
                  Continue to Final Test →
                </button>
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="content-main">
              {learningMode === "flashcards" && (
                <FlashcardDeck key={currentModule?.module_id || "no-module"} cards={currentModule?.flashcards || []} />
              )}

              {learningMode === "concept" && currentModule && (
                <ConceptView module={currentModule} />
              )}

              {learningMode === "listen" && currentModule && (() => {
                const audioAsset = getReadyAsset(currentModule.module_id, "audio");
                return audioAsset ? (
                  <div style={{ marginTop: "1.5rem" }}>
                    <h3 style={{ margin: "0 0 1rem", fontSize: "1.1rem" }}>🎧 Podcast — {currentModule.title}</h3>
                    <audio controls style={{ width: "100%", borderRadius: "8px" }}>
                      <source src={audioAsset.url!} />
                    </audio>
                    <p style={{ marginTop: "0.8rem", color: "var(--ink-soft)", fontSize: "0.9rem" }}>
                      Listen to the AI-generated explanation of this concept.
                    </p>
                  </div>
                ) : (
                  <div style={{ textAlign: "center", padding: "2rem", color: "var(--ink-soft)" }}>
                    Audio is still being generated...
                  </div>
                );
              })()}

              {learningMode === "watch" && currentModule && (() => {
              const videoAsset = getPreferredVideoAsset(currentModule.module_id);
                const rawVideoUrl = quickWatchVideoUrl ?? videoAsset?.url;
                const displayVideoUrl = resolveMediaSource(rawVideoUrl);
                return videoAsset || quickWatchVideoUrl ? (
                  <div style={{ marginTop: "1.5rem" }}>
                    <h3 style={{ margin: "0 0 1rem", fontSize: "1.1rem" }}>
                      🎬 Watch — {currentModule.title}
                    </h3>
                    <video controls style={{ width: "100%", borderRadius: "12px", background: "#000" }}>
                      <source src={displayVideoUrl} />
                    </video>
                    {quickWatchError && (
                      <p style={{ marginTop: "0.75rem", color: "var(--danger, #b3261e)", fontSize: "0.9rem" }}>
                        {quickWatchError}
                      </p>
                    )}
                  </div>
                ) : (
                  <div style={{ textAlign: "center", padding: "2rem", color: "var(--ink-soft)" }}>
                    {quickWatchError || "Manim animation is still being rendered..."}
                  </div>
                );
              })()}
            </div>

            <div className="content-footer">
              <div style={{ flex: 1, fontSize: "0.88rem", color: "var(--ink-soft)" }}>
                Module {currentModuleIndex + 1} of {lesson.modules.length}
              </div>
              <button
                className="button secondary"
                onClick={() => router.push("/profile")}
              >
                Back to Profile
              </button>
              {!isOnFinalModule && (
                <button
                  className="button secondary"
                  onClick={requestSkipToFinalTest}
                  disabled={isVerifyingSkipCode}
                  title="Requires demo confirmation code"
                >
                  {isVerifyingSkipCode ? "Verifying code..." : "Skip to Final Test (Demo)"}
                </button>
              )}
              <button
                className="button primary"
                onClick={() => setViewMode("knowledge-check")}
              >
                I&apos;m ready — Spar with AI 🥊
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
