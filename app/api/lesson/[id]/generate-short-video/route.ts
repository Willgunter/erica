import { NextResponse } from "next/server";

const FLASK_API_URL = process.env.FLASK_API_URL || "http://localhost:8000";

type JsonResponse = Record<string, unknown>;

function normalizeBaseUrl(url: string): string {
  return url.replace(/\/+$/, "");
}

function buildCandidateBaseUrls(configuredBaseUrl: string): string[] {
  return [
    configuredBaseUrl,
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
  ]
    .map((url) => normalizeBaseUrl(url).replace(/\/api\/?$/, ""))
    .filter(Boolean)
    .filter((url, index, all) => all.indexOf(url) === index);
}

function parseJsonSafely(raw: string): JsonResponse {
  if (!raw) return {};
  try {
    return JSON.parse(raw) as JsonResponse;
  } catch {
    return { raw };
  }
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const paramsData = await params;
    const body = await request.json();
    const lessonId = paramsData.id;
    const targets = buildCandidateBaseUrls(FLASK_API_URL).map((base) => `${base}/api/lesson/${lessonId}/generate-short-video`);
    const networkFailures: Array<{ target: string; message: string }> = [];
    const route404Targets: string[] = [];
    let lastErrorStatus = 502;
    let lastErrorData: JsonResponse = { error: "Failed to generate quick video" };

    for (const target of targets) {
      try {
        const response = await fetch(target, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(body)
        });
        const raw = await response.text();
        const data = parseJsonSafely(raw);

        if (response.ok) {
          return NextResponse.json(data, { status: response.status });
        }

        if (response.status === 404) {
          route404Targets.push(target);
          continue;
        }

        lastErrorStatus = response.status;
        lastErrorData = {
          error:
            typeof data.error === "string"
              ? data.error
              : `Quick video request failed with status ${response.status}`,
          details:
            typeof data.details === "string"
              ? data.details
              : `Backend target: ${target}`
        };
      } catch (error) {
        networkFailures.push({
          target,
          message: error instanceof Error ? error.message : "Unknown network error"
        });
      }
    }

    if (route404Targets.length > 0 && route404Targets.length === targets.length) {
      return NextResponse.json(
        {
          error: "Quick video endpoint not found",
          details: `Connected to backend but /api/lesson/:id/generate-short-video was not found. Tried: ${targets.join(", ")}`,
          hint: "Start Flask with: python app/main.py (includes lesson routes), or set FLASK_API_URL to that server."
        },
        { status: 404 }
      );
    }

    if (networkFailures.length === targets.length) {
      return NextResponse.json(
        {
          error: "Failed to connect to lesson service",
          details: `No backend reachable for quick video generation. Tried: ${targets.join(", ")}`,
          network_failures: networkFailures
        },
        { status: 503 }
      );
    }

    return NextResponse.json(lastErrorData, { status: lastErrorStatus });
  } catch (error) {
    console.error("Quick video generation proxy error:", error);
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : "Failed to connect to lesson service",
        details: "Make sure the Flask backend is running and FLASK_API_URL points to it."
      },
      { status: 500 }
    );
  }
}
