import { NextResponse } from "next/server";
import {
  composeProfileOutput,
  normalizeProfileInput,
  profileInputSchema,
  type DbPreferenceRow,
  type DbProfileRow
} from "@/lib/profile";
import { createSupabaseClient, resolveUserId } from "@/lib/supabase";

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

export async function POST(request: Request) {
  const accessToken = getBearerToken(request.headers.get("authorization"));
  const resolvedUser = await resolveUserId(accessToken, request.headers.get("x-dev-user-id"));

  if ("error" in resolvedUser) {
    return NextResponse.json({ error: resolvedUser.error }, { status: resolvedUser.status });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const parsed = profileInputSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json(
      {
        error: "Invalid profile payload",
        details: parsed.error.issues
      },
      { status: 400 }
    );
  }

  const normalized = normalizeProfileInput(parsed.data);
  const supabase = createSupabaseClient(accessToken ?? undefined);

  const { error: profileError } = await supabase.from("profiles").upsert(
    {
      user_id: resolvedUser.userId,
      subject: normalized.subject,
      goals: normalized.goals,
      study_time: normalized.study_time,
      pacing: normalized.pacing,
      accessibility: normalized.accessibility
    },
    { onConflict: "user_id" }
  );

  if (profileError) {
    return NextResponse.json({ error: profileError.message }, { status: 500 });
  }

  const { error: preferencesError } = await supabase.from("learning_preferences").upsert(
    {
      user_id: resolvedUser.userId,
      teaching_style: normalized.learning_preferences.teaching_style,
      content_formats: normalized.learning_preferences.content_formats,
      review_preferences: normalized.learning_preferences.review_preferences,
      uncertainty_flags: normalized.learning_preferences.uncertainty_flags
    },
    { onConflict: "user_id" }
  );

  if (preferencesError) {
    return NextResponse.json({ error: preferencesError.message }, { status: 500 });
  }

  return NextResponse.json(
    {
      profile: {
        user_id: resolvedUser.userId,
        ...normalized
      }
    },
    { status: 200 }
  );
}

export async function GET(request: Request) {
  const accessToken = getBearerToken(request.headers.get("authorization"));
  const resolvedUser = await resolveUserId(accessToken, request.headers.get("x-dev-user-id"));

  if ("error" in resolvedUser) {
    return NextResponse.json({ error: resolvedUser.error }, { status: resolvedUser.status });
  }

  const supabase = createSupabaseClient(accessToken ?? undefined);

  const [{ data: profileData, error: profileError }, { data: preferenceData, error: preferenceError }] =
    await Promise.all([
      supabase.from("profiles").select("*").eq("user_id", resolvedUser.userId).maybeSingle(),
      supabase
        .from("learning_preferences")
        .select("*")
        .eq("user_id", resolvedUser.userId)
        .maybeSingle()
    ]);

  if (profileError || preferenceError) {
    return NextResponse.json(
      { error: profileError?.message ?? preferenceError?.message ?? "Could not fetch profile" },
      { status: 500 }
    );
  }

  if (!profileData || !preferenceData) {
    return NextResponse.json({ error: "Profile not found" }, { status: 404 });
  }

  const profile = composeProfileOutput(profileData as DbProfileRow, preferenceData as DbPreferenceRow);

  return NextResponse.json({ profile }, { status: 200 });
}
