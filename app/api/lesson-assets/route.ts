import { NextResponse } from "next/server";
import { promises as fs } from "node:fs";
import path from "node:path";

function getMimeType(filePath: string): string {
  const extension = path.extname(filePath).toLowerCase();
  switch (extension) {
    case ".mp4":
      return "video/mp4";
    case ".mp3":
      return "audio/mpeg";
    case ".json":
      return "application/json";
    case ".txt":
      return "text/plain";
    case ".css":
      return "text/css";
    case ".js":
      return "text/javascript";
    default:
      return "application/octet-stream";
  }
}

function isAllowedStorageUrl(storageUrl: string): boolean {
  return storageUrl.startsWith("local://");
}

export async function GET(request: Request) {
  try {
    const url = new URL(request.url);
    const storageUrl = url.searchParams.get("storage_url") || url.searchParams.get("url");

    if (!storageUrl) {
      return NextResponse.json(
        { error: "storage_url is required (for example: local://renders/lesson-.../module-... .mp4)" },
        { status: 400 }
      );
    }

    if (!isAllowedStorageUrl(storageUrl)) {
      return NextResponse.json(
        {
          error: "Only local storage URLs are supported in the local asset proxy.",
          storage_url: storageUrl,
        },
        { status: 400 }
      );
    }

    const relativePath = storageUrl.replace("local://", "");
    const projectRoot = process.cwd();
    const baseDir = path.join(projectRoot, "app", "object_storage");
    const candidatePath = path.isAbsolute(relativePath)
      ? path.resolve(relativePath)
      : path.resolve(baseDir, relativePath);
    const safePrefix = path.resolve(baseDir) + path.sep;

    if (!candidatePath.startsWith(safePrefix)) {
      return NextResponse.json(
        { error: "Requested local path is outside the allowed directory." },
        { status: 403 }
      );
    }

    const contents = await fs.readFile(candidatePath);
    return new NextResponse(contents, {
      status: 200,
      headers: {
        "Content-Type": getMimeType(candidatePath),
        "Cache-Control": "private, max-age=0",
      },
    });
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") {
      return NextResponse.json({ error: "Asset not found." }, { status: 404 });
    }

    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : "Failed to load asset."
      },
      { status: 500 }
    );
  }
}
