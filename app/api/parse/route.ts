import { appendFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";

export const runtime = "nodejs";

const FLASK_API_URL = (process.env.FLASK_API_URL || "http://localhost:8000").replace(/\/+$/, "");
const PARSE_ERROR_LOG_PATH = path.join(process.cwd(), "scratch", "parse-api-errors.jsonl");

type JsonResponse = Record<string, unknown>;
type AttemptLog = {
  target: string;
  duration_ms: number;
  status?: number;
  ok: boolean;
  error?: string;
  backend_error?: string;
};
type NetworkFailure = { target: string; message: string };
type ParseLogContext = {
  request_id: string;
  configured_flask_base_url: string;
  targets: string[];
  request_meta: Record<string, string>;
  file_meta: Record<string, unknown>;
  total_duration_ms: number;
  attempts: AttemptLog[];
  network_failures: NetworkFailure[];
  result_status: number;
  result_body: Record<string, unknown>;
};
type HttpFailure = { target: string; status: number };

function normalizeBaseUrl(url: string): string {
  return url.replace(/\/+$/, "");
}

function cleanWhitespace(text: string): string {
  return text.replace(/\s+/g, " ").trim();
}

function smartSlice(text: string, start: number, maxLen: number): [string, number] {
  const end = Math.min(start + maxLen, text.length);
  if (end === text.length) {
    return [text.slice(start, end), end];
  }

  const cut = text.lastIndexOf(" ", end);
  if (cut <= start) {
    return [text.slice(start, end), end];
  }
  return [text.slice(start, cut), cut];
}

function buildLocalTextChunks(text: string, fileName: string): Array<Record<string, unknown>> {
  const cleaned = cleanWhitespace(text);
  if (!cleaned) return [];

  const chunks: Array<Record<string, unknown>> = [];
  const targetChars = 1200;
  const overlapChars = 200;
  let index = 0;
  let start = 0;

  while (start < cleaned.length) {
    const [pieceRaw, end] = smartSlice(cleaned, start, targetChars);
    const piece = pieceRaw.trim();
    if (piece) {
      chunks.push({
        id: crypto.randomUUID(),
        chunk_index: index,
        text: piece,
        metadata: {
          parser: "next-local-fallback",
          filename: fileName,
          start_char: start,
          end_char: end,
          length: piece.length
        }
      });
      index += 1;
    }
    if (end >= cleaned.length) break;
    start = Math.max(0, end - overlapChars);
  }

  return chunks;
}

function supportsLocalTextFallback(file: File): boolean {
  const type = (file.type || "").toLowerCase();
  const name = (file.name || "").toLowerCase();
  return type === "text/plain" || type === "text/markdown" || name.endsWith(".txt") || name.endsWith(".md");
}

function buildParseTargets(baseUrl: string): string[] {
  const base = normalizeBaseUrl(baseUrl);
  const noApi = base.replace(/\/api\/?$/, "");
  return [`${base}/api/parse`, `${noApi}/api/parse`, `${base}/parse`, `${noApi}/parse`];
}

function buildCandidateBaseUrls(configuredBaseUrl: string): string[] {
  const candidates = [
    configuredBaseUrl,
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5000",
    "http://127.0.0.1:5000"
  ].map(normalizeBaseUrl);

  return [...new Set(candidates)];
}

function describeFetchError(error: unknown): string {
  if (error instanceof Error) {
    const cause = error.cause;
    if (cause && typeof cause === "object") {
      const withCode = cause as { code?: unknown; message?: unknown };
      const code = typeof withCode.code === "string" ? withCode.code : null;
      const message = typeof withCode.message === "string" ? withCode.message : null;
      if (code && message) return `${code}: ${message}`;
      if (code) return code;
      if (message) return message;
    }
    return error.message || "Unknown network error";
  }

  return "Unknown network error";
}

async function appendParseErrorLog(context: ParseLogContext): Promise<void> {
  try {
    await mkdir(path.dirname(PARSE_ERROR_LOG_PATH), { recursive: true });
    await appendFile(
      PARSE_ERROR_LOG_PATH,
      `${JSON.stringify({ timestamp: new Date().toISOString(), ...context })}\n`,
      "utf8"
    );
  } catch (error) {
    console.error("Failed to write parse API log:", error);
  }
}

export async function POST(request: Request) {
  const requestId = crypto.randomUUID();
  const requestStart = Date.now();
  const attempts: AttemptLog[] = [];
  const networkFailures: NetworkFailure[] = [];
  const httpFailures: HttpFailure[] = [];
  const requestMeta = {
    method: request.method,
    user_agent: request.headers.get("user-agent") || "",
    referer: request.headers.get("referer") || "",
    origin: request.headers.get("origin") || "",
    x_forwarded_for: request.headers.get("x-forwarded-for") || ""
  };

  try {
    const formData = await request.formData();
    const filePart = formData.get("file");
    const file = filePart instanceof File ? filePart : null;

    if (!file) {
      const responseBody = { error: "No file provided", request_id: requestId };
      await appendParseErrorLog({
        request_id: requestId,
        configured_flask_base_url: FLASK_API_URL,
        targets: [],
        request_meta: requestMeta,
        file_meta: {},
        total_duration_ms: Date.now() - requestStart,
        attempts,
        network_failures: networkFailures,
        result_status: 400,
        result_body: responseBody
      });
      return NextResponse.json(responseBody, { status: 400 });
    }

    const fileMeta = {
      name: file.name,
      type: file.type,
      size: file.size
    };

    if (supportsLocalTextFallback(file)) {
      const rawText = await file.text();
      const chunks = buildLocalTextChunks(rawText, file.name);
      if (chunks.length > 0) {
        const responseBody = {
          chunks,
          parser: "next-local-fallback",
          request_id: requestId
        };
        await appendParseErrorLog({
          request_id: requestId,
          configured_flask_base_url: FLASK_API_URL,
          targets: [],
          request_meta: requestMeta,
          file_meta: fileMeta,
          total_duration_ms: Date.now() - requestStart,
          attempts,
          network_failures: networkFailures,
          result_status: 200,
          result_body: { parser: "next-local-fallback", chunks_count: chunks.length }
        });
        return NextResponse.json(responseBody, { status: 200 });
      }
    }

    const targets = [...new Set(buildCandidateBaseUrls(FLASK_API_URL).flatMap(buildParseTargets))];
    let lastErrorStatus = 500;
    let lastErrorData: JsonResponse = { error: "Failed to parse file" };

    for (const target of targets) {
      const attemptStart = Date.now();
      try {
        const response = await fetch(target, {
          method: "POST",
          body: formData
        });

        const maybeJson = await response.text();
        let data: JsonResponse;
        try {
          data = maybeJson ? (JSON.parse(maybeJson) as JsonResponse) : {};
        } catch {
          data = { error: `Non-JSON response from backend at ${target}` };
        }

        attempts.push({
          target,
          duration_ms: Date.now() - attemptStart,
          status: response.status,
          ok: response.ok,
          backend_error: typeof data.error === "string" ? data.error : undefined
        });
        httpFailures.push({ target, status: response.status });

        if (response.ok) {
          const responseBody = {
            ...data,
            request_id: requestId
          };
          await appendParseErrorLog({
            request_id: requestId,
            configured_flask_base_url: FLASK_API_URL,
            targets,
            request_meta: requestMeta,
            file_meta: fileMeta,
            total_duration_ms: Date.now() - requestStart,
            attempts,
            network_failures: networkFailures,
            result_status: response.status,
            result_body: { result: "ok" }
          });
          return NextResponse.json(responseBody, { status: response.status });
        }

        lastErrorStatus = response.status;
        lastErrorData = { ...data, _backend_target: target };

        if (response.status !== 404) {
          const responseBody = {
            error: lastErrorData.error || "Failed to parse file",
            details: `Backend target: ${target}`,
            request_id: requestId
          };
          await appendParseErrorLog({
            request_id: requestId,
            configured_flask_base_url: FLASK_API_URL,
            targets,
            request_meta: requestMeta,
            file_meta: fileMeta,
            total_duration_ms: Date.now() - requestStart,
            attempts,
            network_failures: networkFailures,
            result_status: response.status,
            result_body: responseBody
          });
          return NextResponse.json(responseBody, { status: response.status });
        }
      } catch (error) {
        const message = describeFetchError(error);
        attempts.push({
          target,
          duration_ms: Date.now() - attemptStart,
          ok: false,
          error: message
        });
        networkFailures.push({ target, message });
        lastErrorStatus = 503;
      }
    }

    const hasAny404 = httpFailures.some((failure) => failure.status === 404);
    const hasAnyNon404HttpFailure = httpFailures.some((failure) => failure.status !== 404);

    if (lastErrorStatus === 404 || (hasAny404 && !hasAnyNon404HttpFailure)) {
      const route404Targets = httpFailures
        .filter((failure) => failure.status === 404)
        .map((failure) => failure.target);
      const responseBody = {
        error: "Parser backend route not found",
        details: `Connected to backend but parse route was not found (404). 404 targets: ${route404Targets.join(", ")}`,
        hint: "Start Flask with: python app/main.py (port 8000), or set FLASK_API_URL to your backend base URL.",
        request_id: requestId
      };
      await appendParseErrorLog({
        request_id: requestId,
        configured_flask_base_url: FLASK_API_URL,
        targets,
        request_meta: requestMeta,
        file_meta: fileMeta,
        total_duration_ms: Date.now() - requestStart,
        attempts,
        network_failures: networkFailures,
        result_status: 502,
        result_body: responseBody
      });
      return NextResponse.json(responseBody, { status: 502 });
    }

    const responseBody = {
      error:
        typeof lastErrorData.error === "string"
          ? lastErrorData.error
          : "Failed to parse file",
      details: `Could not reach a parse endpoint at ${FLASK_API_URL} with routes: ${targets.join(", ")}`,
      network_failures: networkFailures,
      hint: "Verify Flask is running and reachable: curl -i http://localhost:8000/health",
      request_id: requestId
    };
    await appendParseErrorLog({
      request_id: requestId,
      configured_flask_base_url: FLASK_API_URL,
      targets,
      request_meta: requestMeta,
      file_meta: fileMeta,
      total_duration_ms: Date.now() - requestStart,
      attempts,
      network_failures: networkFailures,
      result_status: 503,
      result_body: responseBody
    });
    return NextResponse.json(responseBody, { status: 503 });
  } catch (error) {
    const responseBody = {
      error: error instanceof Error ? error.message : "Failed to parse file",
      details: "Make sure the Flask backend is running on port 8000",
      request_id: requestId
    };
    await appendParseErrorLog({
      request_id: requestId,
      configured_flask_base_url: FLASK_API_URL,
      targets: [],
      request_meta: requestMeta,
      file_meta: {},
      total_duration_ms: Date.now() - requestStart,
      attempts,
      network_failures: networkFailures,
      result_status: 500,
      result_body: responseBody
    });
    console.error("File parsing proxy error:", error);
    return NextResponse.json(responseBody, { status: 500 });
  }
}
