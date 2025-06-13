import jwt from "jsonwebtoken";
import fs from "fs";
import path from "path";

const privateKeyPath = path.join(process.cwd(), "keys", "private.pem");
const privateKey = fs.readFileSync(privateKeyPath, "utf8");

const publicKeyPath = path.join(process.cwd(), "keys", "public.pem");
const publicKey = fs.readFileSync(publicKeyPath, "utf8");

interface JWTPayload {
  name: string;
  role: string;
}

export function createJWT(name: any, role: string): string {
  return jwt.sign({ name, role }, privateKey, { algorithm: "RS256" });
}

export function decodeJWT(token: string): JWTPayload | undefined {
  try {
    const data = jwt.verify(token, publicKey, {
      algorithms: ["RS256", "HS256"],
    });

    if (typeof data === "object" && "name" in data && "role" in data) {
      return data as JWTPayload;
    }

    throw new Error("Invalid JWT");
  } catch (err: any) {
    return;
  }
}
