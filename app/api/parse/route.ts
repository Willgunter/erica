import { NextResponse } from "next/server";

const FLASK_API_URL = process.env.FLASK_API_URL || "http://localhost:8000";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    
    const response = await fetch(`${FLASK_API_URL}/api/parse`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: data.error || "Failed to parse file" },
        { status: response.status }
      );
    }

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("File parsing proxy error:", error);
    return NextResponse.json(
      { 
        error: error instanceof Error ? error.message : "Failed to parse file",
        details: "Make sure the Flask backend is running on port 8000"
      },
      { status: 500 }
    );
  }
}
