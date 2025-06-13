import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col justify-center bg-gradient-to-b from-black via-red-900 to-slate-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-red-900/20 backdrop-blur-sm border border-red-500/50 rounded-lg p-8 shadow-2xl">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-red-400 mb-4">
                NAVIGATION ERROR
              </h2>
              <p className="text-xl text-red-300 mb-4">
                Sector not found in ASTRA-9 station map
              </p>
              <p className="text-lg text-red-200 mb-6">
                The requested coordinates do not exist in our orbital navigation
                database.
              </p>
            </div>

            <div className="bg-slate-800/50 p-6 rounded-lg border border-red-500/30 mb-8">
              <h3 className="text-xl font-semibold text-red-400 mb-4">
                ⚠️ SYSTEM STATUS
              </h3>
              <div className="space-y-3 font-mono text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Navigation Array:</span>
                  <span className="text-red-400">ERROR</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Sector Mapping:</span>
                  <span className="text-yellow-400">RECALIBRATING</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Emergency Protocols:</span>
                  <span className="text-green-400">ACTIVE</span>
                </div>
              </div>
            </div>

            <div className="text-center space-y-4">
              <p className="text-gray-300 mb-6">
                Please return to a known sector or contact station control for
                assistance.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/docking-bay">
                  <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3">
                    Return to Docking Bay
                  </Button>
                </Link>
              </div>
            </div>
          </div>

          <div className="mt-8 text-center">
            <div className="inline-block bg-slate-800/30 border border-yellow-500/30 rounded-lg p-4">
              <p className="text-yellow-300 text-sm">
                Lost crew members often find their way by exploring known
                sectors first.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
