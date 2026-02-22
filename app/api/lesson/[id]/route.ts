import { NextResponse } from "next/server";

const FLASK_API_URL = process.env.FLASK_API_URL || "http://localhost:8000";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

    const response = await fetch(`${FLASK_API_URL}/api/lesson/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: data.error || "Failed to fetch lesson" },
        { status: response.status }
      );
    }

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Lesson fetch proxy error:", error);
    return NextResponse.json(
      { 
        error: error instanceof Error ? error.message : "Failed to connect to lesson service",
        details: "Make sure the Flask backend is running on port 8000"
      },
      { status: 500 }
    );
  }
}
