import { NextResponse } from "next/server";
import { promises as fs } from "node:fs";
import path from "node:path";

export const runtime = "nodejs";

const VIDEO_RELATIVE_PATH = path.join(".vscode", "QuadraticFormulaLesson.mp4");
const VIDEO_CONTENT_TYPE = "video/mp4";

function buildHeaders(
  size: number,
  start: number,
  end: number,
  partial: boolean,
): HeadersInit {
  const headers: HeadersInit = {
    "Content-Type": VIDEO_CONTENT_TYPE,
    "Accept-Ranges": "bytes",
    "Cache-Control": "private, max-age=0, must-revalidate",
    "Content-Length": String(end - start + 1),
  };

  if (partial) {
    headers["Content-Range"] = `bytes ${start}-${end}/${size}`;
  }

  return headers;
}

export async function GET(request: Request) {
  try {
    const videoPath = path.resolve(process.cwd(), VIDEO_RELATIVE_PATH);
    const stat = await fs.stat(videoPath);
    const fullBuffer = await fs.readFile(videoPath);
    const size = stat.size;
    const rangeHeader = request.headers.get("range");

    if (!rangeHeader) {
      return new NextResponse(fullBuffer, {
        status: 200,
        headers: buildHeaders(size, 0, size - 1, false),
      });
    }

    const match = /^bytes=(\d*)-(\d*)$/.exec(rangeHeader.trim());
    if (!match) {
      return new NextResponse("Invalid range header", {
        status: 416,
        headers: { "Content-Range": `bytes */${size}` },
      });
    }

    const startStr = match[1];
    const endStr = match[2];
    let start = startStr ? Number(startStr) : 0;
    let end = endStr ? Number(endStr) : size - 1;

    if (!Number.isFinite(start) || !Number.isFinite(end)) {
      return new NextResponse("Invalid range values", {
        status: 416,
        headers: { "Content-Range": `bytes */${size}` },
      });
    }

    if (startStr === "" && endStr !== "") {
      const suffixLength = Number(endStr);
      start = Math.max(size - suffixLength, 0);
      end = size - 1;
    }

    if (start < 0 || end < 0 || start > end || start >= size) {
      return new NextResponse("Range not satisfiable", {
        status: 416,
        headers: { "Content-Range": `bytes */${size}` },
      });
    }

    end = Math.min(end, size - 1);
    const chunk = fullBuffer.subarray(start, end + 1);
    return new NextResponse(chunk, {
      status: 206,
      headers: buildHeaders(size, start, end, true),
    });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") {
      return NextResponse.json({ error: "Quadratic lesson video not found." }, { status: 404 });
    }
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to stream watch video." },
      { status: 500 },
    );
  }
}
