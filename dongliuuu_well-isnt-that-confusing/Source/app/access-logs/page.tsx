import Link from "next/link";
import { Button } from "@/components/ui/button";
import { accessLogs } from "@/lib/access-logs";

export default function AccessLogs() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-gray-900 to-black text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-gray-400 to-blue-300 bg-clip-text text-transparent">
            ACCESS LOGS
          </h1>
          <p className="text-xl text-gray-300 mb-2">
            ASTRA-9 Security Monitoring System
          </p>
          <div className="flex justify-center items-center gap-2 text-blue-400">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
            <span className="text-sm">LOGGING ACTIVE</span>
          </div>
        </div>

        <div className="max-w-6xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur-sm border border-gray-500/30 rounded-lg shadow-2xl overflow-hidden">
            <div className="bg-slate-900/50 p-4 border-b border-gray-500/30">
              <h2 className="text-xl font-semibold text-gray-300">
                Recent Station Activity
              </h2>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-900/30">
                  <tr className="text-left">
                    <th className="p-4 text-gray-400 font-medium">Timestamp</th>
                    <th className="p-4 text-gray-400 font-medium">User</th>
                    <th className="p-4 text-gray-400 font-medium">Location</th>
                    <th className="p-4 text-gray-400 font-medium">Result</th>
                    <th className="p-4 text-gray-400 font-medium">Details</th>
                  </tr>
                </thead>
                <tbody>
                  {accessLogs.map((log, index) => (
                    <tr
                      key={index}
                      className="border-b border-gray-700/30 hover:bg-slate-800/30"
                    >
                      <td className="p-4 text-gray-300 font-mono text-sm">
                        {log.timestamp}
                      </td>
                      <td className="p-4 text-blue-300 font-medium">
                        {log.user}
                      </td>
                      <td className="p-4 text-cyan-300">{log.location}</td>
                      <td className="p-4">
                        <span
                          className={`px-2 py-1 rounded text-xs font-medium ${
                            log.result === "Granted"
                              ? "bg-green-900/30 text-green-400 border border-green-500/30"
                              : "bg-red-900/30 text-red-400 border border-red-500/30"
                          }`}
                        >
                          {log.result}
                        </span>
                      </td>
                      <td className="p-4 text-gray-400 text-sm">
                        {log.reason}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Link href="/docking-bay">
          <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3">
            Return to Docking Bay
          </Button>
        </Link>
      </div>
    </div>
  );
}
