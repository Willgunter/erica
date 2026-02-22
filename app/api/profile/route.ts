import { NextResponse } from "next/server";
import { promises as fs } from "node:fs";
import path from "node:path";
import {
  composeProfileOutput,
  normalizeProfileInput,
  profileInputSchema,
  type DbPreferenceRow,
  type DbProfileRow
} from "@/lib/profile";
import { createSupabaseClient, createSupabaseServiceClient, resolveUserId } from "@/lib/supabase";

export const runtime = "nodejs";
const DEV_PROFILE_STORE_PATH = path.join(process.cwd(), "scratch", "profiles.dev.json");

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

function isTlsOrNetworkFetchError(error: unknown): boolean {
  if (!(error instanceof Error)) {
    return false;
  }

  const message = error.message.toLowerCase();
  if (message.includes("fetch failed")) {
    return true;
  }

  const cause = (error as Error & { cause?: unknown }).cause as { code?: unknown; message?: unknown } | undefined;
  const code = typeof cause?.code === "string" ? cause.code : "";
  const causeMessage = typeof cause?.message === "string" ? cause.message.toLowerCase() : "";

  return (
    code === "UNABLE_TO_GET_ISSUER_CERT_LOCALLY" ||
    code === "SELF_SIGNED_CERT_IN_CHAIN" ||
    code === "CERT_HAS_EXPIRED" ||
    code === "DEPTH_ZERO_SELF_SIGNED_CERT" ||
    code === "ECONNREFUSED" ||
    code === "ENOTFOUND" ||
    causeMessage.includes("certificate")
  );
}

function isMissingProfileSchema(errorMessage: string | undefined): boolean {
  if (!errorMessage) {
    return false;
  }

  const lowered = errorMessage.toLowerCase();
  return (
    lowered.includes("could not find the table 'public.profiles'") ||
    lowered.includes("could not find the table 'public.learning_preferences'") ||
    lowered.includes("relation") && (lowered.includes("profiles") || lowered.includes("learning_preferences")) ||
    lowered.includes("does not exist") ||
    (lowered.includes("schema cache") && (lowered.includes("profiles") || lowered.includes("learning_preferences")))
  );
}

async function readDevProfileStore(): Promise<Record<string, unknown>> {
  try {
    const raw = await fs.readFile(DEV_PROFILE_STORE_PATH, "utf8");
    const parsed = JSON.parse(raw) as Record<string, unknown>;
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch (error) {
    const code = (error as NodeJS.ErrnoException).code;
    if (code === "ENOENT") {
      return {};
    }
    throw error;
  }
}

async function writeDevProfileStore(store: Record<string, unknown>) {
  await fs.mkdir(path.dirname(DEV_PROFILE_STORE_PATH), { recursive: true });
  await fs.writeFile(DEV_PROFILE_STORE_PATH, JSON.stringify(store, null, 2), "utf8");
}

async function saveDevProfile(userId: string, profile: Record<string, unknown>) {
  const store = await readDevProfileStore();
  store[userId] = profile;
  await writeDevProfileStore(store);
}

async function getDevProfile(userId: string): Promise<Record<string, unknown> | null> {
  const store = await readDevProfileStore();
  const entry = store[userId];
  if (!entry || typeof entry !== "object") {
    return null;
  }
  return entry as Record<string, unknown>;
}

function buildDefaultDevProfile(userId: string): Record<string, unknown> {
  const normalized = normalizeProfileInput({});
  return {
    user_id: userId,
    ...normalized
  };
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

  let data:
    | {
        user: unknown;
      }
    | null = null;
  let error: { message: string } | null = null;
  try {
    const result = await serviceClient.auth.admin.getUserById(userId);
    data = result.data as { user: unknown } | null;
    error = result.error as { message: string } | null;
  } catch (fetchError) {
    if (isTlsOrNetworkFetchError(fetchError)) {
      // Best-effort in local dev: skip remote auth bootstrap when TLS/network is unavailable.
      return null;
    }
    return { error: fetchError instanceof Error ? fetchError.message : "Failed to access auth service", status: 500 };
  }
  if (data?.user) {
    return null;
  }

  if (error && !isUserNotFound(error.message)) {
    return { error: error.message, status: 500 };
  }

  let createError: { message: string } | null = null;
  try {
    const created = await serviceClient.auth.admin.createUser({
      id: userId,
      email: `dev-${userId}@local.erica.test`,
      password: `${userId.slice(0, 8)}Dev!123`,
      email_confirm: true,
      user_metadata: { source: "local-dev-profile" }
    });
    createError = created.error as { message: string } | null;
  } catch (fetchError) {
    if (isTlsOrNetworkFetchError(fetchError)) {
      return null;
    }
    return { error: fetchError instanceof Error ? fetchError.message : "Failed to create auth user", status: 500 };
  }

  if (createError && !isAlreadyExists(createError.message)) {
    return { error: createError.message, status: 500 };
  }

  return null;
}

export async function POST(request: Request) {
  const accessToken = getBearerToken(request.headers.get("authorization"));
  const devUserId = request.headers.get("x-dev-user-id");
  let resolvedUser: Awaited<ReturnType<typeof resolveUserId>>;
  try {
    resolvedUser = await resolveUserId(accessToken, devUserId);
  } catch (error) {
    if (process.env.NODE_ENV !== "production" && devUserId) {
      resolvedUser = { userId: devUserId };
    } else {
      return NextResponse.json(
        { error: error instanceof Error ? error.message : "Failed to resolve user" },
        { status: 500 }
      );
    }
  }

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
  const profileForResponse: Record<string, unknown> = {
    user_id: resolvedUser.userId,
    ...normalized
  };

  console.log("[POST /api/profile] Saving profile for user:", resolvedUser.userId);

  const useDevFallback =
    process.env.NODE_ENV !== "production" && Boolean(devUserId) && resolvedUser.userId === devUserId;
  if (useDevFallback) {
    console.log("[POST /api/profile] Using dev fallback mode");
    const ensureUserError = await ensureDevAuthUserExists(resolvedUser.userId);
    if (ensureUserError) {
      return NextResponse.json({ error: ensureUserError.error }, { status: ensureUserError.status });
    }
  }

  const supabase = useDevFallback
    ? createSupabaseServiceClient()
    : createSupabaseClient(accessToken ?? undefined);

  let profileError: { message: string } | null = null;
  try {
    const profileResult = await supabase.from("profiles").upsert(
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
    profileError = profileResult.error as { message: string } | null;
  } catch (error) {
    if (process.env.NODE_ENV !== "production" && useDevFallback && isTlsOrNetworkFetchError(error)) {
      await saveDevProfile(resolvedUser.userId, profileForResponse);
      return NextResponse.json({ profile: profileForResponse }, { status: 200 });
    }
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to persist profile" },
      { status: 500 }
    );
  }

  if (profileError) {
    if (
      process.env.NODE_ENV !== "production" &&
      (isMissingProfileSchema(profileError.message) || useDevFallback)
    ) {
      try {
        await saveDevProfile(resolvedUser.userId, profileForResponse);
        return NextResponse.json({ profile: profileForResponse }, { status: 200 });
      } catch (storeError) {
        return NextResponse.json(
          { error: `Supabase schema missing and local fallback failed: ${(storeError as Error).message}` },
          { status: 500 }
        );
      }
    }
    return NextResponse.json({ error: profileError.message }, { status: 500 });
  }

  let preferencesError: { message: string } | null = null;
  try {
    const preferenceResult = await supabase.from("learning_preferences").upsert(
      {
        user_id: resolvedUser.userId,
        teaching_style: normalized.learning_preferences.teaching_style,
        content_formats: normalized.learning_preferences.content_formats,
        review_preferences: normalized.learning_preferences.review_preferences,
        uncertainty_flags: normalized.learning_preferences.uncertainty_flags
      },
      { onConflict: "user_id" }
    );
    preferencesError = preferenceResult.error as { message: string } | null;
  } catch (error) {
    if (process.env.NODE_ENV !== "production" && useDevFallback && isTlsOrNetworkFetchError(error)) {
      await saveDevProfile(resolvedUser.userId, profileForResponse);
      return NextResponse.json({ profile: profileForResponse }, { status: 200 });
    }
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to persist learning preferences" },
      { status: 500 }
    );
  }

  if (preferencesError) {
    if (
      process.env.NODE_ENV !== "production" &&
      (isMissingProfileSchema(preferencesError.message) || useDevFallback)
    ) {
      try {
        await saveDevProfile(resolvedUser.userId, profileForResponse);
        return NextResponse.json({ profile: profileForResponse }, { status: 200 });
      } catch (storeError) {
        return NextResponse.json(
          { error: `Supabase schema missing and local fallback failed: ${(storeError as Error).message}` },
          { status: 500 }
        );
      }
    }
    return NextResponse.json({ error: preferencesError.message }, { status: 500 });
  }

  if (useDevFallback) {
    try {
      await saveDevProfile(resolvedUser.userId, profileForResponse);
    } catch (storeError) {
      console.warn("[POST /api/profile] Failed to persist local dev profile copy:", storeError);
    }
  }

  return NextResponse.json(
    {
      profile: profileForResponse
    },
    { status: 200 }
  );
}

export async function GET(request: Request) {
  const accessToken = getBearerToken(request.headers.get("authorization"));
  const devUserId = request.headers.get("x-dev-user-id");
  let resolvedUser: Awaited<ReturnType<typeof resolveUserId>>;
  try {
    resolvedUser = await resolveUserId(accessToken, devUserId);
  } catch (error) {
    if (process.env.NODE_ENV !== "production" && devUserId) {
      resolvedUser = { userId: devUserId };
    } else {
      return NextResponse.json(
        { error: error instanceof Error ? error.message : "Failed to resolve user" },
        { status: 500 }
      );
    }
  }

  if ("error" in resolvedUser) {
    return NextResponse.json({ error: resolvedUser.error }, { status: resolvedUser.status });
  }

  console.log("[GET /api/profile] Fetching profile for user:", resolvedUser.userId);

  const useDevFallback = process.env.NODE_ENV !== "production" && Boolean(devUserId);
  if (useDevFallback) {
    console.log("[GET /api/profile] Using dev fallback mode (service client)");
    const ensureUserError = await ensureDevAuthUserExists(resolvedUser.userId);
    if (ensureUserError) {
      return NextResponse.json({ error: ensureUserError.error }, { status: ensureUserError.status });
    }
  }

  const supabase = useDevFallback
    ? createSupabaseServiceClient()
    : createSupabaseClient(accessToken ?? undefined);

  let profileData: unknown = null;
  let preferenceData: unknown = null;
  let profileError: { message: string } | null = null;
  let preferenceError: { message: string } | null = null;
  try {
    const [profileResult, preferenceResult] = await Promise.all([
      supabase.from("profiles").select("*").eq("user_id", resolvedUser.userId).maybeSingle(),
      supabase
        .from("learning_preferences")
        .select("*")
        .eq("user_id", resolvedUser.userId)
        .maybeSingle()
    ]);
    profileData = profileResult.data;
    preferenceData = preferenceResult.data;
    profileError = profileResult.error as { message: string } | null;
    preferenceError = preferenceResult.error as { message: string } | null;
  } catch (error) {
    if (process.env.NODE_ENV !== "production" && useDevFallback && isTlsOrNetworkFetchError(error)) {
      const devProfile = await getDevProfile(resolvedUser.userId);
      if (devProfile) {
        return NextResponse.json({ profile: devProfile }, { status: 200 });
      }
      const seededProfile = buildDefaultDevProfile(resolvedUser.userId);
      await saveDevProfile(resolvedUser.userId, seededProfile);
      return NextResponse.json({ profile: seededProfile }, { status: 200 });
    }
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Could not fetch profile" },
      { status: 500 }
    );
  }

  if (profileError || preferenceError) {
    const maybeMissingSchemaMessage = profileError?.message ?? preferenceError?.message;
    console.log("[GET /api/profile] Supabase error:", maybeMissingSchemaMessage);
    
    if (process.env.NODE_ENV !== "production") {
      console.log("[GET /api/profile] Attempting dev fallback for user:", resolvedUser.userId);
      try {
        const devProfile = await getDevProfile(resolvedUser.userId);
        if (devProfile) {
          console.log("[GET /api/profile] Found dev profile");
          return NextResponse.json({ profile: devProfile }, { status: 200 });
        }
        console.log("[GET /api/profile] No dev profile found");
      } catch (storeError) {
        console.error("[GET /api/profile] Dev fallback error:", storeError);
      }
    }

    return NextResponse.json(
      { error: profileError?.message ?? preferenceError?.message ?? "Could not fetch profile" },
      { status: 500 }
    );
  }

  if (!profileData || !preferenceData) {
    if (process.env.NODE_ENV !== "production") {
      const devProfile = await getDevProfile(resolvedUser.userId);
      if (devProfile) {
        return NextResponse.json({ profile: devProfile }, { status: 200 });
      }
      if (useDevFallback) {
        const seededProfile = buildDefaultDevProfile(resolvedUser.userId);
        await saveDevProfile(resolvedUser.userId, seededProfile);
        return NextResponse.json({ profile: seededProfile }, { status: 200 });
      }
    }

    return NextResponse.json({ error: "Profile not found" }, { status: 404 });
  }

  const profile = composeProfileOutput(profileData as DbProfileRow, preferenceData as DbPreferenceRow);

  return NextResponse.json({ profile }, { status: 200 });
}
