const jose = require("node-jose");
const fs = require("fs");
const path = require("path");

const publicKeyPath = path.resolve(__dirname, "../keys/public.pem");
const jwksDir = path.resolve(__dirname, "../public/.well-known");
const jwksPath = path.join(jwksDir, "jwks.json");

const pubKey = fs.readFileSync(publicKeyPath, "utf8");

jose.JWK.asKey(pubKey, "pem").then(function (key) {
  const jwk = key.toJSON();

  const jwks = {
    keys: [jwk],
  };

  fs.mkdirSync(jwksDir, { recursive: true });
  fs.writeFileSync(jwksPath, JSON.stringify(jwks, null, 2));
});
