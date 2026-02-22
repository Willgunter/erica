import { spawnSync } from "node:child_process";
import vm from "node:vm";
import type {
  AssessmentQuestion,
  AssessmentResponseItem,
  AssessmentSection,
  CodeLanguage,
  PracticeTrack,
  QuestionType,
  ReviewedAssessmentItem
} from "@/lib/assessment";

const MAX_CODE_PAYLOAD_BYTES = 12_000;
const JS_TIMEOUT_MS = 250;
const PY_TIMEOUT_MS = 1_500;

type McqQuestionInternal = {
  id: string;
  type: "mcq";
  prompt: string;
  choices: [string, string, string, string];
  correctIndex: number;
  explanation: string;
  competencyTags: string[];
};

type WrittenQuestionInternal = {
  id: string;
  type: "short_answer" | "open_ended";
  prompt: string;
  rubricKeywords: string[];
  explanation: string;
  minWords: number;
  competencyTags: string[];
  manualReviewMode: boolean;
};

type CodeTestCase = {
  label: string;
  input: number[];
  expected: number;
  visibility: "visible" | "hidden";
};

type CodeQuestionInternal = {
  id: string;
  type: "code";
  title: string;
  prompt: string;
  functionName: string;
  starterCode: string;
  defaultLanguage: CodeLanguage;
  allowedLanguages: CodeLanguage[];
  testCases: CodeTestCase[];
  explanation: string;
  competencyTags: string[];
};

type AssessmentQuestionInternal = McqQuestionInternal | WrittenQuestionInternal | CodeQuestionInternal;

export type AssessmentProfileConfig = {
  examStyle: string;
  durationSeconds: number;
  autosaveEnabled: boolean;
  resumeEnabled: boolean;
  sectionTimeLimits: Record<string, number | null>;
};

export type AssessmentDefinition = {
  practiceTrack: PracticeTrack;
  examStyle: string;
  durationSeconds: number;
  autosaveEnabled: boolean;
  resumeEnabled: boolean;
  sections: AssessmentSection[];
  questions: AssessmentQuestion[];
  internalQuestions: AssessmentQuestionInternal[];
};

export type QuestionOutcomeRecord = {
  question_id: string;
  question_type: QuestionType;
  competency_tags: string[];
  is_correct: boolean;
  earned_score: number;
  max_score: number;
  manual_review_required: boolean;
  feedback: string;
  response_payload: Record<string, unknown>;
  expected_payload: Record<string, unknown>;
};

const CS_MCQ_QUESTIONS: McqQuestionInternal[] = [
  {
    id: "cs-q1",
    type: "mcq",
    prompt: "What is the main benefit of using a hash map for lookups?",
    choices: ["Lower memory usage", "Average O(1) key lookup", "Guaranteed sorted keys", "No collisions ever"],
    correctIndex: 1,
    explanation: "Hash maps trade ordering for fast average key lookup.",
    competencyTags: ["data_structures", "complexity"]
  },
  {
    id: "cs-q2",
    type: "mcq",
    prompt: "Which data structure best represents call stack behavior?",
    choices: ["Queue", "Heap", "Stack", "Graph"],
    correctIndex: 2,
    explanation: "Function calls push/pop in LIFO order, which is stack behavior.",
    competencyTags: ["data_structures"]
  },
  {
    id: "cs-q3",
    type: "mcq",
    prompt: "What does Big-O describe?",
    choices: [
      "Exact runtime in milliseconds",
      "Memory address offsets",
      "Asymptotic growth as input size increases",
      "CPU architecture details"
    ],
    correctIndex: 2,
    explanation: "Big-O captures growth trend, not exact wall-clock time.",
    competencyTags: ["complexity"]
  },
  {
    id: "cs-q4",
    type: "mcq",
    prompt: "Why are unit tests useful in coding exams and interviews?",
    choices: [
      "They replace algorithmic thinking",
      "They provide immediate correctness checks against cases",
      "They always optimize runtime",
      "They make code shorter by default"
    ],
    correctIndex: 1,
    explanation: "Tests validate behavior quickly and catch edge-case failures.",
    competencyTags: ["testing"]
  },
  {
    id: "cs-q5",
    type: "mcq",
    prompt: "Which technique improves confidence before submission?",
    choices: [
      "Skip edge cases",
      "Only test with one trivial input",
      "Dry-run and validate boundary inputs",
      "Rename variables repeatedly"
    ],
    correctIndex: 2,
    explanation: "Boundary and edge-case checks reduce hidden failures.",
    competencyTags: ["debugging", "testing"]
  },
  {
    id: "cs-q6",
    type: "mcq",
    prompt: "If a loop runs over `n` items once, its time complexity is usually:",
    choices: ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
    correctIndex: 2,
    explanation: "Single linear pass over n items is O(n).",
    competencyTags: ["complexity"]
  },
  {
    id: "cs-q7",
    type: "mcq",
    prompt: "What is a common use case for recursion?",
    choices: [
      "Only for string concatenation",
      "Problems with repeating self-similar substructure",
      "Avoiding all base cases",
      "Replacing arrays entirely"
    ],
    correctIndex: 1,
    explanation: "Recursion fits naturally when smaller subproblems mirror the whole.",
    competencyTags: ["algorithms"]
  },
  {
    id: "cs-q8",
    type: "mcq",
    prompt: "A failing hidden test usually suggests:",
    choices: [
      "The prompt is wrong",
      "There is likely an uncovered edge case",
      "The solution is too short",
      "The code used too many comments"
    ],
    correctIndex: 1,
    explanation: "Hidden failures are commonly edge-case or assumption issues.",
    competencyTags: ["debugging", "testing"]
  },
  {
    id: "cs-q9",
    type: "mcq",
    prompt: "In exam settings, why mimic the actual coding interface during practice?",
    choices: [
      "To avoid learning concepts",
      "To build familiarity with the real constraints and flow",
      "To reduce test variety",
      "To prevent writing any code"
    ],
    correctIndex: 1,
    explanation: "Format familiarity reduces friction and improves execution under pressure.",
    competencyTags: ["exam_strategy"]
  }
];

const CS_CODE_QUESTIONS: CodeQuestionInternal[] = [
  {
    id: "cs-coding-1",
    type: "code",
    title: "Coding prompt",
    prompt:
      "Implement `sumEven(numbers)` that returns the sum of all even integers in an array. Ignore odd values.",
    functionName: "sumEven",
    starterCode: "function sumEven(numbers) {\n  // TODO: return the sum of even integers\n  return 0;\n}",
    defaultLanguage: "javascript",
    allowedLanguages: ["javascript", "python"],
    testCases: [
      { label: "basic mix", input: [1, 2, 3, 4], expected: 6, visibility: "visible" },
      { label: "all even", input: [2, 2, 2], expected: 6, visibility: "visible" },
      { label: "no evens", input: [1, 3, 5], expected: 0, visibility: "visible" },
      { label: "includes negative values", input: [-2, 5, 8], expected: 6, visibility: "hidden" }
    ],
    explanation: "Strong solutions handle mixed signs and odd values without mutating input.",
    competencyTags: ["algorithms", "implementation", "testing"]
  },
  {
    id: "cs-coding-2",
    type: "code",
    title: "Coding prompt",
    prompt:
      "Implement `maxValue(numbers)` that returns the largest number in an array. Return `Number.NEGATIVE_INFINITY` for an empty array.",
    functionName: "maxValue",
    starterCode:
      "function maxValue(numbers) {\n  // TODO: return the maximum value in the array\n  return Number.NEGATIVE_INFINITY;\n}",
    defaultLanguage: "javascript",
    allowedLanguages: ["javascript", "python"],
    testCases: [
      { label: "mixed values", input: [10, -3, 4, 99, 2], expected: 99, visibility: "visible" },
      { label: "negative-only values", input: [-10, -5, -7], expected: -5, visibility: "visible" },
      { label: "single value", input: [4], expected: 4, visibility: "visible" },
      { label: "with duplicate max", input: [7, 1, 7, 3], expected: 7, visibility: "hidden" }
    ],
    explanation: "Track the current maximum while iterating once.",
    competencyTags: ["algorithms", "implementation"]
  },
  {
    id: "cs-coding-3",
    type: "code",
    title: "Coding prompt",
    prompt:
      "Implement `countPositive(numbers)` that returns how many positive integers are in the input array.",
    functionName: "countPositive",
    starterCode:
      "function countPositive(numbers) {\n  // TODO: return the count of values greater than 0\n  return 0;\n}",
    defaultLanguage: "javascript",
    allowedLanguages: ["javascript", "python"],
    testCases: [
      { label: "basic mix", input: [1, -2, 3, 0, -4, 5], expected: 3, visibility: "visible" },
      { label: "no positives", input: [-1, -2, 0, -3], expected: 0, visibility: "visible" },
      { label: "all positives", input: [2, 4, 6], expected: 3, visibility: "visible" },
      { label: "includes zeros", input: [0, 0, 0, 10], expected: 1, visibility: "hidden" }
    ],
    explanation: "Positive counting should include values strictly greater than zero.",
    competencyTags: ["algorithms", "implementation", "testing"]
  }
];

const BIO_MCQ_QUESTIONS: McqQuestionInternal[] = [
  {
    id: "bio-q1",
    type: "mcq",
    prompt: "Where does cellular respiration primarily take place?",
    choices: ["Nucleus", "Mitochondria", "Golgi apparatus", "Ribosome"],
    correctIndex: 1,
    explanation: "Most respiration steps happen in mitochondria.",
    competencyTags: ["cell_biology"]
  },
  {
    id: "bio-q2",
    type: "mcq",
    prompt: "What is the main role of enzymes in biology?",
    choices: [
      "Consume all reactants",
      "Permanently change DNA",
      "Speed up reactions by lowering activation energy",
      "Stop all metabolism"
    ],
    correctIndex: 2,
    explanation: "Enzymes accelerate reactions by reducing activation energy barriers.",
    competencyTags: ["biochemistry"]
  },
  {
    id: "bio-q3",
    type: "mcq",
    prompt: "Which molecule carries genetic instructions?",
    choices: ["ATP", "DNA", "Lipids", "Glucose"],
    correctIndex: 1,
    explanation: "DNA encodes hereditary information.",
    competencyTags: ["genetics"]
  },
  {
    id: "bio-q4",
    type: "mcq",
    prompt: "Photosynthesis directly produces:",
    choices: ["Nitrogen gas", "Glucose and oxygen", "Only water", "Only carbon dioxide"],
    correctIndex: 1,
    explanation: "Photosynthesis uses light to produce glucose and releases oxygen.",
    competencyTags: ["plant_biology"]
  },
  {
    id: "bio-q5",
    type: "mcq",
    prompt: "Homeostasis means an organism:",
    choices: [
      "Never changes",
      "Maintains stable internal conditions",
      "Only responds to sunlight",
      "Stops metabolic activity"
    ],
    correctIndex: 1,
    explanation: "Homeostasis regulates internal balance despite external change.",
    competencyTags: ["physiology"]
  },
  {
    id: "bio-q6",
    type: "mcq",
    prompt: "A mutation is best described as:",
    choices: [
      "Guaranteed harmful trait",
      "Temporary protein shutdown",
      "A change in genetic sequence",
      "Loss of all chromosomes"
    ],
    correctIndex: 2,
    explanation: "Mutations are changes in DNA sequence with varied outcomes.",
    competencyTags: ["genetics"]
  }
];

const BIO_WRITTEN_QUESTIONS: WrittenQuestionInternal[] = [
  {
    id: "bio-w1",
    type: "short_answer",
    prompt: "In 2-3 sentences, explain why ATP is important in cells.",
    rubricKeywords: ["energy", "cell", "process"],
    explanation: "Strong answers mention ATP as an energy carrier used by cell processes.",
    minWords: 12,
    competencyTags: ["cell_biology", "biochemistry"],
    manualReviewMode: false
  },
  {
    id: "bio-w2",
    type: "short_answer",
    prompt: "Briefly describe the relationship between structure and function in proteins.",
    rubricKeywords: ["shape", "function", "amino"],
    explanation: "Good responses connect amino-acid-driven shape to protein function.",
    minWords: 12,
    competencyTags: ["biochemistry"],
    manualReviewMode: false
  },
  {
    id: "bio-w3",
    type: "open_ended",
    prompt: "Open response: compare photosynthesis and cellular respiration, including inputs/outputs and how they relate.",
    rubricKeywords: ["glucose", "oxygen", "carbon dioxide", "energy"],
    explanation: "Expected ideas include complementary flow of energy and matter between both processes.",
    minWords: 28,
    competencyTags: ["cell_biology", "systems_thinking"],
    manualReviewMode: false
  },
  {
    id: "bio-w4",
    type: "open_ended",
    prompt: "Open response: explain how an ecosystem change can affect a food web.",
    rubricKeywords: ["population", "predator", "prey", "balance"],
    explanation: "Strong answers describe cascading effects across multiple trophic levels.",
    minWords: 24,
    competencyTags: ["ecology", "systems_thinking"],
    manualReviewMode: true
  }
];

const GENERAL_MCQ_QUESTIONS: McqQuestionInternal[] = [
  {
    id: "g-q1",
    type: "mcq",
    prompt: "What best describes active recall during studying?",
    choices: [
      "Re-reading notes multiple times",
      "Trying to retrieve ideas from memory before checking notes",
      "Highlighting every key sentence",
      "Watching a lecture at 2x speed"
    ],
    correctIndex: 1,
    explanation: "Active recall means practicing retrieval from memory, not just re-consuming content.",
    competencyTags: ["study_strategy"]
  },
  {
    id: "g-q2",
    type: "mcq",
    prompt: "Which approach is most aligned with spaced repetition?",
    choices: [
      "Studying once right before the test",
      "Reviewing all material only when confused",
      "Revisiting topics at increasing intervals over time",
      "Focusing only on the easiest topics first"
    ],
    correctIndex: 2,
    explanation: "Spaced repetition schedules reviews across time, usually with widening intervals.",
    competencyTags: ["study_strategy"]
  },
  {
    id: "g-q3",
    type: "mcq",
    prompt: "A useful way to check true understanding is to:",
    choices: [
      "Explain the idea in your own words with an example",
      "Copy definitions exactly from notes",
      "Memorize headings only",
      "Skip questions until the end"
    ],
    correctIndex: 0,
    explanation: "Explaining concepts in your own words exposes gaps in reasoning.",
    competencyTags: ["metacognition"]
  },
  {
    id: "g-q4",
    type: "mcq",
    prompt: "If a learner misses a question, the best immediate step is usually to:",
    choices: [
      "Move on and avoid the topic",
      "Retry blindly until lucky",
      "Review why the answer was wrong and attempt a similar question",
      "Change topics permanently"
    ],
    correctIndex: 2,
    explanation: "Error-focused review plus a similar follow-up question improves retention.",
    competencyTags: ["error_correction"]
  },
  {
    id: "g-q5",
    type: "mcq",
    prompt: "What is the main goal of a checkpoint question in a lesson?",
    choices: [
      "To rank students publicly",
      "To test only trivia facts",
      "To diagnose understanding before moving forward",
      "To replace instruction entirely"
    ],
    correctIndex: 2,
    explanation: "Checkpoints are diagnostic and guide next steps in learning.",
    competencyTags: ["assessment_literacy"]
  },
  {
    id: "g-q6",
    type: "mcq",
    prompt: "Which practice most improves transfer to new problems?",
    choices: [
      "Solving only one identical question type",
      "Mixing related problem types and identifying differences",
      "Studying with no feedback",
      "Ignoring conceptual explanations"
    ],
    correctIndex: 1,
    explanation: "Interleaving related problem types supports flexible application.",
    competencyTags: ["transfer_learning"]
  },
  {
    id: "g-q7",
    type: "mcq",
    prompt: "What is the best reason to delay feedback until after a full quiz submission?",
    choices: [
      "To reduce server costs",
      "To keep question order secret",
      "To prevent answer leakage during the same attempt",
      "To make the interface look simpler"
    ],
    correctIndex: 2,
    explanation: "Withheld feedback reduces contamination from earlier items in the same attempt.",
    competencyTags: ["assessment_literacy"]
  },
  {
    id: "g-q8",
    type: "mcq",
    prompt: "A strong learning session should include:",
    choices: [
      "Only passive reading",
      "A cycle of learning, retrieval, and reflection",
      "No breaks, regardless of fatigue",
      "Skipping practice to save time"
    ],
    correctIndex: 1,
    explanation: "The cycle of study, retrieval practice, and reflection drives durable learning.",
    competencyTags: ["study_strategy"]
  },
  {
    id: "g-q9",
    type: "mcq",
    prompt: "When confidence is high but accuracy is low, this usually indicates:",
    choices: [
      "Good calibration",
      "Overconfidence and shallow verification",
      "A perfect study plan",
      "That no more practice is needed"
    ],
    correctIndex: 1,
    explanation: "Miscalibration appears when confidence is not validated by performance.",
    competencyTags: ["metacognition"]
  },
  {
    id: "g-q10",
    type: "mcq",
    prompt: "What is the best next step after finishing a quiz?",
    choices: [
      "Ignore results and start a new topic",
      "Only celebrate correct answers",
      "Review misses, target weak areas, and retest later",
      "Delete prior notes"
    ],
    correctIndex: 2,
    explanation: "Post-quiz review should convert misses into a focused follow-up plan.",
    competencyTags: ["reflection"]
  }
];

function toPublicQuestion(question: AssessmentQuestionInternal): AssessmentQuestion {
  if (question.type === "mcq") {
    return {
      id: question.id,
      type: "mcq",
      prompt: question.prompt,
      choices: question.choices,
      competency_tags: question.competencyTags
    };
  }

  if (question.type === "code") {
    return {
      id: question.id,
      type: "code",
      title: question.title,
      prompt: question.prompt,
      function_name: question.functionName,
      starter_code: question.starterCode,
      default_language: question.defaultLanguage,
      allowed_languages: question.allowedLanguages,
      visible_tests: question.testCases
        .filter((testCase) => testCase.visibility === "visible")
        .map((testCase) => ({
          label: testCase.label,
          input: testCase.input,
          expected: testCase.expected
        })),
      competency_tags: question.competencyTags
    };
  }

  return {
    id: question.id,
    type: question.type,
    prompt: question.prompt,
    min_words: question.minWords,
    competency_tags: question.competencyTags,
    manual_review_mode: question.manualReviewMode
  };
}

function defaultSections(track: PracticeTrack, sectionTimeLimits: Record<string, number | null>): AssessmentSection[] {
  if (track === "computer_science") {
    return [
      {
        id: "section-coding",
        title: "Coding challenge",
        question_types: ["code"],
        time_limit_seconds: sectionTimeLimits.coding ?? 900
      },
      {
        id: "section-mcq",
        title: "Technical multiple choice",
        question_types: ["mcq"],
        time_limit_seconds: sectionTimeLimits.mcq ?? 900
      }
    ];
  }

  if (track === "biology") {
    return [
      {
        id: "section-mcq",
        title: "Concept checks",
        question_types: ["mcq"],
        time_limit_seconds: sectionTimeLimits.mcq ?? 600
      },
      {
        id: "section-written",
        title: "Written responses",
        question_types: ["short_answer", "open_ended"],
        time_limit_seconds: sectionTimeLimits.written ?? 900
      }
    ];
  }

  return [
    {
      id: "section-mcq",
      title: "General checkpoint",
      question_types: ["mcq"],
      time_limit_seconds: sectionTimeLimits.mcq ?? 600
    }
  ];
}

export function inferTrackFromSubject(subject: string | null | undefined): PracticeTrack {
  const normalized = (subject ?? "").toLowerCase();

  const csSignals = ["computer science", "cs", "programming", "coding", "algorithm", "data structure"];
  if (csSignals.some((signal) => normalized.includes(signal))) {
    return "computer_science";
  }

  const bioSignals = ["biology", "biochemistry", "cell", "genetics", "ecology", "respiration"];
  if (bioSignals.some((signal) => normalized.includes(signal))) {
    return "biology";
  }

  return "general";
}

export function buildAssessmentDefinition(
  practiceTrack: PracticeTrack,
  profileConfig?: Partial<AssessmentProfileConfig>,
  internalQuestionOverrides?: AssessmentDefinition["internalQuestions"]
): AssessmentDefinition {
  const baseProfile: AssessmentProfileConfig =
    practiceTrack === "computer_science"
      ? {
          examStyle: "Coding challenge + technical multiple choice",
          durationSeconds: 1_800,
          autosaveEnabled: true,
          resumeEnabled: true,
          sectionTimeLimits: { coding: 900, mcq: 900 }
        }
      : practiceTrack === "biology"
        ? {
            examStyle: "Multiple choice + short answer + open response",
            durationSeconds: 1_500,
            autosaveEnabled: true,
            resumeEnabled: true,
            sectionTimeLimits: { mcq: 600, written: 900 }
          }
        : {
            examStyle: "Multiple choice",
            durationSeconds: 1_200,
            autosaveEnabled: true,
            resumeEnabled: true,
            sectionTimeLimits: { mcq: 1_200 }
          };

  const mergedProfile: AssessmentProfileConfig = {
    examStyle: profileConfig?.examStyle ?? baseProfile.examStyle,
    durationSeconds: profileConfig?.durationSeconds ?? baseProfile.durationSeconds,
    autosaveEnabled: profileConfig?.autosaveEnabled ?? baseProfile.autosaveEnabled,
    resumeEnabled: profileConfig?.resumeEnabled ?? baseProfile.resumeEnabled,
    sectionTimeLimits: {
      ...baseProfile.sectionTimeLimits,
      ...(profileConfig?.sectionTimeLimits ?? {})
    }
  };

  const internalQuestions: AssessmentQuestionInternal[] =
    Array.isArray(internalQuestionOverrides) && internalQuestionOverrides.length > 0
      ? [...internalQuestionOverrides]
      : practiceTrack === "computer_science"
        ? [...CS_MCQ_QUESTIONS, ...CS_CODE_QUESTIONS]
        : practiceTrack === "biology"
          ? [...BIO_MCQ_QUESTIONS, ...BIO_WRITTEN_QUESTIONS]
          : [...GENERAL_MCQ_QUESTIONS];

  return {
    practiceTrack,
    examStyle: mergedProfile.examStyle,
    durationSeconds: mergedProfile.durationSeconds,
    autosaveEnabled: mergedProfile.autosaveEnabled,
    resumeEnabled: mergedProfile.resumeEnabled,
    sections: defaultSections(practiceTrack, mergedProfile.sectionTimeLimits),
    questions: internalQuestions.map((question) => toPublicQuestion(question)),
    internalQuestions
  };
}

function normalizeKeywordText(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9\s]/g, " ");
}

function evaluateWrittenAnswer(answer: string, rubricKeywords: string[]): { isCorrect: boolean; expected: string } {
  const normalized = normalizeKeywordText(answer);
  const hitCount = rubricKeywords.filter((keyword) => normalized.includes(keyword.toLowerCase())).length;
  const threshold = Math.max(1, Math.ceil(rubricKeywords.length / 2));

  return {
    isCorrect: hitCount >= threshold,
    expected: `Include core ideas like: ${rubricKeywords.join(", ")}`
  };
}

type CodeEvaluationResult = {
  passedCount: number;
  totalCount: number;
  details: Array<{ label: string; passed: boolean; message: string }>;
  manualReviewRequired: boolean;
};

function evaluateJavascriptSubmission(
  submission: string,
  question: CodeQuestionInternal
): CodeEvaluationResult {
  if (Buffer.byteLength(submission, "utf8") > MAX_CODE_PAYLOAD_BYTES) {
    return {
      passedCount: 0,
      totalCount: question.testCases.length,
      details: [
        {
          label: "payload",
          passed: false,
          message: `Submission exceeds max payload of ${MAX_CODE_PAYLOAD_BYTES} bytes.`
        }
      ],
      manualReviewRequired: false
    };
  }

  const context = vm.createContext({});

  try {
    new vm.Script(submission).runInContext(context, { timeout: JS_TIMEOUT_MS });
  } catch (error) {
    return {
      passedCount: 0,
      totalCount: question.testCases.length,
      details: [
        {
          label: "compile",
          passed: false,
          message: `Code did not compile: ${(error as Error).message}`
        }
      ],
      manualReviewRequired: false
    };
  }

  let hasFunction = false;
  try {
    const checkScript = new vm.Script(`typeof ${question.functionName} === \"function\"`);
    const checkResult = checkScript.runInContext(context, { timeout: JS_TIMEOUT_MS });
    hasFunction = Boolean(checkResult);
  } catch {
    hasFunction = false;
  }

  if (!hasFunction) {
    return {
      passedCount: 0,
      totalCount: question.testCases.length,
      details: [
        {
          label: "function export",
          passed: false,
          message: `Could not find function ${question.functionName}(...) in submission.`
        }
      ],
      manualReviewRequired: false
    };
  }

  let passedCount = 0;
  const details: Array<{ label: string; passed: boolean; message: string }> = [];

  for (const testCase of question.testCases) {
    try {
      const invokeScript = new vm.Script(`${question.functionName}(${JSON.stringify(testCase.input)})`);
      const output = invokeScript.runInContext(context, { timeout: JS_TIMEOUT_MS }) as unknown;
      const passed = output === testCase.expected;

      if (passed) {
        passedCount += 1;
      }

      if (testCase.visibility === "visible" || !passed) {
        details.push({
          label: testCase.label,
          passed,
          message: passed
            ? `Passed (${String(output)})`
            : testCase.visibility === "hidden"
              ? "Hidden test failed."
              : `Expected ${testCase.expected}, got ${String(output)}`
        });
      }
    } catch (error) {
      details.push({
        label: testCase.label,
        passed: false,
        message:
          testCase.visibility === "hidden"
            ? "Hidden test failed with runtime error."
            : `Runtime error: ${(error as Error).message}`
      });
    }
  }

  return {
    passedCount,
    totalCount: question.testCases.length,
    details,
    manualReviewRequired: false
  };
}

function evaluatePythonSubmission(submission: string, question: CodeQuestionInternal): CodeEvaluationResult {
  if (Buffer.byteLength(submission, "utf8") > MAX_CODE_PAYLOAD_BYTES) {
    return {
      passedCount: 0,
      totalCount: question.testCases.length,
      details: [
        {
          label: "payload",
          passed: false,
          message: `Submission exceeds max payload of ${MAX_CODE_PAYLOAD_BYTES} bytes.`
        }
      ],
      manualReviewRequired: false
    };
  }

  const testsPayload = JSON.stringify(
    question.testCases.map((testCase) => ({
      label: testCase.label,
      input: testCase.input,
      expected: testCase.expected,
      visibility: testCase.visibility
    }))
  );

  const harness = `
import json

result = {"compile_error": None, "results": [], "passed_count": 0, "total_count": 0}
submission = ${JSON.stringify(submission)}
function_name = ${JSON.stringify(question.functionName)}
tests = json.loads(${JSON.stringify(testsPayload)})

globals_dict = {}
try:
    exec(submission, globals_dict)
except Exception as exc:
    result["compile_error"] = str(exc)
    print(json.dumps(result))
    raise SystemExit(0)

candidate = globals_dict.get(function_name)
if not callable(candidate):
    result["compile_error"] = f"Could not find function {function_name}(...) in submission."
    print(json.dumps(result))
    raise SystemExit(0)

for test in tests:
    result["total_count"] += 1
    try:
        output = candidate(test["input"])
        passed = output == test["expected"]
        if passed:
            result["passed_count"] += 1
        result["results"].append({
            "label": test["label"],
            "passed": bool(passed),
            "visibility": test["visibility"],
            "message": f"Passed ({output})" if passed else f"Expected {test['expected']}, got {output}"
        })
    except Exception as exc:
        result["results"].append({
            "label": test["label"],
            "passed": False,
            "visibility": test["visibility"],
            "message": f"Runtime error: {exc}"
        })

print(json.dumps(result))
`;

  const execution = spawnSync("python3", ["-c", harness], {
    encoding: "utf8",
    timeout: PY_TIMEOUT_MS,
    maxBuffer: 512 * 1024
  });

  if (execution.error) {
    const isTimeout = (execution.error as NodeJS.ErrnoException).code === "ETIMEDOUT";
    return {
      passedCount: 0,
      totalCount: question.testCases.length,
      details: [
        {
          label: "runner",
          passed: false,
          message: isTimeout
            ? "Python execution timed out."
            : `Python runner error: ${(execution.error as Error).message}`
        }
      ],
      manualReviewRequired: false
    };
  }

  const output = (execution.stdout ?? "").trim();
  const lastLine = output.split("\n").filter((line) => line.trim().length > 0).pop();

  if (!lastLine) {
    return {
      passedCount: 0,
      totalCount: question.testCases.length,
      details: [
        {
          label: "runner",
          passed: false,
          message: "Python runner produced no output."
        }
      ],
      manualReviewRequired: false
    };
  }

  try {
    const parsed = JSON.parse(lastLine) as {
      compile_error?: string | null;
      passed_count?: number;
      total_count?: number;
      results?: Array<{ label: string; passed: boolean; visibility: "visible" | "hidden"; message: string }>;
    };

    if (parsed.compile_error) {
      return {
        passedCount: 0,
        totalCount: question.testCases.length,
        details: [
          {
            label: "compile",
            passed: false,
            message: `Code did not compile: ${parsed.compile_error}`
          }
        ],
        manualReviewRequired: false
      };
    }

    const results = parsed.results ?? [];
    const details = results
      .filter((result) => result.visibility === "visible" || !result.passed)
      .map((result) => ({
        label: result.label,
        passed: result.passed,
        message: result.passed
          ? result.message
          : result.visibility === "hidden"
            ? "Hidden test failed."
            : result.message
      }));

    return {
      passedCount: parsed.passed_count ?? 0,
      totalCount: parsed.total_count ?? question.testCases.length,
      details,
      manualReviewRequired: false
    };
  } catch {
    return {
      passedCount: 0,
      totalCount: question.testCases.length,
      details: [
        {
          label: "runner",
          passed: false,
          message: "Could not parse Python runner output."
        }
      ],
      manualReviewRequired: false
    };
  }
}

function evaluateCodeSubmission(
  submission: string,
  language: CodeLanguage,
  question: CodeQuestionInternal
): CodeEvaluationResult {
  if (language === "python") {
    return evaluatePythonSubmission(submission, question);
  }
  return evaluateJavascriptSubmission(submission, question);
}

function sectionLabelForQuestionType(questionType: QuestionType): string {
  if (questionType === "mcq") {
    return "Multiple choice";
  }
  if (questionType === "code") {
    return "Coding challenge";
  }
  return "Written responses";
}

function buildRecommendations(focusTags: string[]): string[] {
  if (focusTags.length === 0) {
    return ["Maintain your current pace and run another mixed-format practice set this week."];
  }

  return focusTags.slice(0, 3).map((tag) => `Review ${tag.replace(/_/g, " ")} with one guided example, then retest.`);
}

export function scoreAssessmentSubmission(args: {
  definition: AssessmentDefinition;
  responses: AssessmentResponseItem[];
}): {
  reviewedItems: ReviewedAssessmentItem[];
  sectionScores: Array<{ label: string; correct: number; total: number }>;
  correctCount: number;
  totalCount: number;
  percentage: number;
  needsReview: boolean;
  focusAreas: string[];
  recommendations: string[];
  outcomes: QuestionOutcomeRecord[];
} {
  const responseByQuestionId = new Map<string, AssessmentResponseItem>();
  for (const response of args.responses) {
    responseByQuestionId.set(response.question_id, response);
  }

  const reviewedItems: ReviewedAssessmentItem[] = [];
  const outcomes: QuestionOutcomeRecord[] = [];

  const sectionAccumulator = new Map<string, { correct: number; total: number }>();
  const addSectionResult = (questionType: QuestionType, isCorrect: boolean) => {
    const label = sectionLabelForQuestionType(questionType);
    const current = sectionAccumulator.get(label) ?? { correct: 0, total: 0 };
    current.total += 1;
    if (isCorrect) {
      current.correct += 1;
    }
    sectionAccumulator.set(label, current);
  };

  for (const question of args.definition.internalQuestions) {
    const response = responseByQuestionId.get(question.id);

    if (question.type === "mcq") {
      const selectedIndex = response?.question_type === "mcq" ? response.selected_index : -1;
      const isCorrect = selectedIndex === question.correctIndex;
      const userResponse = selectedIndex >= 0 ? question.choices[selectedIndex] ?? "No answer" : "No answer";

      reviewedItems.push({
        id: question.id,
        question_type: "mcq",
        prompt: question.prompt,
        user_response: userResponse,
        expected: question.choices[question.correctIndex],
        is_correct: isCorrect,
        explanation: question.explanation,
        competency_tags: question.competencyTags
      });

      outcomes.push({
        question_id: question.id,
        question_type: "mcq",
        competency_tags: question.competencyTags,
        is_correct: isCorrect,
        earned_score: isCorrect ? 1 : 0,
        max_score: 1,
        manual_review_required: false,
        feedback: question.explanation,
        response_payload: { selected_index: selectedIndex, choice: userResponse },
        expected_payload: { selected_index: question.correctIndex, choice: question.choices[question.correctIndex] }
      });

      addSectionResult("mcq", isCorrect);
      continue;
    }

    if (question.type === "short_answer" || question.type === "open_ended") {
      const userText = response?.question_type === question.type ? response.text_response.trim() : "";
      const scored = evaluateWrittenAnswer(userText, question.rubricKeywords);
      const minimumLengthMet =
        userText
          .split(/\s+/)
          .filter((part: string) => part.length > 0).length >= question.minWords;
      const isCorrect = scored.isCorrect && minimumLengthMet;
      const manualReviewRequired = question.manualReviewMode && !isCorrect;

      reviewedItems.push({
        id: question.id,
        question_type: question.type,
        prompt: question.prompt,
        user_response: userText || "No answer",
        expected: scored.expected,
        is_correct: isCorrect,
        explanation: question.explanation,
        competency_tags: question.competencyTags,
        manual_review_required: manualReviewRequired
      });

      outcomes.push({
        question_id: question.id,
        question_type: question.type,
        competency_tags: question.competencyTags,
        is_correct: isCorrect,
        earned_score: isCorrect ? 1 : 0,
        max_score: 1,
        manual_review_required: manualReviewRequired,
        feedback: question.explanation,
        response_payload: { text_response: userText },
        expected_payload: { rubric_keywords: question.rubricKeywords, min_words: question.minWords }
      });

      addSectionResult(question.type, isCorrect);
      continue;
    }

    if (question.type !== "code") {
      continue;
    }

    const codeSubmission = response?.question_type === "code" ? response.code_submission : "";
    const language =
      response?.question_type === "code" ? response.language ?? question.defaultLanguage : question.defaultLanguage;
    const codeResult = evaluateCodeSubmission(codeSubmission, language, question);
    const passedAll = codeResult.passedCount === codeResult.totalCount;

    reviewedItems.push({
      id: question.id,
      question_type: "code",
      prompt: question.prompt,
      user_response: codeSubmission
        ? `Passed ${codeResult.passedCount}/${codeResult.totalCount} tests (${language}).`
        : "No answer",
      expected: `Pass all ${codeResult.totalCount}/${codeResult.totalCount} tests`,
      is_correct: passedAll,
      explanation: passedAll
        ? "Code passed all tests."
        : codeResult.details
            .filter((detail) => !detail.passed)
            .map((detail) => `${detail.label}: ${detail.message}`)
            .join(" | "),
      competency_tags: question.competencyTags,
      manual_review_required: codeResult.manualReviewRequired
    });

    outcomes.push({
      question_id: question.id,
      question_type: "code",
      competency_tags: question.competencyTags,
      is_correct: passedAll,
      earned_score: passedAll ? 1 : 0,
      max_score: 1,
      manual_review_required: codeResult.manualReviewRequired,
      feedback: codeResult.details.map((detail) => `${detail.label}: ${detail.message}`).join(" | "),
      response_payload: { code_submission: codeSubmission, language },
      expected_payload: {
        function_name: question.functionName,
        total_tests: question.testCases.length,
        visible_tests: question.testCases.filter((testCase) => testCase.visibility === "visible").length
      }
    });

    addSectionResult("code", passedAll);
  }

  const sectionScores = Array.from(sectionAccumulator.entries()).map(([label, score]) => ({
    label,
    correct: score.correct,
    total: score.total
  }));

  const totalCount = reviewedItems.length;
  const correctCount = reviewedItems.filter((item) => item.is_correct).length;
  const percentage = totalCount > 0 ? Number(((correctCount / totalCount) * 100).toFixed(1)) : 0;
  const focusAreas = reviewedItems.filter((item) => !item.is_correct).map((item) => item.prompt);

  const focusTagCounts = new Map<string, number>();
  for (const item of reviewedItems.filter((entry) => !entry.is_correct)) {
    for (const tag of item.competency_tags) {
      focusTagCounts.set(tag, (focusTagCounts.get(tag) ?? 0) + 1);
    }
  }

  const topTags = Array.from(focusTagCounts.entries())
    .sort((a, b) => b[1] - a[1])
    .map((entry) => entry[0]);

  return {
    reviewedItems,
    sectionScores,
    correctCount,
    totalCount,
    percentage,
    needsReview:
      totalCount === 0 ||
      percentage < 80 ||
      reviewedItems.some((item) => item.manual_review_required === true),
    focusAreas: focusAreas.slice(0, 4),
    recommendations: buildRecommendations(topTags),
    outcomes
  };
}
