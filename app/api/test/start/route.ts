import { NextResponse } from "next/server";

const FLASK_API_URL = process.env.FLASK_API_URL || "http://localhost:8000";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const response = await fetch(`${FLASK_API_URL}/api/test/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: data.error || "Failed to start test" },
        { status: response.status }
      );
    }

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Test start proxy error:", error);
    return NextResponse.json(
      { 
        error: error instanceof Error ? error.message : "Failed to connect to test service",
        details: "Make sure the Flask backend is running on port 8000"
      },
      { status: 500 }
    );
  }
}
