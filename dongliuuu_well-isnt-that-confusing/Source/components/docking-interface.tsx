"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Image from "next/image";

interface DockingInterfaceProps {
  currentCrewData?: {
    name: string;
    role: string;
  };
}

export function DockingInterface({ currentCrewData }: DockingInterfaceProps) {
  const [name, setName] = useState("");
  const [status, setStatus] = useState<
    "idle" | "processing" | "granted" | "denied"
  >("idle");
  const [message, setMessage] = useState("");
  const [showPortrait, setShowPortrait] = useState(false);

  useEffect(() => {
    if (currentCrewData) {
      setName(currentCrewData.name);
      setStatus("granted");
      setMessage(
        `Docking granted. Welcome aboard ASTRA-9, ${currentCrewData.name}.`
      );
      setShowPortrait(true);
    }
  }, []);

  const handleDockingRequest = async () => {
    setStatus("processing");
    setMessage("Scanning crew manifest...");

    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 1500));

    try {
      const response = await fetch("/api/auth/dock", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name }),
      });

      const data = await response.json();

      if (data.success) {
        setStatus("granted");
        setMessage(`Docking granted. Welcome aboard ASTRA-9, ${name}.`);
        setShowPortrait(true);
      } else {
        setStatus("denied");
        setMessage(
          data.message || "Access denied. Name not found in crew manifest."
        );
        setShowPortrait(false);
      }
    } catch (error) {
      console.log("FAILED", error);
      setStatus("denied");
      setMessage("System error. Please contact station administrator.");
      setShowPortrait(false);
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case "processing":
        return "text-yellow-400";
      case "granted":
        return "text-green-400";
      case "denied":
        return "text-red-400";
      default:
        return "text-blue-300";
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <div>
          <Label
            htmlFor="crew-name"
            className="text-cyan-300 text-sm font-medium"
          >
            CREW MEMBER IDENTIFICATION
          </Label>
          <Input
            id="crew-name"
            type="text"
            placeholder="Enter your registered name..."
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-2 bg-slate-900/50 border-blue-500/50 text-white placeholder-slate-400 focus:border-cyan-400"
            disabled={status === "processing"}
          />
        </div>

        <Button
          onClick={handleDockingRequest}
          disabled={!name.trim() || status === "processing"}
          className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold py-3"
        >
          {status === "processing" ? (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              PROCESSING...
            </div>
          ) : (
            "REQUEST DOCKING CLEARANCE"
          )}
        </Button>
      </div>

      {message && (
        <div
          className={`p-4 rounded-lg border ${
            status === "granted"
              ? "bg-green-900/20 border-green-500/50"
              : status === "denied"
              ? "bg-red-900/20 border-red-500/50"
              : "bg-yellow-900/20 border-yellow-500/50"
          }`}
        >
          <p className={`font-medium ${getStatusColor()}`}>{message}</p>
        </div>
      )}

      {showPortrait && (
        <div className="text-center space-y-4 p-6 bg-slate-900/30 rounded-lg border border-cyan-500/30">
          <Image
            src="/commander_portrait.png?height=200&width=200"
            alt="Portrait of Commander Reinhard"
            width={200}
            height={200}
            className="mx-auto rounded-lg border-2 border-gold-400"
          />
          <p className="text-gold-400 italic text-sm">
            Portrait of a well-known Commander
          </p>
        </div>
      )}
    </div>
  );
}
