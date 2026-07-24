# Writing Intelligence v3.1 REST runtime. tsx is the runtime (no compile step).
# BUILD CONTEXT MUST BE THE REPO ROOT so agents/ + schemas/ are available:
#   docker build -f services/api/Dockerfile --build-arg WI_GIT_SHA=$(git rev-parse --short HEAD) -t wi-api .
FROM node:20-slim

ARG WI_GIT_SHA=dev
ENV WI_GIT_SHA=$WI_GIT_SHA
ENV WI_REPO_ROOT=/app
ENV NODE_ENV=production
ENV PORT=4090

WORKDIR /app/services/api

# Install deps first for layer caching. tsx + typescript stay in dependencies (runtime needs tsx).
COPY services/api/package.json services/api/package-lock.json* ./
RUN npm install --omit=dev --no-audit --no-fund

# App source.
COPY services/api/tsconfig.json ./
COPY services/api/src ./src

# Doctrine assets the manifest + schema routes read at runtime (resolved via WI_REPO_ROOT).
COPY agents /app/agents
COPY schemas /app/schemas

EXPOSE 4090

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:'+ (process.env.PORT||4090) +'/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["npx", "tsx", "src/server.ts"]
