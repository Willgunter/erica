import type { QuestionType } from "@/lib/assessment";
import type { AssessmentDefinition } from "@/lib/assessment-engine";

type InternalQuestion = AssessmentDefinition["internalQuestions"][number];

const MAX_GENERATED_QUESTIONS = 12;

const STOP_WORDS = new Set([
  "about",
  "after",
  "also",
  "because",
  "between",
  "being",
  "could",
  "does",
  "from",
  "have",
  "into",
  "just",
  "more",
  "most",
  "should",
  "that",
  "their",
  "there",
  "these",
  "this",
  "those",
  "through",
  "what",
  "when",
  "where",
  "which",
  "while",
  "with",
  "would",
  "your"
]);

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function cleanText(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function toStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value.map(cleanText).filter((item) => item.length > 0);
}

function tokenize(value: string): string[] {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((token) => token.length >= 3 && !STOP_WORDS.has(token));
}

function unique(values: string[]): string[] {
  return Array.from(new Set(values));
}

function deriveRubricKeywords(values: string[]): string[] {
  const combined = values
    .map((value) => cleanText(value))
    .filter((value) => value.length > 0)
    .join(" ");
  const tokens = unique(tokenize(combined)).slice(0, 8);
  if (tokens.length > 0) {
    return tokens;
  }

  return ["concept", "application"];
}

function deriveCompetencyTags(title: string): string[] {
  const tokens = unique(tokenize(title)).slice(0, 3);
  if (tokens.length > 0) {
    return tokens;
  }

  return ["lesson_mastery"];
}

function normalizeQuestionType(index: number): "short_answer" | "open_ended" {
  return (index + 1) % 3 === 0 ? "open_ended" : "short_answer";
}

type ModuleQuestionCandidate = {
  prompt: string;
  answer: string;
  hints: string[];
};

function readModuleQuestionCandidates(module: Record<string, unknown>): ModuleQuestionCandidate[] {
  const candidates: ModuleQuestionCandidate[] = [];
  const examQuestions = Array.isArray(module.exam_questions) ? module.exam_questions : [];
  for (const entry of examQuestions) {
    if (!isPlainObject(entry)) {
      continue;
    }

    const prompt = cleanText(entry.question);
    if (!prompt) {
      continue;
    }

    const answer = cleanText(entry.answer);
    const hints = toStringArray(entry.hints).slice(0, 3);
    candidates.push({ prompt, answer, hints });
  }

  if (candidates.length > 0) {
    return candidates;
  }

  const checkpoint = isPlainObject(module.checkpoint) ? module.checkpoint : null;
  const checkpointQuestions = checkpoint ? toStringArray(checkpoint.questions) : [];
  const fallbackAnswer = cleanText(module.key_insight) || cleanText(module.concept_explanation);

  return checkpointQuestions.map((prompt) => ({
    prompt,
    answer: fallbackAnswer,
    hints: []
  }));
}

export function buildInternalQuestionsFromLesson(lesson: unknown): InternalQuestion[] {
  if (!isPlainObject(lesson) || !Array.isArray(lesson.modules)) {
    return [];
  }

  const questions: InternalQuestion[] = [];
  lesson.modules.forEach((entry, moduleIndex) => {
    if (!isPlainObject(entry) || questions.length >= MAX_GENERATED_QUESTIONS) {
      return;
    }

    const moduleTitle = cleanText(entry.title) || `Module ${moduleIndex + 1}`;
    const competencyTags = deriveCompetencyTags(moduleTitle);
    const moduleCandidates = readModuleQuestionCandidates(entry).slice(0, 3);

    moduleCandidates.forEach((candidate, candidateIndex) => {
      if (questions.length >= MAX_GENERATED_QUESTIONS) {
        return;
      }

      const type = normalizeQuestionType(candidateIndex);
      const rubricKeywords = deriveRubricKeywords([candidate.answer, ...candidate.hints, candidate.prompt]);
      const explanation =
        candidate.answer ||
        candidate.hints[0] ||
        `Review ${moduleTitle.toLowerCase()} in your uploaded material and explain your reasoning.`;

      questions.push({
        id: `lesson-q-${moduleIndex + 1}-${candidateIndex + 1}`,
        type,
        prompt: candidate.prompt,
        rubricKeywords,
        explanation,
        minWords: type === "open_ended" ? 28 : 12,
        competencyTags,
        manualReviewMode: type === "open_ended"
      });
    });
  });

  return questions;
}

function isQuestionType(value: unknown): value is QuestionType {
  return value === "mcq" || value === "short_answer" || value === "open_ended" || value === "code";
}

function isStringTupleOfFour(value: unknown): value is [string, string, string, string] {
  return (
    Array.isArray(value) &&
    value.length === 4 &&
    value.every((entry) => typeof entry === "string" && entry.trim().length > 0)
  );
}

function serializeQuestion(question: InternalQuestion): Record<string, unknown> {
  if (question.type === "mcq") {
    return {
      id: question.id,
      type: question.type,
      prompt: question.prompt,
      choices: [...question.choices],
      correctIndex: question.correctIndex,
      explanation: question.explanation,
      competencyTags: [...question.competencyTags]
    };
  }

  if (question.type === "code") {
    return {
      id: question.id,
      type: question.type,
      title: question.title,
      prompt: question.prompt,
      functionName: question.functionName,
      starterCode: question.starterCode,
      defaultLanguage: question.defaultLanguage,
      allowedLanguages: [...question.allowedLanguages],
      testCases: question.testCases.map((testCase) => ({
        label: testCase.label,
        input: [...testCase.input],
        expected: testCase.expected,
        visibility: testCase.visibility
      })),
      explanation: question.explanation,
      competencyTags: [...question.competencyTags]
    };
  }

  return {
    id: question.id,
    type: question.type,
    prompt: question.prompt,
    rubricKeywords: [...question.rubricKeywords],
    explanation: question.explanation,
    minWords: question.minWords,
    competencyTags: [...question.competencyTags],
    manualReviewMode: question.manualReviewMode
  };
}

export function serializeInternalQuestionsForSnapshot(questions: InternalQuestion[]): Record<string, unknown>[] {
  return questions.map((question) => serializeQuestion(question));
}

function parseSnapshotQuestion(value: unknown): InternalQuestion | null {
  if (!isPlainObject(value)) {
    return null;
  }

  const id = cleanText(value.id);
  const type = value.type;
  const prompt = cleanText(value.prompt);
  const competencyTags = toStringArray(value.competencyTags);
  const explanation = cleanText(value.explanation);

  if (!id || !isQuestionType(type) || !prompt) {
    return null;
  }

  if (type === "mcq") {
    const choices = value.choices;
    const correctIndex = value.correctIndex;
    if (!isStringTupleOfFour(choices) || typeof correctIndex !== "number" || !Number.isInteger(correctIndex)) {
      return null;
    }

    if (correctIndex < 0 || correctIndex > 3) {
      return null;
    }

    return {
      id,
      type,
      prompt,
      choices,
      correctIndex,
      explanation,
      competencyTags
    };
  }

  if (type === "code") {
    const title = cleanText(value.title);
    const functionName = cleanText(value.functionName);
    const starterCode = cleanText(value.starterCode);
    const defaultLanguage = value.defaultLanguage;
    const allowedLanguages = toStringArray(value.allowedLanguages);
    const testCasesRaw = Array.isArray(value.testCases) ? value.testCases : [];

    if (
      !title ||
      !functionName ||
      !starterCode ||
      (defaultLanguage !== "javascript" && defaultLanguage !== "python")
    ) {
      return null;
    }

    const testCases = testCasesRaw
      .map((entry) => {
        if (!isPlainObject(entry)) {
          return null;
        }

        const label = cleanText(entry.label);
        const visibility = entry.visibility;
        const expected = entry.expected;
        const input = Array.isArray(entry.input) ? entry.input : [];
        if (
          !label ||
          (visibility !== "visible" && visibility !== "hidden") ||
          typeof expected !== "number" ||
          !input.every((inputItem) => typeof inputItem === "number")
        ) {
          return null;
        }

        return {
          label,
          visibility,
          expected,
          input: input as number[]
        };
      })
      .filter((entry): entry is { label: string; visibility: "visible" | "hidden"; expected: number; input: number[] } =>
        Boolean(entry)
      );

    if (testCases.length === 0) {
      return null;
    }

    const normalizedAllowedLanguages = allowedLanguages.filter(
      (language): language is "javascript" | "python" => language === "javascript" || language === "python"
    );

    if (normalizedAllowedLanguages.length === 0) {
      normalizedAllowedLanguages.push(defaultLanguage);
    }

    return {
      id,
      type,
      title,
      prompt,
      functionName,
      starterCode,
      defaultLanguage,
      allowedLanguages: normalizedAllowedLanguages,
      testCases,
      explanation,
      competencyTags
    };
  }

  const rubricKeywords = toStringArray(value.rubricKeywords);
  const minWordsRaw = value.minWords;
  const minWords = typeof minWordsRaw === "number" && Number.isFinite(minWordsRaw) ? minWordsRaw : 12;
  const manualReviewMode = Boolean(value.manualReviewMode);

  if (rubricKeywords.length === 0) {
    return null;
  }

  return {
    id,
    type,
    prompt,
    rubricKeywords,
    explanation,
    minWords,
    competencyTags,
    manualReviewMode
  };
}

export function parseInternalQuestionsFromSnapshot(value: unknown): InternalQuestion[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value.map((entry) => parseSnapshotQuestion(entry)).filter((entry): entry is InternalQuestion => Boolean(entry));
}
