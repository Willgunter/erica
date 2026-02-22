import { randomUUID } from "node:crypto";

import { NextResponse } from "next/server";
import type { AssessmentStartResponse, PracticeTrack, QuestionType } from "@/lib/assessment";
import { assessmentStartRequestSchema } from "@/lib/assessment";
import {
  buildInternalQuestionsFromLesson,
  serializeInternalQuestionsForSnapshot
} from "@/lib/assessment-generated";
import {
  buildAssessmentDefinition,
  inferTrackFromSubject,
  type AssessmentProfileConfig
} from "@/lib/assessment-engine";
import { saveDevAttempt, type DevAttemptRecord } from "@/lib/assessment-dev-store";
import { createSupabaseClient, createSupabaseServiceClient, resolveUserId } from "@/lib/supabase";

export const runtime = "nodejs";
const FLASK_API_URL = process.env.FLASK_API_URL || "http://localhost:8000";

function getBearerToken(headerValue: string | null): string | null {
  if (!headerValue) {
    return null;
  }

  const [type, token] = headerValue.split(" ");
  if (type?.toLowerCase() !== "bearer" || !token) {
    return null;
  }

  return token;
}

function isUserNotFound(errorMessage: string): boolean {
  return errorMessage.toLowerCase().includes("not found");
}

function isAlreadyExists(errorMessage: string): boolean {
  const lowered = errorMessage.toLowerCase();
  return lowered.includes("already") || lowered.includes("exists");
}

async function ensureDevAuthUserExists(userId: string): Promise<{ error: string; status: number } | null> {
  if (process.env.NODE_ENV === "production") {
    return { error: "Unauthorized", status: 401 };
  }

  let serviceClient: ReturnType<typeof createSupabaseServiceClient>;
  try {
    serviceClient = createSupabaseServiceClient();
  } catch {
    return {
      error: "Local dev fallback requires SUPABASE_SERVICE_ROLE_KEY in your environment.",
      status: 500
    };
  }

  const { data, error } = await serviceClient.auth.admin.getUserById(userId);
  if (data?.user) {
    return null;
  }

  if (error && !isUserNotFound(error.message)) {
    return { error: error.message, status: 500 };
  }

  const { error: createError } = await serviceClient.auth.admin.createUser({
    id: userId,
    email: `dev-${userId}@local.erica.test`,
    password: `${userId.slice(0, 8)}Dev!123`,
    email_confirm: true,
    user_metadata: { source: "local-dev-assessment" }
  });

  if (createError && !isAlreadyExists(createError.message)) {
    return { error: createError.message, status: 500 };
  }

  return null;
}

function isMissingAssessmentSchema(errorMessage: string | undefined): boolean {
  if (!errorMessage) {
    return false;
  }

  const lowered = errorMessage.toLowerCase();
  return (
    lowered.includes("assessment_profiles") ||
    lowered.includes("lesson_assessment_config") ||
    lowered.includes("assessment_attempts") ||
    lowered.includes("assessment_outcomes")
  );
}

function isMissingProfileSchema(errorMessage: string | undefined): boolean {
  if (!errorMessage) {
    return false;
  }

  const lowered = errorMessage.toLowerCase();
  return lowered.includes("profiles") && lowered.includes("could not find");
}

function normalizeBaseUrl(url: string): string {
  return url.replace(/\/+$/, "");
}

function buildCandidateBaseUrls(configuredBaseUrl: string): string[] {
  return [
    configuredBaseUrl,
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5000",
    "http://127.0.0.1:5000"
  ]
    .map((url) => normalizeBaseUrl(url).replace(/\/api\/?$/, ""))
    .filter(Boolean)
    .filter((url, index, all) => all.indexOf(url) === index);
}

async function fetchLessonForAssessment(lessonId: string): Promise<Record<string, unknown> | null> {
  if (!lessonId || lessonId === "ad-hoc") {
    return null;
  }

  const targets = buildCandidateBaseUrls(FLASK_API_URL).map(
    (base) => `${base}/api/lesson/${encodeURIComponent(lessonId)}`
  );

  for (const target of targets) {
    try {
      const response = await fetch(target, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        },
        cache: "no-store"
      });

      if (!response.ok) {
        continue;
      }

      const payload = (await response.json()) as unknown;
      if (payload && typeof payload === "object" && !Array.isArray(payload)) {
        return payload as Record<string, unknown>;
      }
    } catch {
      continue;
    }
  }

  return null;
}

type DbAssessmentProfileRow = {
  subject: string;
  exam_name: string | null;
  practice_track: PracticeTrack;
  exam_style: string;
  allowed_question_types: QuestionType[] | null;
  ui_constraints: Record<string, unknown> | null;
};

type DbLessonOverrideRow = {
  lesson_id: string;
  track_override: PracticeTrack | null;
  exam_name_override: string | null;
  question_type_order: QuestionType[] | null;
  ui_constraints_override: Record<string, unknown> | null;
  is_active: boolean;
};

function coerceQuestionTypes(values: unknown): QuestionType[] {
  if (!Array.isArray(values)) {
    return [];
  }

  return values.filter(
    (value): value is QuestionType =>
      value === "mcq" || value === "short_answer" || value === "open_ended" || value === "code"
  );
}

function mergeProfileConfig(
  profileRow: DbAssessmentProfileRow | null,
  lessonOverrideRow: DbLessonOverrideRow | null
): Partial<AssessmentProfileConfig> {
  const sourceUi = profileRow?.ui_constraints ?? {};
  const overrideUi = lessonOverrideRow?.ui_constraints_override ?? {};

  const durationSource =
    typeof overrideUi.duration_seconds === "number"
      ? overrideUi.duration_seconds
      : typeof sourceUi.duration_seconds === "number"
        ? sourceUi.duration_seconds
        : undefined;

  const autosaveSource =
    typeof overrideUi.autosave_enabled === "boolean"
      ? overrideUi.autosave_enabled
      : typeof sourceUi.autosave_enabled === "boolean"
        ? sourceUi.autosave_enabled
        : undefined;

  const resumeSource =
    typeof overrideUi.resume_enabled === "boolean"
      ? overrideUi.resume_enabled
      : typeof sourceUi.resume_enabled === "boolean"
        ? sourceUi.resume_enabled
        : undefined;

  const sectionTimeLimits = {
    ...(typeof sourceUi.section_time_limits === "object" && sourceUi.section_time_limits !== null
      ? (sourceUi.section_time_limits as Record<string, unknown>)
      : {}),
    ...(typeof overrideUi.section_time_limits === "object" && overrideUi.section_time_limits !== null
      ? (overrideUi.section_time_limits as Record<string, unknown>)
      : {})
  };

  return {
    examStyle: profileRow?.exam_style,
    durationSeconds: typeof durationSource === "number" ? durationSource : undefined,
    autosaveEnabled: autosaveSource,
    resumeEnabled: resumeSource,
    sectionTimeLimits: {
      mcq: typeof sectionTimeLimits.mcq === "number" ? sectionTimeLimits.mcq : null,
      written: typeof sectionTimeLimits.written === "number" ? sectionTimeLimits.written : null,
      coding: typeof sectionTimeLimits.coding === "number" ? sectionTimeLimits.coding : null
    }
  };
}

function defaultClassName(track: PracticeTrack): string {
  if (track === "computer_science") {
    return "Computer Science Practice";
  }
  if (track === "biology") {
    return "Biology Practice";
  }
  return "General Learning";
}

function defaultSubject(track: PracticeTrack): string {
  if (track === "computer_science") {
    return "Computer science";
  }
  if (track === "biology") {
    return "Biology";
  }
  return "General learning";
}

function normalizeSubjectForProfileLookup(subject: string): string {
  const normalized = subject.trim().toLowerCase();
  if (!normalized) {
    return "general learning";
  }
  if (normalized.includes("computer") || normalized.includes("program") || normalized.includes("coding")) {
    return "computer science";
  }
  if (normalized.includes("bio") || normalized.includes("cell") || normalized.includes("genetic")) {
    return "biology";
  }
  return normalized;
}

async function resolveUserSubject(
  supabase: ReturnType<typeof createSupabaseClient> | ReturnType<typeof createSupabaseServiceClient>,
  userId: string
): Promise<string | null> {
  const { data, error } = await supabase.from("profiles").select("subject").eq("user_id", userId).maybeSingle();
  if (error) {
    if (isMissingProfileSchema(error.message)) {
      return null;
    }
    throw new Error(error.message);
  }

  if (!data || typeof data.subject !== "string") {
    return null;
  }

  return data.subject;
}

async function resolveAssessmentProfile(
  supabase: ReturnType<typeof createSupabaseClient> | ReturnType<typeof createSupabaseServiceClient>,
  normalizedSubject: string,
  examName: string | null
): Promise<DbAssessmentProfileRow | null> {
  const { data, error } = await supabase
    .from("assessment_profiles")
    .select("subject, exam_name, practice_track, exam_style, allowed_question_types, ui_constraints")
    .eq("subject", normalizedSubject)
    .limit(5);

  if (error) {
    if (isMissingAssessmentSchema(error.message)) {
      return null;
    }
    throw new Error(error.message);
  }

  if (!data || data.length === 0) {
    return null;
  }

  const typed = data as DbAssessmentProfileRow[];
  if (examName) {
    const directMatch = typed.find((entry) => entry.exam_name?.toLowerCase() === examName.toLowerCase());
    if (directMatch) {
      return directMatch;
    }
  }

  return typed.find((entry) => entry.exam_name === null) ?? typed[0];
}

async function resolveLessonOverride(
  supabase: ReturnType<typeof createSupabaseClient> | ReturnType<typeof createSupabaseServiceClient>,
  lessonId: string
): Promise<DbLessonOverrideRow | null> {
  const { data, error } = await supabase
    .from("lesson_assessment_config")
    .select("lesson_id, track_override, exam_name_override, question_type_order, ui_constraints_override, is_active")
    .eq("lesson_id", lessonId)
    .eq("is_active", true)
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();

  if (error) {
    if (isMissingAssessmentSchema(error.message)) {
      return null;
    }
    throw new Error(error.message);
  }

  return (data as DbLessonOverrideRow | null) ?? null;
}

export async function POST(request: Request) {
  const accessToken = getBearerToken(request.headers.get("authorization"));
  const devUserId = request.headers.get("x-dev-user-id");
  const resolvedUser = await resolveUserId(accessToken, devUserId);

  if ("error" in resolvedUser) {
    return NextResponse.json({ error: resolvedUser.error }, { status: resolvedUser.status });
  }

  let body: unknown = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const parsedRequest = assessmentStartRequestSchema.safeParse(body);
  if (!parsedRequest.success) {
    return NextResponse.json(
      {
        error: "Invalid assessment start payload",
        details: parsedRequest.error.issues
      },
      { status: 400 }
    );
  }

  const useDevFallback =
    process.env.NODE_ENV !== "production" && Boolean(devUserId) && resolvedUser.userId === devUserId;
  if (useDevFallback) {
    const ensureUserError = await ensureDevAuthUserExists(resolvedUser.userId);
    if (ensureUserError) {
      return NextResponse.json({ error: ensureUserError.error }, { status: ensureUserError.status });
    }
  }

  const supabase = useDevFallback
    ? createSupabaseServiceClient()
    : createSupabaseClient(accessToken ?? undefined);

  const lessonId = parsedRequest.data.lesson_id ?? "ad-hoc";
  const classNameFromRequest = parsedRequest.data.class_name?.trim() ?? null;

  let subjectFromProfile: string | null = null;
  try {
    subjectFromProfile = await resolveUserSubject(supabase, resolvedUser.userId);
  } catch (error) {
    return NextResponse.json({ error: (error as Error).message }, { status: 500 });
  }

  const initialSubject = parsedRequest.data.subject ?? subjectFromProfile ?? "General learning";
  const normalizedSubject = normalizeSubjectForProfileLookup(initialSubject);

  let profileRow: DbAssessmentProfileRow | null = null;
  let lessonOverrideRow: DbLessonOverrideRow | null = null;

  try {
    profileRow = await resolveAssessmentProfile(
      supabase,
      normalizedSubject,
      parsedRequest.data.exam_name ?? null
    );
    lessonOverrideRow = await resolveLessonOverride(supabase, lessonId);
  } catch (error) {
    return NextResponse.json({ error: (error as Error).message }, { status: 500 });
  }

  const inferredTrack = inferTrackFromSubject(initialSubject);
  const resolvedTrack: PracticeTrack =
    parsedRequest.data.track_override ??
    lessonOverrideRow?.track_override ??
    profileRow?.practice_track ??
    inferredTrack;

  const resolvedSubject = initialSubject.trim().length > 0 ? initialSubject : defaultSubject(resolvedTrack);
  const resolvedExamName = lessonOverrideRow?.exam_name_override ?? parsedRequest.data.exam_name ?? profileRow?.exam_name ?? null;

  const mergedProfileConfig = mergeProfileConfig(profileRow, lessonOverrideRow);
  const lessonSnapshot = await fetchLessonForAssessment(lessonId);
  const generatedQuestions = buildInternalQuestionsFromLesson(lessonSnapshot);
  const hasGeneratedQuestions = generatedQuestions.length > 0;
  const definition = buildAssessmentDefinition(
    resolvedTrack,
    mergedProfileConfig,
    hasGeneratedQuestions ? generatedQuestions : undefined
  );

  const allowedTypes = hasGeneratedQuestions ? [] : coerceQuestionTypes(profileRow?.allowed_question_types);
  let internalQuestions =
    allowedTypes.length > 0
      ? definition.internalQuestions.filter((question) => allowedTypes.includes(question.type))
      : [...definition.internalQuestions];

  if (lessonOverrideRow?.question_type_order && lessonOverrideRow.question_type_order.length > 0) {
    const typeOrder = new Map<string, number>();
    lessonOverrideRow.question_type_order.forEach((entry, index) => {
      typeOrder.set(entry, index);
    });

    internalQuestions = [...internalQuestions].sort((a, b) => {
      const aIndex = typeOrder.get(a.type) ?? Number.MAX_SAFE_INTEGER;
      const bIndex = typeOrder.get(b.type) ?? Number.MAX_SAFE_INTEGER;
      return aIndex - bIndex;
    });
  }

  const publicById = new Map(definition.questions.map((question) => [question.id, question]));
  const publicQuestions = internalQuestions
    .map((question) => publicById.get(question.id))
    .filter((question): question is AssessmentStartResponse["questions"][number] => Boolean(question));

  const activeQuestionTypes = new Set(internalQuestions.map((question) => question.type));
  let sections = definition.sections.filter((section) =>
    section.question_types.some((type: QuestionType) => activeQuestionTypes.has(type))
  );
  if (sections.length === 0 && activeQuestionTypes.size > 0) {
    sections = [
      {
        id: "section-lesson-based",
        title: "Lesson-based questions",
        question_types: Array.from(activeQuestionTypes),
        time_limit_seconds: null
      }
    ];
  }

  const startedAt = new Date().toISOString();
  const attemptId = randomUUID();
  const className = classNameFromRequest ?? defaultClassName(resolvedTrack);

  const responsePayload: AssessmentStartResponse = {
    attempt_id: attemptId,
    lesson_id: lessonId,
    class_name: className,
    subject: resolvedSubject,
    exam_name: resolvedExamName,
    practice_track: resolvedTrack,
    exam_style: definition.examStyle,
    autosave_enabled: definition.autosaveEnabled,
    resume_enabled: definition.resumeEnabled,
    duration_seconds: definition.durationSeconds,
    started_at: startedAt,
    sections,
    questions: publicQuestions
  };

  const configSnapshot = {
    exam_style: definition.examStyle,
    duration_seconds: definition.durationSeconds,
    autosave_enabled: definition.autosaveEnabled,
    resume_enabled: definition.resumeEnabled,
    allowed_question_types:
      allowedTypes.length > 0
        ? allowedTypes
        : Array.from(new Set(internalQuestions.map((question) => question.type))),
    question_ids: internalQuestions.map((question) => question.id),
    sections,
    question_type_order: lessonOverrideRow?.question_type_order ?? null,
    generated_questions:
      hasGeneratedQuestions && internalQuestions.length > 0
        ? serializeInternalQuestionsForSnapshot(internalQuestions)
        : null
  };

  const attemptInsertPayload = {
    id: attemptId,
    user_id: resolvedUser.userId,
    lesson_id: lessonId,
    class_name: className,
    subject: resolvedSubject,
    exam_name: resolvedExamName,
    practice_track: resolvedTrack,
    status: "in_progress",
    config_snapshot: configSnapshot,
    started_at: startedAt
  };

  const { error: attemptError } = await supabase.from("assessment_attempts").insert(attemptInsertPayload);

  if (attemptError) {
    if (process.env.NODE_ENV !== "production" && isMissingAssessmentSchema(attemptError.message)) {
      const devRecord: DevAttemptRecord = {
        id: attemptId,
        user_id: resolvedUser.userId,
        lesson_id: lessonId,
        class_name: className,
        subject: resolvedSubject,
        exam_name: resolvedExamName,
        practice_track: resolvedTrack,
        status: "in_progress",
        config_snapshot: configSnapshot,
        started_at: startedAt
      };

      try {
        await saveDevAttempt(devRecord);
      } catch (storeError) {
        return NextResponse.json(
          {
            error: `Assessment schema missing and local fallback failed: ${(storeError as Error).message}`
          },
          { status: 500 }
        );
      }

      return NextResponse.json(responsePayload, { status: 200 });
    }

    return NextResponse.json({ error: attemptError.message }, { status: 500 });
  }

  return NextResponse.json(responsePayload, { status: 200 });
}
