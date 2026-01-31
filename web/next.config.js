/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'agent-avatars-production.up.railway.app',
      },
    ],
  },
}

module.exports = nextConfig
