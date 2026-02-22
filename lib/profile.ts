import { z } from "next/dist/compiled/zod";

const SUBJECT_FALLBACK = "General learning";
const GOALS_FALLBACK = ["Build confidence"];

export const studyTimeSchema = z.enum(["15_min", "30_min", "45_min", "60_min_plus"]);
export const pacingSchema = z.enum(["light", "steady", "accelerated"]);
export const teachingStyleSchema = z.enum(["visual", "socratic", "project_based", "mixed"]);
export const contentFormatSchema = z.enum(["text", "video", "interactive", "audio", "flashcards"]);
export const reviewPreferenceSchema = z.enum([
  "spaced_repetition",
  "practice_quiz",
  "reflection",
  "teach_back"
]);

export const profileInputSchema = z.object({
  subject: z.string().trim().max(80).optional(),
  goals: z.array(z.string().trim().min(1).max(120)).max(8).optional(),
  studyTime: studyTimeSchema.optional(),
  pacing: pacingSchema.optional(),
  teachingStyle: z.union([teachingStyleSchema, z.literal("not_sure")]).optional(),
  contentFormats: z.array(contentFormatSchema).max(5).optional(),
  reviewPreferences: z.array(reviewPreferenceSchema).max(4).optional(),
  accessibility: z
    .object({
      captions: z.boolean().optional(),
      highContrast: z.boolean().optional(),
      reduceMotion: z.boolean().optional(),
      dyslexiaFriendlyFont: z.boolean().optional(),
      screenReaderOptimized: z.boolean().optional()
    })
    .optional()
});

export type ProfileInput = z.infer<typeof profileInputSchema>;

export type AccessibilitySettings = {
  captions: boolean;
  highContrast: boolean;
  reduceMotion: boolean;
  dyslexiaFriendlyFont: boolean;
  screenReaderOptimized: boolean;
};

export type NormalizedProfile = {
  subject: string;
  goals: string[];
  study_time: z.infer<typeof studyTimeSchema>;
  pacing: z.infer<typeof pacingSchema>;
  accessibility: AccessibilitySettings;
  learning_preferences: {
    teaching_style: z.infer<typeof teachingStyleSchema> | null;
    content_formats: Array<z.infer<typeof contentFormatSchema>>;
    review_preferences: Array<z.infer<typeof reviewPreferenceSchema>>;
    uncertainty_flags: {
      teaching_style: boolean;
    };
  };
};

const uniq = <T,>(values: T[]): T[] => [...new Set(values)];
const defaultAccessibility: AccessibilitySettings = {
  captions: false,
  highContrast: false,
  reduceMotion: false,
  dyslexiaFriendlyFont: false,
  screenReaderOptimized: false
};

export function normalizeProfileInput(rawInput: ProfileInput): NormalizedProfile {
  const input = profileInputSchema.parse(rawInput);

  const subject = input.subject && input.subject.length > 0 ? input.subject : SUBJECT_FALLBACK;
  const goals = uniq(input.goals && input.goals.length > 0 ? input.goals : GOALS_FALLBACK);

  const accessibility: AccessibilitySettings = {
    captions: Boolean(input.accessibility?.captions),
    highContrast: Boolean(input.accessibility?.highContrast),
    reduceMotion: Boolean(input.accessibility?.reduceMotion),
    dyslexiaFriendlyFont: Boolean(input.accessibility?.dyslexiaFriendlyFont),
    screenReaderOptimized: Boolean(input.accessibility?.screenReaderOptimized)
  };

  const teachingStyleIsUncertain = !input.teachingStyle || input.teachingStyle === "not_sure";
  const teachingStyle = teachingStyleIsUncertain ? null : input.teachingStyle;

  return {
    subject,
    goals,
    study_time: input.studyTime ?? "30_min",
    pacing: input.pacing ?? "steady",
    accessibility,
    learning_preferences: {
      teaching_style: teachingStyle,
      content_formats: uniq(input.contentFormats && input.contentFormats.length > 0 ? input.contentFormats : ["text", "interactive"]),
      review_preferences: uniq(
        input.reviewPreferences && input.reviewPreferences.length > 0
          ? input.reviewPreferences
          : ["practice_quiz"]
      ),
      uncertainty_flags: {
        teaching_style: teachingStyleIsUncertain
      }
    }
  };
}

const dbAccessibilitySchema = z
  .object({
    captions: z.boolean().optional(),
    highContrast: z.boolean().optional(),
    reduceMotion: z.boolean().optional(),
    dyslexiaFriendlyFont: z.boolean().optional(),
    screenReaderOptimized: z.boolean().optional()
  })
  .transform((accessibility) => ({
    captions: accessibility.captions ?? false,
    highContrast: accessibility.highContrast ?? false,
    reduceMotion: accessibility.reduceMotion ?? false,
    dyslexiaFriendlyFont: accessibility.dyslexiaFriendlyFont ?? false,
    screenReaderOptimized: accessibility.screenReaderOptimized ?? false
  }));

const dbUncertaintyFlagsSchema = z
  .object({
    teaching_style: z.boolean().optional()
  })
  .transform((flags) => ({
    teaching_style: flags.teaching_style ?? false
  }));

const dbProfileSchema = z.object({
  user_id: z.string().uuid(),
  subject: z.string(),
  goals: z.array(z.string()).optional().default([]),
  study_time: studyTimeSchema,
  pacing: pacingSchema,
  accessibility: dbAccessibilitySchema.catch(defaultAccessibility)
});

const dbPreferenceSchema = z.object({
  user_id: z.string().uuid(),
  teaching_style: teachingStyleSchema.nullable().optional().default(null),
  content_formats: z.array(contentFormatSchema).optional().default([]),
  review_preferences: z.array(reviewPreferenceSchema).optional().default([]),
  uncertainty_flags: dbUncertaintyFlagsSchema.catch({ teaching_style: false })
});

export type DbProfileRow = z.infer<typeof dbProfileSchema>;
export type DbPreferenceRow = z.infer<typeof dbPreferenceSchema>;

export function composeProfileOutput(profile: DbProfileRow, preferences: DbPreferenceRow) {
  const parsedProfile = dbProfileSchema.parse(profile);
  const parsedPreferences = dbPreferenceSchema.parse(preferences);

  return {
    user_id: parsedProfile.user_id,
    subject: parsedProfile.subject.trim().length > 0 ? parsedProfile.subject : SUBJECT_FALLBACK,
    goals: parsedProfile.goals.length > 0 ? parsedProfile.goals : GOALS_FALLBACK,
    study_time: parsedProfile.study_time,
    pacing: parsedProfile.pacing,
    accessibility: parsedProfile.accessibility,
    learning_preferences: {
      teaching_style: parsedPreferences.teaching_style,
      content_formats: parsedPreferences.content_formats,
      review_preferences: parsedPreferences.review_preferences,
      uncertainty_flags: parsedPreferences.uncertainty_flags
    }
  };
}
