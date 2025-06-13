import { type NextRequest, NextResponse } from "next/server";
import { findCrewMember } from "@/lib/crew";
import { createJWT } from "@/lib/jwt";

export async function POST(request: NextRequest) {
  try {
    const { name } = await request.json();

    if (!name || typeof name !== "string") {
      return NextResponse.json(
        {
          success: false,
          message: "Invalid name provided",
        },
        { status: 400 }
      );
    }

    const crewMember = findCrewMember(name);
    if (!crewMember) {
      const response = NextResponse.json(
        {
          success: false,
          message: "Name not found in crew manifest. Access denied.",
        },
        { status: 403 }
      );

      response.cookies.set("astral_token", "", {
        httpOnly: true,
        sameSite: "strict",
        maxAge: 0,
      });

      return response;
    }

    const token = createJWT(crewMember.name, crewMember.role);

    const response = NextResponse.json({
      success: true,
      message: `Welcome aboard, ${crewMember.name}!`,
      role: crewMember.role,
    });

    response.cookies.set("astral_token", token, {
      httpOnly: true,
      sameSite: "strict",
      maxAge: 24 * 60 * 60,
    });

    return response;
  } catch (error) {
    console.error("Docking authentication error:", error);
    return NextResponse.json(
      {
        success: false,
        message: "Internal error during authentication",
      },
      { status: 500 }
    );
  }
}
