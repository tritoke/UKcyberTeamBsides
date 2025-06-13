const fs = require("fs");
const path = require("path");
const forge = require("node-forge");

const { pki } = forge;

const keypair = pki.rsa.generateKeyPair({ bits: 2048, e: 0x10001 });

const privatePem = pki.privateKeyToPem(keypair.privateKey);
const publicPem = pki.publicKeyToPem(keypair.publicKey);

const keysDir = path.resolve(__dirname, "../keys");
const privateKeyPath = path.join(keysDir, "private.pem");
const publicKeyPath = path.join(keysDir, "public.pem");

fs.mkdirSync(keysDir, { recursive: true });

fs.writeFileSync(privateKeyPath, privatePem);
fs.writeFileSync(publicKeyPath, publicPem);
