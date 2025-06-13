import { cookies } from "next/headers";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { decodeJWT } from "@/lib/jwt";
import fs from "fs";

const flag = fs.readFileSync("./flag.txt", "utf-8").trim();

export default async function Bridge() {
  const cookieStore = await cookies();
  const token = cookieStore.get("astral_token");

  let isAuthorised = false;
  let name = "";
  let errorMessage = "";

  if (!token) {
    errorMessage =
      "Unable to identify personnel. Please dock at the station first.";
  } else {
    const decoded = decodeJWT(token.value);

    if (!decoded) {
      errorMessage = "Invalid authorisation token.";
    } else {
      name = decoded.name;

      if (
        decoded.role === "commander" &&
        decoded.name.toLowerCase() === "reinhard"
      ) {
        isAuthorised = true;
      } else if (
        decoded.role === "commander" &&
        decoded.name.toLowerCase() !== "reinhard"
      ) {
        errorMessage = "Unknown commander detected.";
      } else {
        errorMessage = "Commander role required.";
      }
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-purple-900 to-slate-900 text-white">
      <div className="container mx-auto px-4 flex flex-col items-center justify-center min-h-screen">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-300 bg-clip-text text-transparent">
            COMMAND BRIDGE
          </h1>
          <p className="text-xl text-purple-200 mb-2">
            ASTRA-9 Central Command Authority
          </p>
          <div className="flex justify-center items-center gap-2 text-red-400">
            <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
            <span className="text-sm">RESTRICTED ACCESS</span>
          </div>
        </div>

        <div className="max-w-4xl mx-auto">
          {isAuthorised ? (
            <div className="bg-green-900/20 backdrop-blur-sm border border-green-500/50 rounded-lg p-8 mb-6 shadow-2xl">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-green-400 mb-4">
                  ACCESS GRANTED
                </h2>
                <p className="text-xl text-green-300">
                  Welcome to the bridge, Commander {name}.
                </p>
                <p className="text-lg text-green-200 mt-2">
                  You are authorised to perform all actions on the station.
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-6 mt-8">
                <div className="bg-slate-800/50 p-6 rounded-lg border border-green-500/30">
                  <h3 className="text-xl font-semibold text-green-400 mb-4">
                    Station Controls
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span>Life Support Systems</span>
                      <span className="text-green-400">ONLINE</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Orbital Thrusters</span>
                      <span className="text-green-400">NOMINAL</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Communication Array</span>
                      <span className="text-green-400">ACTIVE</span>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-800/50 p-6 rounded-lg border border-green-500/30">
                  <h3 className="text-xl font-semibold text-green-400 mb-4">
                    Override Codes
                  </h3>
                  <div className="space-y-2 font-mono text-sm">
                    <div>Emergency: ALPHA-7-7-DELTA</div>
                    <div>Maintenance: BETA-3-3-GAMMA</div>
                    <div className="text-yellow-400">FLAG: {flag}</div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-red-900/20 backdrop-blur-sm border border-red-500/50 rounded-lg p-8 shadow-2xl mb-6">
              <div className="text-center">
                <h2 className="text-4xl font-bold text-red-400 mb-6">
                  ACCESS DENIED
                </h2>
                <p className="text-xl text-red-300 mb-4">{errorMessage}</p>
                <p className="text-lg text-red-200">
                  This area is restricted to authorised command personnel only.
                </p>
              </div>
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/docking-bay">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3">
                Return to Docking Bay
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
