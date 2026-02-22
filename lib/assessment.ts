export type PracticeTrack = "computer_science" | "biology" | "general";
export type QuestionType = "mcq" | "short_answer" | "open_ended" | "code";
export type CodeLanguage = "javascript" | "python";

export type McqQuestion = {
  id: string;
  type: "mcq";
  prompt: string;
  choices: [string, string, string, string];
  competency_tags: string[];
};

export type ShortAnswerQuestion = {
  id: string;
  type: "short_answer";
  prompt: string;
  min_words?: number;
  competency_tags: string[];
  manual_review_mode?: boolean;
};

export type OpenEndedQuestion = {
  id: string;
  type: "open_ended";
  prompt: string;
  min_words?: number;
  competency_tags: string[];
  manual_review_mode?: boolean;
};

export type CodeQuestion = {
  id: string;
  type: "code";
  title: string;
  prompt: string;
  function_name: string;
  starter_code: string;
  default_language: CodeLanguage;
  allowed_languages: CodeLanguage[];
  visible_tests: Array<{ label: string; input: number[]; expected: number }>;
  competency_tags: string[];
};

export type AssessmentQuestion = McqQuestion | ShortAnswerQuestion | OpenEndedQuestion | CodeQuestion;

export type AssessmentSection = {
  id: string;
  title: string;
  question_types: QuestionType[];
  time_limit_seconds: number | null;
};

export type AssessmentStartRequest = {
  lesson_id?: string;
  class_name?: string;
  subject?: string;
  exam_name?: string;
  track_override?: PracticeTrack;
};

export type AssessmentStartResponse = {
  attempt_id: string;
  lesson_id: string;
  class_name: string;
  subject: string;
  exam_name: string | null;
  practice_track: PracticeTrack;
  exam_style: string;
  autosave_enabled: boolean;
  resume_enabled: boolean;
  duration_seconds: number;
  started_at: string;
  sections: AssessmentSection[];
  questions: AssessmentQuestion[];
};

export type McqResponse = {
  question_id: string;
  question_type: "mcq";
  selected_index: number;
};

export type WrittenResponse = {
  question_id: string;
  question_type: "short_answer" | "open_ended";
  text_response: string;
};

export type CodeResponse = {
  question_id: string;
  question_type: "code";
  code_submission: string;
  language?: CodeLanguage;
};

export type AssessmentResponseItem = McqResponse | WrittenResponse | CodeResponse;

export type AssessmentSubmitRequest = {
  attempt_id: string;
  responses: AssessmentResponseItem[];
};

export type ReviewedAssessmentItem = {
  id: string;
  question_type: QuestionType;
  prompt: string;
  user_response: string;
  expected: string;
  is_correct: boolean;
  explanation: string;
  competency_tags: string[];
  manual_review_required?: boolean;
};

export type AssessmentSectionScore = {
  label: string;
  correct: number;
  total: number;
};

export type AssessmentSubmitResponse = {
  attempt_id: string;
  completed_at: string;
  score: {
    correct: number;
    total: number;
    percentage: number;
  };
  section_scores: AssessmentSectionScore[];
  reviewed_items: ReviewedAssessmentItem[];
  needs_review: boolean;
  focus_areas: string[];
  recommendations: string[];
};

type Issue = {
  path: string;
  message: string;
};

type ParseFailure = {
  success: false;
  error: {
    issues: Issue[];
  };
};

type ParseSuccess<T> = {
  success: true;
  data: T;
};

type ParseResult<T> = ParseFailure | ParseSuccess<T>;

function parseFailure(issues: Issue[]): ParseFailure {
  return { success: false, error: { issues } };
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isPracticeTrack(value: unknown): value is PracticeTrack {
  return value === "computer_science" || value === "biology" || value === "general";
}

function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}

function isCodeLanguage(value: unknown): value is CodeLanguage {
  return value === "javascript" || value === "python";
}

export const assessmentStartRequestSchema = {
  safeParse(value: unknown): ParseResult<AssessmentStartRequest> {
    if (!isPlainObject(value)) {
      return parseFailure([{ path: "", message: "Expected object" }]);
    }

    const issues: Issue[] = [];
    const data: AssessmentStartRequest = {};

    const stringField = (key: keyof AssessmentStartRequest, maxLength: number) => {
      const raw = value[key];
      if (raw === undefined) {
        return;
      }
      if (typeof raw !== "string") {
        issues.push({ path: String(key), message: "Expected string" });
        return;
      }
      const trimmed = raw.trim();
      if (trimmed.length === 0) {
        issues.push({ path: String(key), message: "Cannot be empty" });
        return;
      }
      if (trimmed.length > maxLength) {
        issues.push({ path: String(key), message: `Must be at most ${maxLength} characters` });
        return;
      }
      data[key] = trimmed as never;
    };

    stringField("lesson_id", 120);
    stringField("class_name", 120);
    stringField("subject", 80);
    stringField("exam_name", 80);

    const track = value.track_override;
    if (track !== undefined) {
      if (!isPracticeTrack(track)) {
        issues.push({ path: "track_override", message: "Invalid track" });
      } else {
        data.track_override = track;
      }
    }

    if (issues.length > 0) {
      return parseFailure(issues);
    }

    return {
      success: true,
      data
    };
  }
};

function parseResponseItem(value: unknown, index: number): { data?: AssessmentResponseItem; issues: Issue[] } {
  if (!isPlainObject(value)) {
    return {
      issues: [{ path: `responses[${index}]`, message: "Expected object" }]
    };
  }

  const questionId = value.question_id;
  const questionType = value.question_type;

  if (typeof questionId !== "string" || questionId.trim().length === 0) {
    return {
      issues: [{ path: `responses[${index}].question_id`, message: "Expected non-empty string" }]
    };
  }

  if (questionType === "mcq") {
    if (typeof value.selected_index !== "number" || !Number.isInteger(value.selected_index)) {
      return {
        issues: [{ path: `responses[${index}].selected_index`, message: "Expected integer" }]
      };
    }

    if (value.selected_index < 0 || value.selected_index > 3) {
      return {
        issues: [{ path: `responses[${index}].selected_index`, message: "Expected value from 0 to 3" }]
      };
    }

    return {
      data: {
        question_id: questionId,
        question_type: "mcq",
        selected_index: value.selected_index
      },
      issues: []
    };
  }

  if (questionType === "short_answer" || questionType === "open_ended") {
    if (typeof value.text_response !== "string") {
      return {
        issues: [{ path: `responses[${index}].text_response`, message: "Expected string" }]
      };
    }

    return {
      data: {
        question_id: questionId,
        question_type: questionType,
        text_response: value.text_response
      },
      issues: []
    };
  }

  if (questionType === "code") {
    if (typeof value.code_submission !== "string") {
      return {
        issues: [{ path: `responses[${index}].code_submission`, message: "Expected string" }]
      };
    }

    if (value.language !== undefined && !isCodeLanguage(value.language)) {
      return {
        issues: [{ path: `responses[${index}].language`, message: "Invalid language" }]
      };
    }

    return {
      data: {
        question_id: questionId,
        question_type: "code",
        code_submission: value.code_submission,
        language: value.language
      },
      issues: []
    };
  }

  return {
    issues: [{ path: `responses[${index}].question_type`, message: "Unsupported question type" }]
  };
}

export const assessmentSubmitRequestSchema = {
  safeParse(value: unknown): ParseResult<AssessmentSubmitRequest> {
    if (!isPlainObject(value)) {
      return parseFailure([{ path: "", message: "Expected object" }]);
    }

    const issues: Issue[] = [];

    const attemptId = value.attempt_id;
    const normalizedAttemptId = typeof attemptId === "string" ? attemptId : "";
    if (!normalizedAttemptId || !isUuid(normalizedAttemptId)) {
      issues.push({ path: "attempt_id", message: "Expected UUID string" });
    }

    if (!Array.isArray(value.responses)) {
      issues.push({ path: "responses", message: "Expected array" });
      return parseFailure(issues);
    }

    if (value.responses.length > 64) {
      issues.push({ path: "responses", message: "Too many responses" });
    }

    const responses: AssessmentResponseItem[] = [];
    for (let index = 0; index < value.responses.length; index += 1) {
      const parsed = parseResponseItem(value.responses[index], index);
      issues.push(...parsed.issues);
      if (parsed.data) {
        responses.push(parsed.data);
      }
    }

    if (issues.length > 0) {
      return parseFailure(issues);
    }

    return {
      success: true,
      data: {
        attempt_id: normalizedAttemptId,
        responses
      }
    };
  }
};
