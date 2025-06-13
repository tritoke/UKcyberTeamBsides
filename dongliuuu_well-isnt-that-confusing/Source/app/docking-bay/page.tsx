import { DockingInterface } from "@/components/docking-interface";
import { cookies } from "next/headers";
import { decodeJWT } from "@/lib/jwt";

export default async function DockingBay() {
  const cookieStore = await cookies();
  const token = cookieStore.get("astral_token");

  let currentCrewData;
  if (token) {
    const decoded = decodeJWT(token.value);
    if (decoded) {
      currentCrewData = {
        name: decoded.name,
        role: decoded.role,
      };
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-blue-900 to-black text-white">
      <div className="container mx-auto px-4 flex flex-col items-center justify-center min-h-screen">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
            ASTRA-9 ORBITAL STATION
          </h1>
          <p className="text-xl text-blue-200 mb-2">
            Autonomous Docking Bay Alpha-7
          </p>
          <div className="flex justify-center items-center gap-2 text-green-400">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm">SYSTEM ONLINE</span>
          </div>
        </div>

        <div className="max-w-2xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/30 rounded-lg p-8 shadow-2xl">
            <h2 className="text-2xl font-semibold mb-6 text-center text-cyan-300">
              CREW AUTHORISATION TERMINAL
            </h2>

            <DockingInterface currentCrewData={currentCrewData} />
          </div>
        </div>

        <div className="mt-12 text-center">
          <div className="inline-block bg-slate-800/30 border border-yellow-500/30 rounded-lg p-4">
            <p className="text-yellow-300 text-sm">
              ⚠️ SECURITY NOTICE: All crew movements are logged and monitored
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
