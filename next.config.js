/** @type {import('next').NextConfig} */
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
        destination: `${BACKEND_URL}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
