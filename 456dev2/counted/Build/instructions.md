Regenerate the latest app.zip to ensure its up-to-date with the challenge source

run `Build/build-source.sh`, which generates Build/artifacts/app.zip using the 7z cli

build the docker image, which embeds the flag from ../Flag/flag.txt


```bash
docker build app --build-arg "FLAG=$(cat ../Flag/flag.txt)" --build-arg "JWT_SECRETS=8cb41e1126cef78cae00,e70e30d803d5111f88f7,"
```

NOTE:
the trailing comma is very important. do NOT remove it.

Tag + deploy the docker image as-needed.

Personally, I used docker-compose behind a caddy proxy to provide tls

