import type { PracticeTrack } from "@/lib/assessment";

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
