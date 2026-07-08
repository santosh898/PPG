/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV === "development";
// In local dev, proxy to the uvicorn backend (override with BACKEND_URL). In
// production (Vercel), `/api/*` is served by the co-located Python serverless
// function at `api/index.py`.
const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000";

const nextConfig = {
  reactStrictMode: true,
  // MP chat is a multi-step LLM call that can take ~25s+; the rewrite proxy
  // otherwise hard-caps proxied requests at 30s and resets the socket.
  experimental: {
    proxyTimeout: 1000 * 120,
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: isDev ? `${BACKEND_URL}/api/:path*` : "/api/index",
      },
    ];
  },
};

module.exports = nextConfig;
