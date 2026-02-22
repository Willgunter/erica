"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
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

function FlashcardDeck({ cards }: { cards: Flashcard[] }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [mastered, setMastered] = useState<Set<number>>(new Set());

  if (!cards || cards.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "2rem", color: "var(--ink-soft)" }}>
        No flashcards for this module yet.
      </div>
    );
  }

  const card = cards[index];

  const handleNext = (didMaster: boolean) => {
    if (didMaster) setMastered((prev) => new Set([...prev, index]));
    setFlipped(false);
    setTimeout(() => setIndex((i) => (i + 1) % cards.length), 120);
  };

  const handlePrev = () => {
    setFlipped(false);
    setTimeout(() => setIndex((i) => (i - 1 + cards.length) % cards.length), 120);
  };

  return (
    <div className="flashcard-deck">
      <div className="flashcard-meta">
        <span>{index + 1} / {cards.length}</span>
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
          style={{ width: `${(mastered.size / cards.length) * 100}%` }}
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
  const router = useRouter();
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [viewMode, setViewMode] = useState<ViewMode>("content");
  const [learningMode, setLearningMode] = useState<LearningMode>("flashcards");
  const [completedModules, setCompletedModules] = useState<Set<string>>(new Set());

  const currentModule = lesson.modules[currentModuleIndex];

  const totalModules = lesson.modules.length;
  const overallProgress = totalModules > 0
    ? Math.round(((completedModules.size + (viewMode === "knowledge-check" ? 0.5 : 0)) / totalModules) * 100)
    : 0;

  const getModuleAssets = (moduleId: string) =>
    lesson.media_assets?.filter((a) => a.module_id === moduleId) || [];

  const getReadyAsset = (moduleId: string, kind: "visual" | "audio") => {
    const assets = getModuleAssets(moduleId);
    const asset = assets.find((a) => {
      const aKind = a.kind || (a.asset_type === "video" ? "visual" : a.asset_type === "audio" ? "audio" : null);
      const aUrl = a.url || a.storage_url;
      const aStatus = a.status;
      const isReady = aStatus === "ready" || aStatus === "completed";
      return aKind === kind && isReady && aUrl;
    });
    if (!asset) return null;
    return { ...asset, url: asset.url || asset.storage_url };
  };

  const hasAudio = currentModule ? !!getReadyAsset(currentModule.module_id, "audio") : false;
  const hasVideo = currentModule ? !!getReadyAsset(currentModule.module_id, "visual") : false;

  const handleCheckpointComplete = (_sessionId: string) => {
    setCompletedModules((prev) => new Set([...prev, currentModule.module_id]));

    const nextIndex = currentModuleIndex + 1;
    if (nextIndex < lesson.modules.length) {
      setCurrentModuleIndex(nextIndex);
      setLearningMode("flashcards");
      setViewMode("content");
    } else {
      setViewMode("content");
      router.push("/test");
    }
  };

  const handleModuleSelect = (index: number) => {
    setCurrentModuleIndex(index);
    setLearningMode("flashcards");
    setViewMode("content");
  };

  if (viewMode === "knowledge-check" && currentModule) {
    return (
      <KnowledgeCheck
        lesson={{ id: lesson.id }}
        module={{
          module_id: currentModule.module_id,
          title: currentModule.title,
          objective: currentModule.objective,
        }}
        checkpoint={currentModule.checkpoint}
        onComplete={handleCheckpointComplete}
      />
    );
  }

  const isAllComplete = completedModules.size === lesson.modules.length;

  const tabs: { id: LearningMode; label: string; disabled?: boolean }[] = [
    { id: "flashcards", label: "📇 Flashcards" },
    { id: "concept", label: "📖 Concept" },
    { id: "listen", label: "🎧 Listen", disabled: !hasAudio },
    { id: "watch", label: "🎬 Watch", disabled: !hasVideo },
  ];

  return (
    <div className="lesson-container">
      {/* Sidebar */}
      <div className="lesson-sidebar">
        <div className="sidebar-header">
          <h2 className="sidebar-title">{lesson.title}</h2>
          <p className="sidebar-subtitle">{lesson.subject}</p>
        </div>

        <div className="module-list">
          {lesson.modules.map((mod, idx) => {
            const isActive = idx === currentModuleIndex;
            const isDone = completedModules.has(mod.module_id);

            return (
              <div
                key={mod.module_id}
                className={`module-item ${isActive ? "active" : ""} ${isDone ? "completed" : ""}`}
              >
                <div className="module-header" onClick={() => handleModuleSelect(idx)}>
                  <div className="module-number">{isDone ? "✓" : idx + 1}</div>
                  <div className="module-title">{mod.title}</div>
                  <div style={{ fontSize: "0.75rem", color: "var(--ink-soft)" }}>
                    {mod.estimated_minutes}m
                  </div>
                </div>
                {isActive && (
                  <div className="step-list">
                    {tabs.filter((t) => !t.disabled).map((t) => (
                      <div
                        key={t.id}
                        className={`step-item ${learningMode === t.id && viewMode === "content" ? "active" : ""}`}
                        style={{ cursor: "pointer" }}
                        onClick={() => { setLearningMode(t.id); setViewMode("content"); }}
                      >
                        <span className="step-icon">{t.label.split(" ")[0]}</span>
                        {t.label.split(" ").slice(1).join(" ")}
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
            <h1 style={{ margin: 0, fontSize: "1.2rem", fontWeight: 700 }}>{currentModule?.title}</h1>
            <div style={{ fontSize: "0.85rem", color: "var(--ink-soft)" }}>
              {lesson.subject} · {currentModule?.estimated_minutes}min
            </div>
          </div>
          <p className="breadcrumb" style={{ marginTop: "0.3rem" }}>{currentModule?.objective}</p>

          {/* Mode tabs */}
          {!isAllComplete && (
            <div className="mode-tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  className={`mode-tab ${learningMode === tab.id ? "active" : ""}`}
                  onClick={() => !tab.disabled && setLearningMode(tab.id)}
                  disabled={tab.disabled}
                  title={tab.disabled ? "Not available for this module" : undefined}
                >
                  {tab.label}
                </button>
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
              <button
                className="button primary"
                onClick={() => {
                  router.push("/test");
                }}
                style={{ fontSize: "1.1rem", padding: "0.8rem 2rem" }}
              >
                Continue to Final Test →
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="content-main">
              {learningMode === "flashcards" && (
                <FlashcardDeck cards={currentModule?.flashcards || []} />
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
                    Audio is still being generated…
                  </div>
                );
              })()}

              {learningMode === "watch" && currentModule && (() => {
                const videoAsset = getReadyAsset(currentModule.module_id, "visual");
                return videoAsset ? (
                  <div style={{ marginTop: "1.5rem" }}>
                    <h3 style={{ margin: "0 0 1rem", fontSize: "1.1rem" }}>🎬 Animation — {currentModule.title}</h3>
                    <video controls style={{ width: "100%", borderRadius: "12px", background: "#000" }}>
                      <source src={videoAsset.url!} />
                    </video>
                  </div>
                ) : (
                  <div style={{ textAlign: "center", padding: "2rem", color: "var(--ink-soft)" }}>
                    Animation is still being rendered…
                  </div>
                );
              })()}
            </div>

            <div className="content-footer">
              <div style={{ flex: 1, fontSize: "0.88rem", color: "var(--ink-soft)" }}>
                Module {currentModuleIndex + 1} of {lesson.modules.length}
              </div>
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
