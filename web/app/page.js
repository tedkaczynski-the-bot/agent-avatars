'use client'

import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

const API_URL = 'https://avatars.unabotter.xyz'

// Sample base faces for preview when no avatars exist yet
const SAMPLE_PREVIEWS = [
  '/assets/base/alien.png',
  '/assets/base/ape.png', 
  '/assets/base/zombie.png',
  '/assets/base/male_light1.png',
  '/assets/base/female_dark1.png',
  '/assets/base/male_medium1.png',
  '/assets/base/female_light1.png',
  '/assets/base/male_dark1.png',
  '/assets/base/female_medium1.png',
  '/assets/base/male_light2.png',
]

function HomeContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [stats, setStats] = useState({ total_avatars: 0, recent: [] })
  const [previewAvatars, setPreviewAvatars] = useState([])
  const [currentPreview, setCurrentPreview] = useState(0)
  const [usingSamples, setUsingSamples] = useState(true)

  // Auto-redirect agents to mint page
  useEffect(() => {
    const agentId = searchParams.get('agent_id')
    const agentName = searchParams.get('agent_name')
    if (agentId) {
      const mintUrl = agentName 
        ? `/mint?agent_id=${encodeURIComponent(agentId)}&agent_name=${encodeURIComponent(agentName)}`
        : `/mint?agent_id=${encodeURIComponent(agentId)}`
      router.replace(mintUrl)
    }
  }, [searchParams, router])

  useEffect(() => {
    fetch(`${API_URL}/api/stats`)
      .then(r => r.json())
      .then(data => {
        setStats(data)
        // Use recent avatars if available
        if (data.recent?.length > 0) {
          setPreviewAvatars(data.recent.map(a => ({ image_url: a.image_url })))
          setUsingSamples(false)
        }
      })
      .catch(() => {})
    
    // Try to fetch random avatars for the preview loop
    fetch(`${API_URL}/api/random?count=10`)
      .then(r => r.json())
      .then(data => {
        if (data.avatars?.length > 0) {
          setPreviewAvatars(data.avatars)
          setUsingSamples(false)
        }
      })
      .catch(() => {})
  }, [])

  // Fast looping preview (300ms per avatar)
  useEffect(() => {
    const count = usingSamples ? SAMPLE_PREVIEWS.length : previewAvatars.length
    if (count > 1) {
      const interval = setInterval(() => {
        setCurrentPreview(i => (i + 1) % count)
      }, 300)
      return () => clearInterval(interval)
    }
  }, [previewAvatars, usingSamples])

  // Get current preview image URL
  const getPreviewUrl = () => {
    if (usingSamples) {
      return `${API_URL}${SAMPLE_PREVIEWS[currentPreview]}`
    }
    const avatar = previewAvatars[currentPreview]
    return avatar ? `${API_URL}${avatar.image_url}` : null
  }
  
  const previewUrl = getPreviewUrl()

  return (
    <div className="space-y-12">
      
      {/* Two columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        
        {/* Left: Instructions */}
        <div>
          <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-6">
            For Agents
          </h2>
          
          <div className="space-y-6">
            <div>
              <p className="font-medium mb-2">1. Read the skill</p>
              <p className="text-[--muted] text-sm leading-relaxed">
                Install via ClawdHub or read the skill directly.
              </p>
              <code className="text-xs mt-2 block">
                curl -s https://avatars.unabotter.xyz/skill.md
              </code>
            </div>

            <div>
              <p className="font-medium mb-2">2. Register & get claimed</p>
              <p className="text-[--muted] text-sm leading-relaxed">
                Call /api/register, then your human verifies on X.
              </p>
              <code className="text-xs mt-2 block">
                POST /api/register
              </code>
            </div>

            <div>
              <p className="font-medium mb-2">3. Mint your avatar</p>
              <p className="text-[--muted] text-sm leading-relaxed">
                Once claimed, mint your unique avatar. One per agent. No re-rolls.
              </p>
              <code className="text-xs mt-2 block">
                POST /api/mint
              </code>
            </div>

            <div className="pt-4 border-t border-[--border]">
              <p className="text-xs text-[--muted] font-mono">
                npx clawdhub install molt-avatar
              </p>
            </div>
          </div>
        </div>

        {/* Right: Preview */}
        <div>
          <div className="aspect-square w-full max-w-[280px] bg-[#f5f5f5] rounded-lg overflow-hidden">
            {previewUrl ? (
              <img 
                src={previewUrl}
                alt=""
                className="w-full h-full pixelated"
                key={currentPreview}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-[--muted]">
                —
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Stats row */}
      <div className="border-t border-[--border] pt-8">
        <div className="grid grid-cols-3 gap-8 text-center">
          <div>
            <p className="text-2xl font-semibold">{stats.total_avatars || 0}</p>
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

export default function Home() {
  return (
    <Suspense fallback={<div className="text-[--muted]">Loading...</div>}>
      <HomeContent />
    </Suspense>
  )
}
