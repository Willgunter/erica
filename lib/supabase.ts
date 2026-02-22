import { createClient } from "@supabase/supabase-js";

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
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

export function createSupabaseClient(accessToken?: string) {
  const supabaseUrl = requireEnv("NEXT_PUBLIC_SUPABASE_URL");
  const supabaseAnonKey = requireEnv("NEXT_PUBLIC_SUPABASE_ANON_KEY");

  return createClient(supabaseUrl, supabaseAnonKey, {
    global: {
      headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {}
    }
  });
}

export function createSupabaseServiceClient() {
  const supabaseUrl = requireEnv("NEXT_PUBLIC_SUPABASE_URL");
  const supabaseServiceRoleKey = requireEnv("SUPABASE_SERVICE_ROLE_KEY");

  return createClient(supabaseUrl, supabaseServiceRoleKey);
}

export async function resolveUserId(
  accessToken: string | null,
  devUserId: string | null
): Promise<{ userId: string } | { error: string; status: number }> {
  if (accessToken) {
    try {
      const supabase = createSupabaseClient(accessToken);
      const { data, error } = await supabase.auth.getUser(accessToken);

      if (error || !data.user) {
        if (process.env.NODE_ENV !== "production" && devUserId) {
          if (!isUuid(devUserId)) {
            return { error: "Invalid x-dev-user-id header (expected UUID).", status: 400 };
          }
          return { userId: devUserId };
        }
        return { error: "Unauthorized", status: 401 };
      }

      return { userId: data.user.id };
    } catch (error) {
      if (process.env.NODE_ENV !== "production" && devUserId && isTlsOrNetworkFetchError(error)) {
        if (!isUuid(devUserId)) {
          return { error: "Invalid x-dev-user-id header (expected UUID).", status: 400 };
        }
        return { userId: devUserId };
      }
      return { error: "Authentication service unavailable", status: 503 };
    }
  }

  if (process.env.NODE_ENV !== "production" && devUserId) {
    if (!isUuid(devUserId)) {
      return { error: "Invalid x-dev-user-id header (expected UUID).", status: 400 };
    }
    return { userId: devUserId };
  }

  return { error: "Unauthorized", status: 401 };
}
