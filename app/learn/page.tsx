"use client";

import { createClient } from "@supabase/supabase-js";
import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import type {
  AssessmentQuestion,
  AssessmentSection,
  AssessmentStartResponse,
  AssessmentSubmitResponse,
  CodeLanguage,
  PracticeTrack
} from "@/lib/assessment";

type Phase = "sparring" | "quiz" | "results";

type StoredChunk = {
  source?: string;
  text?: string;
};

type ReviewedItem = {
  id: string;
  prompt: string;
  userResponse: string;
  expected: string;
  isCorrect: boolean;
  explanation: string;
  manualReviewRequired: boolean;
};

type SectionScore = {
  label: string;
  correct: number;
  total: number;
};

type QuizResult = {
  correctCount: number;
  totalCount: number;
  percentage: number;
  reviewedItems: ReviewedItem[];
  sectionScores: SectionScore[];
  needsReview: boolean;
  focusAreas: string[];
  recommendations: string[];
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

type TrackConfig = {
  track: PracticeTrack;
  title: string;
  examStyle: string;
  description: string;
};

type CodeCheckResult = {
  passedCount: number;
  totalCount: number;
  details: Array<{ label: string; passed: boolean; message: string }>;
};

type StoredAttemptDraft = {
  assessment: AssessmentStartResponse;
  answers: Record<string, number>;
  writtenAnswers: Record<string, string>;
  codeAnswers: Record<string, string>;
  codeLanguages: Record<string, CodeLanguage>;
  deadlineIso: string | null;
};

type McqQuestion = Extract<AssessmentQuestion, { type: "mcq" }>;
type WrittenQuestion = Extract<AssessmentQuestion, { type: "short_answer" | "open_ended" }>;
type CodeQuestion = Extract<AssessmentQuestion, { type: "code" }>;

const QUIZ_SUMMARY_STORAGE_KEY = "erica_latest_quiz_summary";
const LESSON_HISTORY_STORAGE_KEY = "erica_profile_lesson_history";
const CONTENT_CHUNKS_STORAGE_KEY = "erica_content_chunks";
const ACTIVE_ATTEMPT_STORAGE_KEY = "erica_active_assessment_attempt";
const SUPABASE_TOKEN_STORAGE_KEY = "supabaseAccessToken";
const DEV_USER_ID_STORAGE_KEY = "supabaseDevUserId";

const TRACK_CONFIGS: TrackConfig[] = [
  {
    track: "computer_science",
    title: "Computer Science Exam",
    examStyle: "Coding challenge + technical multiple choice",
    description: "Mirrors coding-test environments with a code box, submit check, and targeted MCQs."
  },
  {
    track: "biology",
    title: "Biology Quiz",
    examStyle: "Multiple choice + short answer + open response",
    description: "Matches biology-style assessment with concept checks and written explanations."
  },
  {
    track: "general",
    title: "General Learning Quiz",
    examStyle: "Multiple choice",
    description: "Default low-friction quiz format for mixed or unknown subjects."
  }
];

function parseStoredChunks(raw: string | null): StoredChunk[] {
  if (!raw) {
    return [];
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed
      .filter((entry): entry is StoredChunk => typeof entry === "object" && entry !== null)
      .map((entry) => ({
        source: typeof entry.source === "string" ? entry.source : undefined,
        text: typeof entry.text === "string" ? entry.text : undefined
      }));
  } catch {
    return [];
  }
}

function parseStoredSummaryHistory(raw: string | null): StoredQuizSummary[] {
  if (!raw) {
    return [];
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed
      .filter((entry): entry is StoredQuizSummary => typeof entry === "object" && entry !== null)
      .map((entry) => ({
        className: typeof entry.className === "string" ? entry.className : "General Learning",
        completedAt: typeof entry.completedAt === "string" ? entry.completedAt : new Date().toISOString(),
        correctCount: typeof entry.correctCount === "number" ? entry.correctCount : 0,
        incorrectCount: typeof entry.incorrectCount === "number" ? entry.incorrectCount : 0,
        totalCount: typeof entry.totalCount === "number" ? entry.totalCount : 0,
        percentage: typeof entry.percentage === "number" ? entry.percentage : 0,
        needsReview: Boolean(entry.needsReview),
        focusAreas: Array.isArray(entry.focusAreas)
          ? entry.focusAreas.filter((item): item is string => typeof item === "string")
          : [],
        practiceTrack:
          entry.practiceTrack === "computer_science" ||
          entry.practiceTrack === "biology" ||
          entry.practiceTrack === "general"
            ? entry.practiceTrack
            : "general",
        examStyle: typeof entry.examStyle === "string" ? entry.examStyle : "Multiple choice",
        sectionScores: Array.isArray(entry.sectionScores)
          ? entry.sectionScores
              .filter((item): item is SectionScore => typeof item === "object" && item !== null)
              .map((item) => ({
                label: typeof item.label === "string" ? item.label : "Section",
                correct: typeof item.correct === "number" ? item.correct : 0,
                total: typeof item.total === "number" ? item.total : 0
              }))
          : [],
        recommendations: Array.isArray(entry.recommendations)
          ? entry.recommendations.filter((item): item is string => typeof item === "string")
          : []
      }));
  } catch {
    return [];
  }
}

function parseStoredAttemptDraft(raw: string | null): StoredAttemptDraft | null {
  if (!raw) {
    return null;
  }

  try {
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") {
      return null;
    }

    const maybeDraft = parsed as Partial<StoredAttemptDraft>;
    if (!maybeDraft.assessment || typeof maybeDraft.assessment !== "object") {
      return null;
    }

    const assessment = maybeDraft.assessment as AssessmentStartResponse;
    if (!assessment.attempt_id || !Array.isArray(assessment.questions)) {
      return null;
    }

    const parsedCodeAnswers =
      maybeDraft.codeAnswers && typeof maybeDraft.codeAnswers === "object" && !Array.isArray(maybeDraft.codeAnswers)
        ? (maybeDraft.codeAnswers as Record<string, unknown>)
        : {};

    const parsedCodeLanguages =
      maybeDraft.codeLanguages && typeof maybeDraft.codeLanguages === "object" && !Array.isArray(maybeDraft.codeLanguages)
        ? (maybeDraft.codeLanguages as Record<string, unknown>)
        : {};

    const codeAnswers: Record<string, string> = {};
    for (const [questionId, value] of Object.entries(parsedCodeAnswers)) {
      if (typeof value === "string") {
        codeAnswers[questionId] = value;
      }
    }

    const codeLanguages: Record<string, CodeLanguage> = {};
    for (const [questionId, value] of Object.entries(parsedCodeLanguages)) {
      if (value === "javascript" || value === "python") {
        codeLanguages[questionId] = value;
      }
    }

    if (Object.keys(codeAnswers).length === 0) {
      const legacyCodeAnswer = typeof (maybeDraft as Record<string, unknown>).codeAnswer === "string"
        ? ((maybeDraft as Record<string, unknown>).codeAnswer as string)
        : "";
      const legacyCodeLanguage =
        (maybeDraft as Record<string, unknown>).codeLanguage === "python" ? "python" : "javascript";
      const firstCodeQuestion = assessment.questions.find((question) => question.type === "code") as
        | CodeQuestion
        | undefined;

      if (legacyCodeAnswer && firstCodeQuestion) {
        codeAnswers[firstCodeQuestion.id] = legacyCodeAnswer;
      }
      if (legacyCodeLanguage && firstCodeQuestion && !codeLanguages[firstCodeQuestion.id]) {
        codeLanguages[firstCodeQuestion.id] = legacyCodeLanguage;
      }
    }

    return {
      assessment,
      answers:
        maybeDraft.answers && typeof maybeDraft.answers === "object"
          ? (maybeDraft.answers as Record<string, number>)
          : {},
      writtenAnswers:
        maybeDraft.writtenAnswers && typeof maybeDraft.writtenAnswers === "object"
          ? (maybeDraft.writtenAnswers as Record<string, string>)
          : {},
      codeAnswers,
      codeLanguages,
      deadlineIso: typeof maybeDraft.deadlineIso === "string" ? maybeDraft.deadlineIso : null
    };
  } catch {
    return null;
  }
}

function inferTrackFromChunks(chunks: StoredChunk[]): PracticeTrack {
  const corpus = chunks
    .map((chunk) => `${chunk.source ?? ""} ${chunk.text ?? ""}`.toLowerCase())
    .join(" ");

  if (!corpus.trim()) {
    return "general";
  }

  const csSignals = [
    "python",
    "javascript",
    "java",
    "leetcode",
    "algorithm",
    "data structure",
    "runtime",
    "complexity",
    "code"
  ];
  const bioSignals = [
    "biology",
    "cell",
    "photosynthesis",
    "mitochondria",
    "dna",
    "ecosystem",
    "respiration",
    "enzyme"
  ];

  const csHits = csSignals.filter((signal) => corpus.includes(signal)).length;
  const bioHits = bioSignals.filter((signal) => corpus.includes(signal)).length;

  if (csHits > bioHits && csHits > 0) {
    return "computer_science";
  }
  if (bioHits > csHits && bioHits > 0) {
    return "biology";
  }
  return "general";
}

function deriveClassName(chunks: StoredChunk[], selectedTrack: PracticeTrack): string {
  if (chunks.length > 0) {
    const first = chunks[0];
    const source = (first.source ?? "").trim();
    if (source && source.toLowerCase() !== "topic") {
      return source.replace(/\.[^/.]+$/, "");
    }

    const text = (first.text ?? "").trim();
    if (text) {
      return text.slice(0, 48);
    }
  }

  if (selectedTrack === "computer_science") {
    return "Computer Science Practice";
  }
  if (selectedTrack === "biology") {
    return "Biology Practice";
  }
  return "General Learning";
}

function inferSubjectHint(track: PracticeTrack): string {
  if (track === "computer_science") {
    return "Computer science";
  }
  if (track === "biology") {
    return "Biology";
  }
  return "General learning";
}

function phaseMeta(phase: Phase): { stepLabel: string; progress: string; title: string } {
  if (phase === "sparring") {
    return {
      stepLabel: "Step 3 of 5: Sparring",
      progress: "60%",
      title: "Sparring Partner / General Learning"
    };
  }
  if (phase === "quiz") {
    return {
      stepLabel: "Step 4 of 5: Quizzes and tests",
      progress: "80%",
      title: "Adaptive practice test"
    };
  }
  return {
    stepLabel: "Step 5 of 5: Results",
    progress: "100%",
    title: "Quiz results"
  };
}

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

  const [phase, setPhase] = useState<Phase>("sparring");
  const [storedChunks, setStoredChunks] = useState<StoredChunk[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<PracticeTrack>("general");

  const [assessment, setAssessment] = useState<AssessmentStartResponse | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [writtenAnswers, setWrittenAnswers] = useState<Record<string, string>>({});
  const [codeAnswers, setCodeAnswers] = useState<Record<string, string>>({});
  const [codeLanguages, setCodeLanguages] = useState<Record<string, CodeLanguage>>({});
  const [codeCheckPreviews, setCodeCheckPreviews] = useState<Record<string, CodeCheckResult | null>>({});

  const [quizError, setQuizError] = useState<string | null>(null);
  const [result, setResult] = useState<QuizResult | null>(null);

  const [isLoadingAssessment, setIsLoadingAssessment] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [redirectSeconds, setRedirectSeconds] = useState<number | null>(null);
  const [timeRemainingSeconds, setTimeRemainingSeconds] = useState<number | null>(null);
  const [deadlineIso, setDeadlineIso] = useState<string | null>(null);

  const autoSubmittedRef = useRef(false);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    const parsedChunks = parseStoredChunks(window.sessionStorage.getItem(CONTENT_CHUNKS_STORAGE_KEY));
    setStoredChunks(parsedChunks);
    setSelectedTrack(inferTrackFromChunks(parsedChunks));

    const draft = parseStoredAttemptDraft(window.sessionStorage.getItem(ACTIVE_ATTEMPT_STORAGE_KEY));
    if (!draft) {
      return;
    }

    setAssessment(draft.assessment);
    setSelectedTrack(draft.assessment.practice_track);
    setAnswers(draft.answers);
    setWrittenAnswers(draft.writtenAnswers);
    setCodeAnswers(draft.codeAnswers);
    setCodeLanguages(draft.codeLanguages);
    setDeadlineIso(draft.deadlineIso);

    if (draft.deadlineIso) {
      const remaining = Math.max(
        0,
        Math.floor((new Date(draft.deadlineIso).getTime() - Date.now()) / 1000)
      );
      setTimeRemainingSeconds(remaining);
    }

    setPhase("quiz");
  }, []);

  const meta = useMemo(() => phaseMeta(phase), [phase]);

  const activeConfig = useMemo(() => {
    if (assessment) {
      return {
        track: assessment.practice_track,
        title:
          assessment.practice_track === "computer_science"
            ? "Computer Science Exam"
            : assessment.practice_track === "biology"
              ? "Biology Quiz"
              : "General Learning Quiz",
        examStyle: assessment.exam_style,
        description:
          assessment.practice_track === "computer_science"
            ? "Mirrors coding-test environments with a code box, submit check, and targeted MCQs."
            : assessment.practice_track === "biology"
              ? "Matches biology-style assessment with concept checks and written explanations."
              : "Default low-friction quiz format for mixed or unknown subjects."
      };
    }

    return getTrackConfig(selectedTrack);
  }, [assessment, selectedTrack]);

  const activeMcqQuestions = useMemo(
    () =>
      (assessment?.questions.filter((question) => question.type === "mcq") as McqQuestion[] | undefined) ?? [],
    [assessment]
  );

  const activeWrittenQuestions = useMemo(
    () =>
      (assessment?.questions.filter(
        (question) => question.type === "short_answer" || question.type === "open_ended"
      ) as WrittenQuestion[] | undefined) ?? [],
    [assessment]
  );

  const activeCodeQuestions = useMemo(
    () =>
      (assessment?.questions.filter((question) => question.type === "code") as CodeQuestion[] | undefined) ?? [],
    [assessment]
  );

  const totalItemCount = useMemo(() => {
    if (!assessment) {
      return 0;
    }
    return assessment.questions.length;
  }, [assessment]);

  const answeredCount = useMemo(() => {
    const mcqCount = activeMcqQuestions.filter((question) => answers[question.id] !== undefined).length;
    const writtenCount = activeWrittenQuestions.filter((question) => {
      const value = writtenAnswers[question.id];
      return Boolean(value && value.trim().length > 0);
    }).length;
    const codingCount = activeCodeQuestions.filter(
      (question) =>
        (codeAnswers[question.id] ?? "").trim().length > 0 &&
        (codeAnswers[question.id] ?? "").trim() !== question.starter_code.trim()
    ).length;
    return mcqCount + writtenCount + codingCount;
  }, [activeCodeQuestions, activeMcqQuestions, activeWrittenQuestions, answers, writtenAnswers, codeAnswers]);

  useEffect(() => {
    if (phase !== "results" || !result) {
      setRedirectSeconds(null);
      return;
    }

    setRedirectSeconds(7);
    const timer = window.setInterval(() => {
      setRedirectSeconds((previous) => {
        if (previous === null) {
          return previous;
        }
        if (previous <= 1) {
          window.clearInterval(timer);
          router.push("/profile");
          return 0;
        }
        return previous - 1;
      });
    }, 1000);
    return () => window.clearInterval(timer);
  }, [phase, result, router]);

  useEffect(() => {
    if (phase !== "quiz" || !deadlineIso) {
      return;
    }

    const timer = window.setInterval(() => {
      const remaining = Math.max(0, Math.floor((new Date(deadlineIso).getTime() - Date.now()) / 1000));
      setTimeRemainingSeconds(remaining);

      if (remaining === 0 && !autoSubmittedRef.current && !isSubmitting) {
        autoSubmittedRef.current = true;
        void submitQuiz({ allowPartial: true, triggeredByTimer: true });
      }
    }, 1000);

    return () => window.clearInterval(timer);
  }, [deadlineIso, phase, isSubmitting]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    if (phase !== "quiz" || !assessment) {
      return;
    }

    if (!assessment.autosave_enabled && !assessment.resume_enabled) {
      return;
    }

    const draft: StoredAttemptDraft = {
      assessment,
      answers,
      writtenAnswers,
      codeAnswers,
      codeLanguages,
      deadlineIso
    };

    window.sessionStorage.setItem(ACTIVE_ATTEMPT_STORAGE_KEY, JSON.stringify(draft));
  }, [phase, assessment, answers, writtenAnswers, codeAnswers, codeLanguages, deadlineIso]);

  function clearAttemptDraft() {
    if (typeof window === "undefined") {
      return;
    }

    window.sessionStorage.removeItem(ACTIVE_ATTEMPT_STORAGE_KEY);
  }

  function setAnswer(questionId: string, choiceIndex: number) {
    setAnswers((prev) => ({ ...prev, [questionId]: choiceIndex }));
    setQuizError(null);
  }

  function setWrittenAnswer(questionId: string, value: string) {
    setWrittenAnswers((prev) => ({ ...prev, [questionId]: value }));
    setQuizError(null);
  }

  function setCodeAnswerForQuestion(questionId: string, answer: string) {
    setCodeAnswers((prev) => ({ ...prev, [questionId]: answer }));
    setQuizError(null);
  }

  function setCodeLanguageForQuestion(questionId: string, language: CodeLanguage) {
    setCodeLanguages((prev) => ({ ...prev, [questionId]: language }));
    setQuizError(null);
  }

  function setCodeCheckPreviewForQuestion(questionId: string, result: CodeCheckResult | null) {
    setCodeCheckPreviews((prev) => ({ ...prev, [questionId]: result }));
  }

  async function startQuiz() {
    setQuizError(null);
    setIsLoadingAssessment(true);
    autoSubmittedRef.current = false;

    try {
      const authHeaders = await buildAuthHeaders();
      const response = await fetch("/api/assessment/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeaders
        },
        body: JSON.stringify({
          track_override: selectedTrack,
          subject: inferSubjectHint(selectedTrack),
          class_name: deriveClassName(storedChunks, selectedTrack)
        })
      });

      const payload = (await response.json()) as AssessmentStartResponse & { error?: string };
      if (!response.ok) {
        throw new Error(payload.error ?? "Failed to start assessment");
      }

      setAssessment(payload);
      setSelectedTrack(payload.practice_track);
      setAnswers({});
      setWrittenAnswers({});
      const codeQuestions = (payload.questions.filter((question) => question.type === "code") as CodeQuestion[]) ?? [];

      const initialCodeAnswers = Object.fromEntries(
        codeQuestions.map((question) => [
          question.id,
          question.starter_code
        ])
      );
      const initialCodeLanguages = Object.fromEntries(
        codeQuestions.map((question) => [
          question.id,
          question.default_language
        ])
      );

      setCodeAnswers(initialCodeAnswers);
      setCodeLanguages(initialCodeLanguages);
      setCodeCheckPreviews({});

      const deadline = new Date(Date.now() + payload.duration_seconds * 1000).toISOString();
      setDeadlineIso(deadline);
      setTimeRemainingSeconds(payload.duration_seconds);

      setResult(null);
      setPhase("quiz");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not start assessment.";
      setQuizError(message);
    } finally {
      setIsLoadingAssessment(false);
    }
  }

  function runMockCodeCheck(question: CodeQuestion) {
    const submission = codeAnswers[question.id] ?? "";
    if (!submission.trim()) {
      return;
    }

    const selectedLanguage = codeLanguages[question.id] ?? question.default_language;
    if (selectedLanguage !== "javascript") {
      setCodeCheckPreviewForQuestion(question.id, {
        passedCount: 0,
        totalCount: question.visible_tests.length,
        details: [
          {
            label: "preview",
            passed: false,
            message: "Preview checker currently supports JavaScript only. Full scoring still runs on submit."
          }
        ]
      });
      setQuizError(null);
      return;
    }

    const evaluation = runJavascriptPreview(submission, question);
    setCodeCheckPreviewForQuestion(question.id, evaluation);
    setQuizError(null);
  }

  function storeSummary(nextResult: QuizResult) {
    if (typeof window === "undefined" || !assessment) {
      return;
    }

    const summary: StoredQuizSummary = {
      className: deriveClassName(storedChunks, assessment.practice_track),
      completedAt: new Date().toISOString(),
      correctCount: nextResult.correctCount,
      incorrectCount: nextResult.totalCount - nextResult.correctCount,
      totalCount: nextResult.totalCount,
      percentage: nextResult.percentage,
      needsReview: nextResult.needsReview,
      focusAreas: nextResult.focusAreas,
      practiceTrack: assessment.practice_track,
      examStyle: assessment.exam_style,
      sectionScores: nextResult.sectionScores,
      recommendations: nextResult.recommendations
    };

    window.sessionStorage.setItem(QUIZ_SUMMARY_STORAGE_KEY, JSON.stringify(summary));
    const existing = parseStoredSummaryHistory(window.sessionStorage.getItem(LESSON_HISTORY_STORAGE_KEY));
    const nextHistory = [summary, ...existing].slice(0, 20);
    window.sessionStorage.setItem(LESSON_HISTORY_STORAGE_KEY, JSON.stringify(nextHistory));
  }

  async function submitQuiz(options?: { allowPartial?: boolean; triggeredByTimer?: boolean }) {
    if (!assessment) {
      setQuizError("Assessment session missing. Start the quiz again.");
      return;
    }

    const allowPartial = Boolean(options?.allowPartial);
    if (!allowPartial && answeredCount < totalItemCount) {
      const remaining = totalItemCount - answeredCount;
      setQuizError(`Complete all required responses before submitting. ${remaining} remaining.`);
      return;
    }

    setIsSubmitting(true);
    setQuizError(null);

    try {
      const responses: Array<
        | { question_id: string; question_type: "mcq"; selected_index: number }
        | { question_id: string; question_type: "short_answer" | "open_ended"; text_response: string }
        | {
            question_id: string;
            question_type: "code";
            code_submission: string;
            language: CodeLanguage;
          }
      > = [];

      for (const question of activeMcqQuestions) {
        const selectedIndex = answers[question.id];
        if (typeof selectedIndex === "number") {
          responses.push({
            question_id: question.id,
            question_type: "mcq",
            selected_index: selectedIndex
          });
        }
      }

      for (const question of activeWrittenQuestions) {
        const textResponse = (writtenAnswers[question.id] ?? "").trim();
        if (textResponse.length > 0) {
          responses.push({
            question_id: question.id,
            question_type: question.type,
            text_response: textResponse
          });
        }
      }

      for (const question of activeCodeQuestions) {
        const codeSubmission = (codeAnswers[question.id] ?? "").trim();
        const hasEditedCode = codeSubmission.length > 0 && codeSubmission !== question.starter_code.trim();
        if (hasEditedCode) {
          responses.push({
            question_id: question.id,
            question_type: "code",
            code_submission: codeSubmission,
            language: codeLanguages[question.id] ?? question.default_language
          });
        }
      }

      const authHeaders = await buildAuthHeaders();
      const response = await fetch("/api/assessment/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeaders
        },
        body: JSON.stringify({
          attempt_id: assessment.attempt_id,
          responses
        })
      });

      const payload = (await response.json()) as AssessmentSubmitResponse & { error?: string };
      if (!response.ok) {
        throw new Error(payload.error ?? "Failed to submit assessment");
      }

      const mappedResult = mapSubmitResponse(payload);
      storeSummary(mappedResult);

      setResult(mappedResult);
      setPhase("results");
      setRedirectSeconds(null);
      setTimeRemainingSeconds(null);
      setDeadlineIso(null);
      clearAttemptDraft();

      if (options?.triggeredByTimer) {
        setQuizError("Time expired. Your in-progress responses were submitted automatically.");
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not submit assessment.";
      setQuizError(message);
      autoSubmittedRef.current = false;
    } finally {
      setIsSubmitting(false);
    }
  }

  function retakeQuiz() {
    clearAttemptDraft();
    autoSubmittedRef.current = false;
    setAssessment(null);
    setAnswers({});
    setWrittenAnswers({});
    setCodeAnswers({});
    setCodeLanguages({});
    setCodeCheckPreviews({});
    setResult(null);
    setQuizError(null);
    setRedirectSeconds(null);
    setTimeRemainingSeconds(null);
    setDeadlineIso(null);
    setPhase("sparring");
  }

  function sectionLabelFromServer(section: AssessmentSection): string {
    if (section.id.includes("coding")) {
      return "Coding challenge";
    }
    if (section.id.includes("written")) {
      return "Written responses";
    }
    return "Multiple choice";
  }

  return (
    <main className="onboarding-shell">
      <header className="hero-band">
        <h1 className="hero-title">{meta.title}</h1>
        <p className="hero-sub">{meta.stepLabel}</p>
        <div className="progress-wrap" aria-hidden="true">
          <div className="progress-bar" style={{ width: meta.progress }} />
        </div>
      </header>

      <section className="onboarding-body learn-body">
        {phase === "sparring" && (
          <article className="step-card">
            <h2 className="step-title">General learning phase (stub)</h2>
            <p className="step-subtitle">
              This is a placeholder for the live sparring partner. Select the exam style and start an
              API-backed adaptive assessment.
            </p>

            <div className="sparring-stub">
              <p className="label">Current behavior</p>
              <ul className="stub-list">
                <li>Subject is inferred from uploaded material when possible</li>
                <li>You can override exam format before starting the test</li>
                <li>Question schema and scoring now come from backend assessment endpoints</li>
              </ul>
            </div>

            <div className="context-preview">
              <p className="label">Adaptive format selection (server-backed)</p>
              <div className="format-options">
                {TRACK_CONFIGS.map((config) => {
                  const isActive = config.track === selectedTrack;
                  return (
                    <button
                      key={config.track}
                      type="button"
                      className={`format-chip${isActive ? " active" : ""}`}
                      onClick={() => setSelectedTrack(config.track)}
                    >
                      <span className="format-chip-title">{config.title}</span>
                      <span className="format-chip-sub">{config.examStyle}</span>
                    </button>
                  );
                })}
              </div>
              <p className="helper">
                Active mode: {activeConfig.title} ({activeConfig.examStyle})
              </p>
              <p className="helper">{activeConfig.description}</p>
            </div>

            {storedChunks.length > 0 && (
              <div className="context-preview">
                <p className="label">Learning context snapshot</p>
                <ul className="context-list">
                  {storedChunks.slice(0, 5).map((chunk, index) => (
                    <li key={`${chunk.source ?? "topic"}-${index}`} className="context-item">
                      <strong>{chunk.source ?? "topic"}:</strong> {(chunk.text ?? "").slice(0, 140) || "No text found"}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="transcript-shell">
              <p className="label">Stub transcript</p>
              <div className="transcript-line transcript-line-ai">
                Tutor: We will practice in the same format as your real test.
              </div>
              <div className="transcript-line transcript-line-user">
                Student: Great, I want the format to feel familiar before exam day.
              </div>
              <div className="transcript-line transcript-line-ai">
                Tutor: Perfect. Start the adaptive test when ready.
              </div>
            </div>

            {quizError && <p className="error">{quizError}</p>}

            <footer className="footer">
              <button type="button" className="button secondary" onClick={() => router.push("/upload")}>
                Back
              </button>
              <button
                type="button"
                className="button primary"
                onClick={() => {
                  void startQuiz();
                }}
                disabled={isLoadingAssessment}
              >
                {isLoadingAssessment ? "Starting..." : "Start adaptive test"}
              </button>
            </footer>
          </article>
        )}

        {phase === "quiz" && assessment && (
          <article className="step-card">
            <h2 className="step-title">{activeConfig.title}</h2>
            <p className="step-subtitle">Format: {assessment.exam_style}. Complete all items before submission.</p>

            <p className="helper">
              Progress: {answeredCount}/{totalItemCount} responses completed
            </p>

            {timeRemainingSeconds !== null && (
              <p className={`timer-pill${timeRemainingSeconds <= 60 ? " warning" : ""}`}>
                Time remaining: {formatDuration(timeRemainingSeconds)}
              </p>
            )}

            {assessment.sections.length > 0 && (
              <div className="section-score-list">
                {assessment.sections.map((section) => (
                  <div key={section.id} className="section-score-item">
                    <p className="label">{sectionLabelFromServer(section)}</p>
                    <p className="profile-line">
                      {section.time_limit_seconds ? `${Math.floor(section.time_limit_seconds / 60)} min section` : "Untimed section"}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {activeCodeQuestions.map((question) => (
              <section key={question.id} className="coding-card">
                <p className="label">{question.title}</p>
                <p className="coding-prompt">{question.prompt}</p>
                <p className="code-hint">Function signature: {question.function_name}(...)</p>

                <div className="field">
                  <label className="label" htmlFor={`code-language-${question.id}`}>
                    Language
                  </label>
                  <select
                    id={`code-language-${question.id}`}
                    className="input"
                    value={codeLanguages[question.id] ?? question.default_language}
                    onChange={(event) => {
                      setCodeLanguageForQuestion(question.id, event.target.value as CodeLanguage);
                      setCodeCheckPreviewForQuestion(question.id, null);
                    }}
                  >
                    {question.allowed_languages.map((language) => (
                      <option key={language} value={language}>
                        {language}
                      </option>
                    ))}
                  </select>
                </div>

                <textarea
                  className="code-editor"
                  value={codeAnswers[question.id] ?? ""}
                  onChange={(event) => {
                    setCodeAnswerForQuestion(question.id, event.target.value);
                    setCodeCheckPreviewForQuestion(question.id, null);
                    setQuizError(null);
                  }}
                  spellCheck={false}
                />

                <div className="code-actions">
                  <button type="button" className="button secondary" onClick={() => runMockCodeCheck(question)}>
                    Run mock checker
                  </button>
                </div>

                {codeCheckPreviews[question.id] && (
                  <ul className="code-test-list">
                    {codeCheckPreviews[question.id]!.details.map((detail) => (
                      <li key={detail.label} className={`code-test-item${detail.passed ? " pass" : " fail"}`}>
                        <strong>{detail.label}:</strong> {detail.message}
                      </li>
                    ))}
                  </ul>
                )}
              </section>
            ))}

            <form
              className="quiz-form"
              onSubmit={(event) => {
                event.preventDefault();
                void submitQuiz();
              }}
            >
              {activeMcqQuestions.map((question, index) => (
                <fieldset key={question.id} className="question-card">
                  <legend className="question-prompt">
                    {index + 1}. {question.prompt}
                  </legend>
                  <div className="question-options">
                    {question.choices.map((choice, choiceIndex) => {
                      const checked = answers[question.id] === choiceIndex;
                      return (
                        <label key={`${question.id}-${choiceIndex}`} className={`choice${checked ? " active" : ""}`}>
                          <input
                            type="radio"
                            name={question.id}
                            checked={checked}
                            onChange={() => setAnswer(question.id, choiceIndex)}
                          />
                          <span>{choice}</span>
                        </label>
                      );
                    })}
                  </div>
                </fieldset>
              ))}

              {activeWrittenQuestions.map((question, index) => {
                const runningIndex = activeMcqQuestions.length + index + 1;
                return (
                  <div key={question.id} className="written-card">
                    <p className="question-prompt">
                      {runningIndex}. {question.prompt}
                    </p>
                    <textarea
                      className="written-input"
                      value={writtenAnswers[question.id] ?? ""}
                      onChange={(event) => setWrittenAnswer(question.id, event.target.value)}
                      placeholder={question.type === "short_answer" ? "Short response..." : "Open-ended response..."}
                    />
                  </div>
                );
              })}

              {quizError && <p className="error">{quizError}</p>}

              <footer className="footer">
                <button
                  type="button"
                  className="button secondary"
                  onClick={() => {
                    clearAttemptDraft();
                    setPhase("sparring");
                  }}
                >
                  Back to sparring
                </button>
                <button type="submit" className="button primary" disabled={isSubmitting}>
                  {isSubmitting ? "Submitting..." : "Submit test"}
                </button>
              </footer>
            </form>
          </article>
        )}

        {phase === "results" && result && (
          <article className="step-card">
            <h2 className="step-title">Test complete</h2>
            <p className="step-subtitle">
              Score: {result.correctCount}/{result.totalCount} ({result.percentage}%)
            </p>

            <div className="quiz-summary-grid">
              <div className="summary-stat">
                <p className="label">Correct</p>
                <p className="summary-value">{result.correctCount}</p>
              </div>
              <div className="summary-stat">
                <p className="label">Incorrect</p>
                <p className="summary-value">{result.totalCount - result.correctCount}</p>
              </div>
              <div className="summary-stat">
                <p className="label">Accuracy</p>
                <p className="summary-value">{result.percentage}%</p>
              </div>
            </div>

            <div className="section-score-list">
              {result.sectionScores.map((section) => (
                <div key={section.label} className="section-score-item">
                  <p className="label">{section.label}</p>
                  <p className="summary-value">
                    {section.correct}/{section.total}
                  </p>
                </div>
              ))}
            </div>

            {result.recommendations.length > 0 && (
              <div className="context-preview">
                <p className="label">Recommended next steps</p>
                <ul className="stub-list">
                  {result.recommendations.map((recommendation, index) => (
                    <li key={`${recommendation}-${index}`}>{recommendation}</li>
                  ))}
                </ul>
              </div>
            )}

            {redirectSeconds !== null && (
              <p className="helper">Redirecting to your profile in {redirectSeconds}s...</p>
            )}

            <ul className="result-list">
              {result.reviewedItems.map((item, index) => (
                <li key={item.id} className={`result-item${item.isCorrect ? " correct" : " incorrect"}`}>
                  <p className="result-prompt">
                    {index + 1}. {item.prompt}
                  </p>
                  <p className="result-answer">Your response: {item.userResponse}</p>
                  <p className="result-answer">Expected: {item.expected}</p>
                  <p className="result-explanation">{item.explanation}</p>
                  {item.manualReviewRequired && (
                    <p className="review-pill">Manual review required for final grading.</p>
                  )}
                </li>
              ))}
            </ul>

            <footer className="footer">
              <button type="button" className="button secondary" onClick={retakeQuiz}>
                Retake test
              </button>
              <button type="button" className="button primary" onClick={() => router.push("/profile")}>
                Go to profile now
              </button>
            </footer>
          </article>
        )}
      </section>
    </main>
  );
}
