FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN mkdir -p keys public/.well-known
RUN node setup/gen_rsa.js
RUN node setup/gen_jwk.js
RUN echo "FLAG{w3ll_th47s_c0nfus1n9}" > flag.txt
RUN chmod 644 flag.txt
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/keys ./keys
COPY --from=builder /app/flag.txt ./flag.txt

EXPOSE 3000
CMD ["npm", "run", "start"]
