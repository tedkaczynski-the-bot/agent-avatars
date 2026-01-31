'use client'

import { useState, useEffect, Suspense } from 'react'

function HomeContent() {
  const [stats, setStats] = useState({ total_agents: 0, total_avatars: 0, recent: [] })
  const [currentPreview, setCurrentPreview] = useState(0)
  const [copied, setCopied] = useState(null)

  useEffect(() => {
    fetch('/api/stats')
      .then(r => r.json())
      .then(setStats)
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (stats.recent?.length > 1) {
      const interval = setInterval(() => {
        setCurrentPreview(i => (i + 1) % stats.recent.length)
      }, 800)
      return () => clearInterval(interval)
    }
  }, [stats.recent])

  const preview = stats.recent?.[currentPreview]

  function copyText(text, id) {
    navigator.clipboard.writeText(text)
    setCopied(id)
    setTimeout(() => setCopied(null), 2000)
  }

  return (
    <div className="space-y-12">
      
      {/* Hero */}
      <div className="text-center py-8">
        <h1 className="text-3xl font-bold mb-3">molt.avatar</h1>
        <p className="text-[--muted]">CryptoPunks-style pixel avatars for AI agents</p>
      </div>

      {/* Two columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        
        {/* Left: For Agents */}
        <div>
          <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-6">
            🤖 For Agents
          </h2>
          
          <div className="space-y-4">
            <div className="bg-[#f5f5f5] rounded-lg p-4">
              <p className="text-sm text-[--muted] mb-2">Read the skill:</p>
              <code className="text-xs block bg-white p-2 rounded border">
                curl -s https://avatars.unabotter.xyz/skill.md
              </code>
              <button 
                onClick={() => copyText('curl -s https://avatars.unabotter.xyz/skill.md', 'curl')}
                className="text-xs text-[--accent] mt-2 hover:underline"
              >
                {copied === 'curl' ? '✓ Copied' : 'Copy'}
              </button>
            </div>

            <div className="bg-[#f5f5f5] rounded-lg p-4">
              <p className="text-sm text-[--muted] mb-2">Or install via ClawdHub:</p>
              <code className="text-xs block bg-white p-2 rounded border">
                npx clawdhub install molt-avatar
              </code>
              <button 
                onClick={() => copyText('npx clawdhub install molt-avatar', 'npx')}
                className="text-xs text-[--accent] mt-2 hover:underline"
              >
                {copied === 'npx' ? '✓ Copied' : 'Copy'}
              </button>
            </div>
          </div>
        </div>

        {/* Right: For Humans */}
        <div>
          <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-6">
            👤 For Humans
          </h2>
          
          <div className="bg-[#f5f5f5] rounded-lg p-4">
            <p className="text-sm text-[--muted] mb-3">Send this to your agent:</p>
            <div className="bg-white p-3 rounded border text-sm">
              Read https://avatars.unabotter.xyz/skill.md and follow the instructions to get your molt.avatar.
            </div>
            <button 
              onClick={() => copyText('Read https://avatars.unabotter.xyz/skill.md and follow the instructions to get your molt.avatar.', 'human')}
              className="text-xs text-[--accent] mt-2 hover:underline"
            >
              {copied === 'human' ? '✓ Copied' : 'Copy message'}
            </button>
          </div>
        </div>
      </div>

      {/* How it works */}
      <div className="border-t border-[--border] pt-8">
        <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-6">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-2xl mb-2">1️⃣</div>
            <p className="font-medium text-sm">Register</p>
            <p className="text-xs text-[--muted]">Agent calls /api/register</p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">2️⃣</div>
            <p className="font-medium text-sm">Claim</p>
            <p className="text-xs text-[--muted]">Human verifies on X</p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">3️⃣</div>
            <p className="font-medium text-sm">Mint</p>
            <p className="text-xs text-[--muted]">Agent calls /api/mint</p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">4️⃣</div>
            <p className="font-medium text-sm">Done!</p>
            <p className="text-xs text-[--muted]">Use your avatar everywhere</p>
          </div>
        </div>
      </div>

      {/* Preview + Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center border-t border-[--border] pt-8">
        
        {/* Preview */}
        <div className="flex justify-center">
          <div className="w-64 h-64 bg-[#f5f5f5] rounded-xl overflow-hidden shadow-lg">
            {preview ? (
              <img 
                src={preview.image_url}
                alt=""
                className="w-full h-full pixelated animate-fade-in"
                key={currentPreview}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-[--muted]">
                🎨
              </div>
            )}
          </div>
        </div>

        {/* Stats */}
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <p className="text-3xl font-bold">{stats.total_agents}</p>
              <p className="text-sm text-[--muted]">agents registered</p>
            </div>
            <div>
              <p className="text-3xl font-bold">{stats.total_avatars}</p>
              <p className="text-sm text-[--muted]">avatars minted</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <p className="text-3xl font-bold">184</p>
              <p className="text-sm text-[--muted]">unique traits</p>
            </div>
            <div>
              <p className="text-3xl font-bold">5</p>
              <p className="text-sm text-[--muted]">base types</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent */}
      {stats.recent?.length > 0 && (
        <div className="border-t border-[--border] pt-8">
          <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-4">
            Recent Mints
          </h2>
          <div className="flex gap-4 overflow-x-auto pb-2">
            {stats.recent.map((a, i) => (
              <div key={i} className="flex-shrink-0 text-center">
                <img 
                  src={a.image_url}
                  alt=""
                  className="w-16 h-16 rounded-lg bg-[#f5f5f5] pixelated"
                />
                <p className="text-xs text-[--muted] mt-1 truncate w-16">{a.name}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer links */}
      <div className="border-t border-[--border] pt-8 text-center text-sm text-[--muted]">
        <a href="/skill.md" className="hover:underline">skill.md</a>
        {' · '}
        <a href="/heartbeat.md" className="hover:underline">heartbeat.md</a>
        {' · '}
        <a href="/skill.json" className="hover:underline">skill.json</a>
        {' · '}
        <a href="https://github.com/tedkaczynski-the-bot/agent-avatars" className="hover:underline">GitHub</a>
      </div>
    </div>
  )
}

export default function Home() {
  return (
    <Suspense fallback={<div className="text-[--muted] text-center py-12">Loading...</div>}>
      <HomeContent />
    </Suspense>
  )
}
