import { createClient } from "@supabase/supabase-js";

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
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

export async function resolveUserId(
  accessToken: string | null,
  devUserId: string | null
): Promise<{ userId: string } | { error: string; status: number }> {
  if (accessToken) {
    const supabase = createSupabaseClient(accessToken);
    const { data, error } = await supabase.auth.getUser(accessToken);

    if (error || !data.user) {
      return { error: "Unauthorized", status: 401 };
    }

    return { userId: data.user.id };
  }

  if (process.env.NODE_ENV !== "production" && devUserId) {
    return { userId: devUserId };
  }

  return { error: "Unauthorized", status: 401 };
}
