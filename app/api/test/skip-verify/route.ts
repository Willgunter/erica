import { NextResponse } from "next/server";

type RequestBody = {
  code?: unknown;
};

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as RequestBody;
    const submittedCode = typeof body.code === "string" ? body.code.trim() : "";
    if (!submittedCode) {
      return NextResponse.json(
        { ok: false, error: "Confirmation code is required." },
        { status: 400 }
      );
    }

    const configuredCode = process.env.DEMO_SKIP_CODE?.trim();
    if (!configuredCode) {
      return NextResponse.json(
        {
          ok: false,
          error: "Demo skip code is not configured on the server."
        },
        { status: 503 }
      );
    }

    if (submittedCode !== configuredCode) {
      return NextResponse.json(
        { ok: false, error: "Invalid demo confirmation code." },
        { status: 401 }
      );
    }

    return NextResponse.json({ ok: true }, { status: 200 });
  } catch {
    return NextResponse.json(
      { ok: false, error: "Invalid request body." },
      { status: 400 }
    );
  }
}
