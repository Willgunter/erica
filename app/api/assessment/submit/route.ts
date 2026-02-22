import { NextResponse } from "next/server";
import type {
  AssessmentSection,
  AssessmentSubmitResponse,
  PracticeTrack,
  QuestionType,
  ReviewedAssessmentItem
} from "@/lib/assessment";
import { assessmentSubmitRequestSchema } from "@/lib/assessment";
import {
  buildAssessmentDefinition,
  inferTrackFromSubject,
  scoreAssessmentSubmission,
  type AssessmentProfileConfig
} from "@/lib/assessment-engine";
import {
  getDevAttempt,
  markDevAttemptSubmitted,
  saveDevOutcomes,
  type DevOutcomeRecord
} from "@/lib/assessment-dev-store";
import { createSupabaseClient, createSupabaseServiceClient, resolveUserId } from "@/lib/supabase";

export const runtime = "nodejs";

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

function parsePracticeTrack(value: unknown, subject: string): PracticeTrack {
  if (value === "computer_science" || value === "biology" || value === "general") {
    return value;
  }
  return inferTrackFromSubject(subject);
}

function coerceQuestionTypes(values: unknown): QuestionType[] {
  if (!Array.isArray(values)) {
    return [];
  }

  return values.filter(
    (value): value is QuestionType =>
      value === "mcq" || value === "short_answer" || value === "open_ended" || value === "code"
  );
}

function parseStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((entry): entry is string => typeof entry === "string");
}

type DbAttemptRow = {
  id: string;
  user_id: string;
  lesson_id: string;
  class_name: string;
  subject: string;
  exam_name: string | null;
  practice_track: PracticeTrack;
  status: "in_progress" | "submitted";
  config_snapshot: Record<string, unknown> | null;
};

function resolveProfileConfig(snapshot: Record<string, unknown> | null): Partial<AssessmentProfileConfig> {
  if (!snapshot) {
    return {};
  }

  return {
    examStyle: typeof snapshot.exam_style === "string" ? snapshot.exam_style : undefined,
    durationSeconds: typeof snapshot.duration_seconds === "number" ? snapshot.duration_seconds : undefined,
    autosaveEnabled: typeof snapshot.autosave_enabled === "boolean" ? snapshot.autosave_enabled : undefined,
    resumeEnabled: typeof snapshot.resume_enabled === "boolean" ? snapshot.resume_enabled : undefined,
    sectionTimeLimits: {}
  };
}

function applySnapshotFilters(args: {
  definition: ReturnType<typeof buildAssessmentDefinition>;
  configSnapshot: Record<string, unknown> | null;
}): {
  questions: ReturnType<typeof buildAssessmentDefinition>["questions"];
  internalQuestions: ReturnType<typeof buildAssessmentDefinition>["internalQuestions"];
  sections: AssessmentSection[];
} {
  const allowedTypes = coerceQuestionTypes(args.configSnapshot?.allowed_question_types);
  const questionIds = parseStringArray(args.configSnapshot?.question_ids);
  const questionTypeOrder = coerceQuestionTypes(args.configSnapshot?.question_type_order);

  let internalQuestions =
    allowedTypes.length > 0
      ? args.definition.internalQuestions.filter((question) => allowedTypes.includes(question.type))
      : [...args.definition.internalQuestions];

  if (questionIds.length > 0) {
    const questionIdSet = new Set(questionIds);
    internalQuestions = internalQuestions.filter((question) => questionIdSet.has(question.id));
  }

  if (questionTypeOrder.length > 0) {
    const typeOrder = new Map<string, number>();
    questionTypeOrder.forEach((entry, index) => {
      typeOrder.set(entry, index);
    });

    internalQuestions = [...internalQuestions].sort((a, b) => {
      const aIndex = typeOrder.get(a.type) ?? Number.MAX_SAFE_INTEGER;
      const bIndex = typeOrder.get(b.type) ?? Number.MAX_SAFE_INTEGER;
      return aIndex - bIndex;
    });
  }

  const publicById = new Map(args.definition.questions.map((question) => [question.id, question]));
  const questions = internalQuestions
    .map((question) => publicById.get(question.id))
    .filter((question): question is ReturnType<typeof buildAssessmentDefinition>["questions"][number] =>
      Boolean(question)
    );

  const activeTypes = new Set(internalQuestions.map((question) => question.type));
  const sections = args.definition.sections.filter((section) =>
    section.question_types.some((type: QuestionType) => activeTypes.has(type))
  );

  return {
    questions,
    internalQuestions,
    sections
  };
}

function deriveFocusAreas(reviewedItems: ReviewedAssessmentItem[]): string[] {
  return reviewedItems.filter((item) => !item.is_correct).map((item) => item.prompt).slice(0, 4);
}

function toDevOutcomes(
  attemptId: string,
  completedAt: string,
  outcomes: ReturnType<typeof scoreAssessmentSubmission>["outcomes"]
): DevOutcomeRecord[] {
  return outcomes.map((outcome) => ({
    attempt_id: attemptId,
    question_id: outcome.question_id,
    question_type: outcome.question_type,
    competency_tags: outcome.competency_tags,
    is_correct: outcome.is_correct,
    earned_score: outcome.earned_score,
    max_score: outcome.max_score,
    manual_review_required: outcome.manual_review_required,
    feedback: outcome.feedback,
    response_payload: outcome.response_payload,
    expected_payload: outcome.expected_payload,
    created_at: completedAt
  }));
}

export async function POST(request: Request) {
  const accessToken = getBearerToken(request.headers.get("authorization"));
  const devUserId = request.headers.get("x-dev-user-id");
  const resolvedUser = await resolveUserId(accessToken, devUserId);

  if ("error" in resolvedUser) {
    return NextResponse.json({ error: resolvedUser.error }, { status: resolvedUser.status });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const parsed = assessmentSubmitRequestSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      {
        error: "Invalid assessment submit payload",
        details: parsed.error.issues
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

  let attempt: DbAttemptRow | null = null;
  const { data: attemptData, error: attemptError } = await supabase
    .from("assessment_attempts")
    .select("id, user_id, lesson_id, class_name, subject, exam_name, practice_track, status, config_snapshot")
    .eq("id", parsed.data.attempt_id)
    .eq("user_id", resolvedUser.userId)
    .maybeSingle();

  if (attemptError) {
    if (process.env.NODE_ENV !== "production" && isMissingAssessmentSchema(attemptError.message)) {
      const devAttempt = await getDevAttempt(parsed.data.attempt_id);
      if (!devAttempt || devAttempt.user_id !== resolvedUser.userId) {
        return NextResponse.json({ error: "Attempt not found" }, { status: 404 });
      }

      attempt = {
        id: devAttempt.id,
        user_id: devAttempt.user_id,
        lesson_id: devAttempt.lesson_id,
        class_name: devAttempt.class_name,
        subject: devAttempt.subject,
        exam_name: devAttempt.exam_name,
        practice_track: devAttempt.practice_track,
        status: devAttempt.status,
        config_snapshot: devAttempt.config_snapshot
      };
    } else {
      return NextResponse.json({ error: attemptError.message }, { status: 500 });
    }
  } else {
    attempt = (attemptData as DbAttemptRow | null) ?? null;
  }

  if (!attempt) {
    return NextResponse.json({ error: "Attempt not found" }, { status: 404 });
  }

  if (attempt.status === "submitted") {
    return NextResponse.json({ error: "Attempt already submitted" }, { status: 409 });
  }

  const practiceTrack = parsePracticeTrack(attempt.practice_track, attempt.subject);
  const definition = buildAssessmentDefinition(practiceTrack, resolveProfileConfig(attempt.config_snapshot));
  const filtered = applySnapshotFilters({ definition, configSnapshot: attempt.config_snapshot });

  const scoreResult = scoreAssessmentSubmission({
    definition: {
      ...definition,
      questions: filtered.questions,
      internalQuestions: filtered.internalQuestions,
      sections: filtered.sections
    },
    responses: parsed.data.responses
  });

  const completedAt = new Date().toISOString();

  const responsePayload: AssessmentSubmitResponse = {
    attempt_id: attempt.id,
    completed_at: completedAt,
    score: {
      correct: scoreResult.correctCount,
      total: scoreResult.totalCount,
      percentage: scoreResult.percentage
    },
    section_scores: scoreResult.sectionScores,
    reviewed_items: scoreResult.reviewedItems,
    needs_review: scoreResult.needsReview,
    focus_areas: deriveFocusAreas(scoreResult.reviewedItems),
    recommendations: scoreResult.recommendations
  };

  const scoreSnapshot = {
    correct: scoreResult.correctCount,
    total: scoreResult.totalCount,
    percentage: scoreResult.percentage,
    needs_review: scoreResult.needsReview,
    focus_areas: responsePayload.focus_areas,
    section_scores: responsePayload.section_scores,
    recommendations: responsePayload.recommendations
  };

  const outcomeRows = scoreResult.outcomes.map((outcome) => ({
    attempt_id: attempt.id,
    user_id: attempt.user_id,
    question_id: outcome.question_id,
    question_type: outcome.question_type,
    competency_tags: outcome.competency_tags,
    is_correct: outcome.is_correct,
    earned_score: outcome.earned_score,
    max_score: outcome.max_score,
    manual_review_required: outcome.manual_review_required,
    feedback: outcome.feedback,
    response_payload: outcome.response_payload,
    expected_payload: outcome.expected_payload,
    created_at: completedAt
  }));

  const updateResult = await supabase
    .from("assessment_attempts")
    .update({
      status: "submitted",
      submitted_at: completedAt,
      score_snapshot: scoreSnapshot
    })
    .eq("id", attempt.id)
    .eq("user_id", attempt.user_id);

  if (updateResult.error) {
    if (process.env.NODE_ENV !== "production" && isMissingAssessmentSchema(updateResult.error.message)) {
      await markDevAttemptSubmitted({
        attemptId: attempt.id,
        scoreSnapshot,
        submittedAt: completedAt
      });
      await saveDevOutcomes(attempt.id, toDevOutcomes(attempt.id, completedAt, scoreResult.outcomes));
      return NextResponse.json(responsePayload, { status: 200 });
    }

    return NextResponse.json({ error: updateResult.error.message }, { status: 500 });
  }

  const { error: deleteError } = await supabase
    .from("assessment_outcomes")
    .delete()
    .eq("attempt_id", attempt.id)
    .eq("user_id", attempt.user_id);

  if (deleteError && !isMissingAssessmentSchema(deleteError.message)) {
    return NextResponse.json({ error: deleteError.message }, { status: 500 });
  }

  const { error: insertOutcomeError } = await supabase.from("assessment_outcomes").insert(outcomeRows);

  if (insertOutcomeError) {
    if (process.env.NODE_ENV !== "production" && isMissingAssessmentSchema(insertOutcomeError.message)) {
      await markDevAttemptSubmitted({
        attemptId: attempt.id,
        scoreSnapshot,
        submittedAt: completedAt
      });
      await saveDevOutcomes(attempt.id, toDevOutcomes(attempt.id, completedAt, scoreResult.outcomes));
      return NextResponse.json(responsePayload, { status: 200 });
    }

    return NextResponse.json({ error: insertOutcomeError.message }, { status: 500 });
  }

  return NextResponse.json(responsePayload, { status: 200 });
}
