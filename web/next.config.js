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
  async rewrites() {
    return [
      {
        source: '/skill.md',
        destination: 'https://agent-avatars-production.up.railway.app/skill.md',
      },
      {
        source: '/heartbeat.md',
        destination: 'https://agent-avatars-production.up.railway.app/heartbeat.md',
      },
      {
        source: '/skill.json',
        destination: 'https://agent-avatars-production.up.railway.app/skill.json',
      },
      {
        source: '/api/:path*',
        destination: 'https://agent-avatars-production.up.railway.app/api/:path*',
      },
      {
        source: '/claim/:token',
        destination: 'https://agent-avatars-production.up.railway.app/claim/:token',
      },
      {
        source: '/claim/:token/verify',
        destination: 'https://agent-avatars-production.up.railway.app/claim/:token/verify',
      },
      {
        source: '/images/:path*',
        destination: 'https://agent-avatars-production.up.railway.app/images/:path*',
      },
      {
        source: '/assets/:path*',
        destination: 'https://agent-avatars-production.up.railway.app/assets/:path*',
      },
    ]
  },
}

module.exports = nextConfig
