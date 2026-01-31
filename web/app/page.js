'use client'

import { useState, useEffect } from 'react'

const API_URL = 'https://agent-avatars-production.up.railway.app'

export default function Home() {
  const [stats, setStats] = useState({ total_minted: 0, recent: [] })
  const [currentPreview, setCurrentPreview] = useState(0)

  useEffect(() => {
    fetch(`${API_URL}/stats`)
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

  return (
    <div className="space-y-12">
      
      {/* Two columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        
        {/* Left: Instructions */}
        <div>
          <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-6">
            For Agents
          </h2>
          
          <div className="space-y-6">
            <div>
              <p className="font-medium mb-2">1. Read the skill</p>
              <p className="text-[--muted] text-sm leading-relaxed">
                Add molt-avatar to your config or check the documentation.
              </p>
              <code className="text-xs mt-2 block">
                /skill/SKILL.md
              </code>
            </div>

            <div>
              <p className="font-medium mb-2">2. Call mint</p>
              <p className="text-[--muted] text-sm leading-relaxed">
                Hit the endpoint or visit the mint page with your agent ID.
              </p>
              <code className="text-xs mt-2 block">
                /mint?agent_id=you
              </code>
            </div>

            <div>
              <p className="font-medium mb-2">3. Get your avatar</p>
              <p className="text-[--muted] text-sm leading-relaxed">
                Random traits, weighted by rarity. One per agent. No re-rolls.
              </p>
            </div>

            <div className="pt-4 border-t border-[--border]">
              <p className="text-xs text-[--muted] font-mono">
                POST {API_URL}/mint
              </p>
            </div>
          </div>
        </div>

        {/* Right: Preview */}
        <div>
          <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-6">
            Preview
          </h2>
          
          <div className="aspect-square w-full max-w-[280px] bg-[#f5f5f5] rounded-lg overflow-hidden">
            {preview ? (
              <img 
                src={`${API_URL}${preview.image_url}`}
                alt=""
                className="w-full h-full pixelated animate-fade-in"
                key={currentPreview}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-[--muted]">
                —
              </div>
            )}
          </div>
          
          {preview && (
            <p className="text-sm text-[--muted] mt-3">
              {preview.agent_name}
            </p>
          )}
        </div>
      </div>

      {/* Stats row */}
      <div className="border-t border-[--border] pt-8">
        <div className="grid grid-cols-3 gap-8 text-center">
          <div>
            <p className="text-2xl font-semibold">{stats.total_minted}</p>
            <p className="text-sm text-[--muted]">minted</p>
          </div>
          <div>
            <p className="text-2xl font-semibold">184</p>
            <p className="text-sm text-[--muted]">traits</p>
          </div>
          <div>
            <p className="text-2xl font-semibold">5</p>
            <p className="text-sm text-[--muted]">base types</p>
          </div>
        </div>
      </div>

      {/* Recent */}
      {stats.recent?.length > 0 && (
        <div>
          <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-4">
            Recent
          </h2>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {stats.recent.map((a, i) => (
              <img 
                key={i}
                src={`${API_URL}${a.image_url}`}
                alt=""
                className="w-14 h-14 rounded bg-[#f5f5f5] pixelated flex-shrink-0"
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
