import "server-only";

import { promises as fs } from "node:fs";
import path from "node:path";

const DEV_ASSESSMENT_STORE_PATH = path.join(process.cwd(), "scratch", "assessment_attempts.dev.json");

export type DevAttemptRecord = {
  id: string;
  user_id: string;
  lesson_id: string;
  class_name: string;
  subject: string;
  exam_name: string | null;
  practice_track: "computer_science" | "biology" | "general";
  status: "in_progress" | "submitted";
  config_snapshot: Record<string, unknown>;
  score_snapshot?: Record<string, unknown>;
  started_at: string;
  submitted_at?: string;
};

export type DevOutcomeRecord = {
  attempt_id: string;
  question_id: string;
  question_type: string;
  competency_tags: string[];
  is_correct: boolean;
  earned_score: number;
  max_score: number;
  manual_review_required: boolean;
  feedback: string;
  response_payload: Record<string, unknown>;
  expected_payload: Record<string, unknown>;
  created_at: string;
};

type DevAssessmentStore = {
  attempts: Record<string, DevAttemptRecord>;
  outcomes: Record<string, DevOutcomeRecord[]>;
};

function createEmptyStore(): DevAssessmentStore {
  return { attempts: {}, outcomes: {} };
}

export async function readDevAssessmentStore(): Promise<DevAssessmentStore> {
  try {
    const raw = await fs.readFile(DEV_ASSESSMENT_STORE_PATH, "utf8");
    const parsed = JSON.parse(raw) as Partial<DevAssessmentStore>;

    return {
      attempts: parsed.attempts && typeof parsed.attempts === "object" ? parsed.attempts : {},
      outcomes: parsed.outcomes && typeof parsed.outcomes === "object" ? parsed.outcomes : {}
    };
  } catch (error) {
    const code = (error as NodeJS.ErrnoException).code;
    if (code === "ENOENT") {
      return createEmptyStore();
    }
    throw error;
  }
}

export async function writeDevAssessmentStore(store: DevAssessmentStore): Promise<void> {
  await fs.mkdir(path.dirname(DEV_ASSESSMENT_STORE_PATH), { recursive: true });
  await fs.writeFile(DEV_ASSESSMENT_STORE_PATH, JSON.stringify(store, null, 2), "utf8");
}

export async function saveDevAttempt(record: DevAttemptRecord): Promise<void> {
  const store = await readDevAssessmentStore();
  store.attempts[record.id] = record;
  await writeDevAssessmentStore(store);
}

export async function getDevAttempt(attemptId: string): Promise<DevAttemptRecord | null> {
  const store = await readDevAssessmentStore();
  return store.attempts[attemptId] ?? null;
}

export async function saveDevOutcomes(attemptId: string, outcomes: DevOutcomeRecord[]): Promise<void> {
  const store = await readDevAssessmentStore();
  store.outcomes[attemptId] = outcomes;
  await writeDevAssessmentStore(store);
}

export async function markDevAttemptSubmitted(args: {
  attemptId: string;
  scoreSnapshot: Record<string, unknown>;
  submittedAt: string;
}): Promise<void> {
  const store = await readDevAssessmentStore();
  const current = store.attempts[args.attemptId];
  if (!current) {
    return;
  }

  store.attempts[args.attemptId] = {
    ...current,
    status: "submitted",
    score_snapshot: args.scoreSnapshot,
    submitted_at: args.submittedAt
  };

  await writeDevAssessmentStore(store);
}
