"use client";

import { useCallback, useRef, useState } from "react";
import { useRouter } from "next/navigation";

type UploadedFile = {
  id: string;
  name: string;
  size: number;
  type: string;
  file: File;
  chunks?: Array<{ id: string; text: string; metadata: any }>;
  error?: string;
};

type TopicEntry = {
  id: string;
  value: string;
};

const ACCEPTED_TYPES = [
  "application/pdf",
  "text/plain",
  "text/markdown",
  "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  "application/vnd.ms-powerpoint",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/msword",
  "image/png",
  "image/jpeg",
  "image/webp"
];

const ACCEPTED_EXTENSIONS = ".pdf,.txt,.md,.pptx,.ppt,.docx,.doc,.png,.jpg,.jpeg,.webp";

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function fileIcon(type: string): string {
  if (type === "application/pdf") return "📄";
  if (type.startsWith("image/")) return "🖼️";
  if (type.includes("presentation") || type.includes("powerpoint")) return "📊";
  if (type.includes("word")) return "📝";
  return "📃";
}

export default function UploadPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [topics, setTopics] = useState<TopicEntry[]>([]);
  const [topicInput, setTopicInput] = useState("");
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "processing">("idle");

  const parseFile = async (file: File): Promise<{ chunks?: any[]; error?: string }> => {
    if (file.type.startsWith("image/")) {
      return { error: "Image parsing not yet supported. Please use PDF, PPTX, DOCX, or TXT files." };
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/parse", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        return { error: data.error || "Failed to parse file" };
      }

      return { chunks: data.chunks };
    } catch (err) {
      return { error: err instanceof Error ? err.message : "Failed to parse file" };
    }
  };

  const addFiles = useCallback(async (incoming: FileList | File[]) => {
    setStatus("processing");
    const list = Array.from(incoming);
    const added: UploadedFile[] = [];
    
    for (const file of list) {
      const result = await parseFile(file);
      added.push({
        id: crypto.randomUUID(),
        name: file.name,
        size: file.size,
        type: file.type,
        file,
        chunks: result.chunks,
        error: result.error,
      });
    }
    
    setFiles((prev) => [...prev, ...added]);
    setStatus("idle");
    setError(null);
  }, []);

  const onFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      addFiles(e.target.files);
      e.target.value = "";
    }
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files.length > 0) {
      addFiles(e.dataTransfer.files);
    }
  };

  const removeFile = (id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const addTopic = () => {
    const value = topicInput.trim();
    if (!value) return;
    if (topics.some((t) => t.value.toLowerCase() === value.toLowerCase())) {
      setTopicInput("");
      return;
    }
    setTopics((prev) => [...prev, { id: crypto.randomUUID(), value }]);
    setTopicInput("");
  };

  const removeTopic = (id: string) => {
    setTopics((prev) => prev.filter((t) => t.id !== id));
  };

  const handleTopicKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addTopic();
    }
  };

  const canProceed = files.length > 0 || topics.length > 0;

  const handleContinue = async () => {
    if (!canProceed) {
      setError("Add at least one file or topic before continuing.");
      return;
    }

    const failedFiles = files.filter((f) => f.error);
    if (failedFiles.length > 0) {
      setError(`Some files failed to parse: ${failedFiles.map((f) => f.name).join(", ")}. Please remove them or try different files.`);
      return;
    }

    setStatus("processing");
    setError(null);

    const chunks: Array<{ id?: string; source: string; text: string; metadata?: any }> = [];
    
    for (const file of files) {
      if (file.chunks) {
        chunks.push(...file.chunks.map((chunk) => ({
          id: chunk.id,
          source: file.name,
          text: chunk.text,
          metadata: chunk.metadata,
        })));
      }
    }
    
    chunks.push(...topics.map((t) => ({ source: "topic", text: t.value })));

    if (chunks.length === 0) {
      setError("No content could be extracted. Please try different files or add topics.");
      setStatus("idle");
      return;
    }

    sessionStorage.setItem("erica_content_chunks", JSON.stringify(chunks));
    router.push("/learn");
  };

  return (
    <main className="onboarding-shell">
      <header className="hero-band">
        <h1 className="hero-title">Upload your lesson content</h1>
        <p className="hero-sub">Step 2 of 5: Content</p>
        <div className="progress-wrap" aria-hidden="true">
          <div className="progress-bar" style={{ width: "40%" }} />
        </div>
      </header>

      <section className="onboarding-body">
        <article className="step-card">
          <h2 className="step-title">What are we learning from?</h2>
          <p className="step-subtitle">
            Drop in slides, PDFs, notes, practice tests, or just type a topic — Erica will build
            your lesson from whatever you provide.
          </p>

          <div
            className={`drop-zone${dragging ? " dragging" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") fileInputRef.current?.click(); }}
            aria-label="Upload files"
          >
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept={ACCEPTED_EXTENSIONS}
              style={{ display: "none" }}
              onChange={onFileInputChange}
            />
            <span className="drop-icon">☁️</span>
            <p className="drop-label">
              {dragging ? "Drop files here" : "Drag & drop files, or click to browse"}
            </p>
            <p className="drop-hint">PDF, PPTX, DOCX, TXT, MD, images — up to 50 MB each</p>
          </div>

          {files.length > 0 && (
            <ul className="file-list" aria-label="Uploaded files">
              {files.map((f) => (
                <li key={f.id} className="file-item" style={{ flexDirection: "column", alignItems: "flex-start" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "0.6rem", width: "100%" }}>
                    <span className="file-icon">{fileIcon(f.type)}</span>
                    <span className="file-name">{f.name}</span>
                    <span className="file-size">{formatBytes(f.size)}</span>
                    <button
                      type="button"
                      className="file-remove"
                      onClick={() => removeFile(f.id)}
                      aria-label={`Remove ${f.name}`}
                    >
                      ✕
                    </button>
                  </div>
                  {f.error && (
                    <p style={{ margin: "0.3rem 0 0 2rem", fontSize: "0.85rem", color: "#8c1a10" }}>
                      Error: {f.error}
                    </p>
                  )}
                  {f.chunks && (
                    <p style={{ margin: "0.3rem 0 0 2rem", fontSize: "0.85rem", color: "#085d49" }}>
                      ✓ Parsed {f.chunks.length} chunk{f.chunks.length !== 1 ? "s" : ""}
                    </p>
                  )}
                </li>
              ))}
            </ul>
          )}

          <div className="field" style={{ marginTop: "1.4rem" }}>
            <span className="label">Or type topics / general subjects</span>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <input
                className="input"
                value={topicInput}
                onChange={(e) => setTopicInput(e.target.value)}
                onKeyDown={handleTopicKeyDown}
                placeholder="e.g. Photosynthesis, The Cold War, Recursion…"
                maxLength={200}
              />
              <button type="button" className="button secondary" onClick={addTopic}>
                Add
              </button>
            </div>
            {topics.length > 0 && (
              <div className="chips" style={{ marginTop: "0.5rem" }}>
                {topics.map((t) => (
                  <span key={t.id} className="chip active" style={{ display: "flex", alignItems: "center", gap: "0.35rem" }}>
                    {t.value}
                    <button
                      type="button"
                      style={{ background: "none", border: "none", cursor: "pointer", padding: 0, lineHeight: 1, color: "inherit" }}
                      onClick={() => removeTopic(t.id)}
                      aria-label={`Remove topic ${t.value}`}
                    >
                      ✕
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>
        </article>

        {error && <p className="error">{error}</p>}

        <footer className="footer">
          <button
            type="button"
            className="button secondary"
            onClick={() => router.push("/onboarding")}
            disabled={status === "processing"}
          >
            Back
          </button>
          <button
            type="button"
            className="button primary"
            onClick={handleContinue}
            disabled={!canProceed || status === "processing"}
          >
            {status === "processing" ? "Processing…" : "Generate my lesson →"}
          </button>
        </footer>
      </section>
    </main>
  );
}
