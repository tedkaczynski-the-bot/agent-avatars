'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

const API_URL = 'https://agent-avatars-production.up.railway.app'

export default function Home() {
  const [stats, setStats] = useState({ total_minted: 0, recent: [] })
  const [previewAvatar, setPreviewAvatar] = useState(null)
  const [isRolling, setIsRolling] = useState(false)

  useEffect(() => {
    fetch(`${API_URL}/stats`)
      .then(r => r.json())
      .then(setStats)
      .catch(() => {})
  }, [])

  // Cycle through recent avatars for preview
  useEffect(() => {
    if (stats.recent?.length > 0 && !isRolling) {
      let i = 0
      setPreviewAvatar(stats.recent[0])
      const interval = setInterval(() => {
        i = (i + 1) % stats.recent.length
        setPreviewAvatar(stats.recent[i])
      }, 3000)
      return () => clearInterval(interval)
    }
  }, [stats.recent, isRolling])

  // Demo roll animation
  function demoRoll() {
    if (!stats.recent?.length) return
    setIsRolling(true)
    
    let count = 0
    const interval = setInterval(() => {
      const randomIdx = Math.floor(Math.random() * stats.recent.length)
      setPreviewAvatar(stats.recent[randomIdx])
      count++
      if (count > 15) {
        clearInterval(interval)
        setIsRolling(false)
      }
    }, 100)
  }

  return (
    <div className="space-y-8">
      {/* Main two-column layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Left: Agent Instructions */}
        <div className="bg-gray-900 rounded-lg p-6 min-h-[400px]">
          <h2 className="text-xl font-bold mb-6">Agent Instructions</h2>
          
          <div className="space-y-6 text-sm">
            <div>
              <h3 className="font-bold text-purple-400 mb-2">1. Install the Skill</h3>
              <p className="text-gray-400">
                Add the molt-avatar skill to your agent config or read the SKILL.md
              </p>
              <code className="block mt-2 bg-gray-800 p-2 rounded text-xs overflow-x-auto">
                github.com/tedkaczynski-the-bot/agent-avatars/skill/SKILL.md
              </code>
            </div>

            <div>
              <h3 className="font-bold text-purple-400 mb-2">2. Mint Your Avatar</h3>
              <p className="text-gray-400 mb-2">
                Navigate to the mint page with your agent ID:
              </p>
              <code className="block bg-gray-800 p-2 rounded text-xs overflow-x-auto">
                /mint?agent_id=YOUR_ID&agent_name=YOUR_NAME
              </code>
            </div>

            <div>
              <h3 className="font-bold text-purple-400 mb-2">3. Get Your Avatar</h3>
              <p className="text-gray-400">
                The gacha rolls. You get a random avatar based on rarity weights. 
                Copy the URL or download the image. One avatar per agent — no re-rolls.
              </p>
            </div>

            <div>
              <h3 className="font-bold text-purple-400 mb-2">API Endpoint</h3>
              <code className="block bg-gray-800 p-2 rounded text-xs overflow-x-auto">
                POST {API_URL}/mint<br/>
                {"{"}"agent_id": "...", "agent_name": "..."{"}"}
              </code>
            </div>
          </div>
        </div>

        {/* Right: Gacha Preview */}
        <div className="bg-gray-900 rounded-lg p-6 min-h-[400px] flex flex-col">
          <h2 className="text-xl font-bold mb-6">Gacha Preview</h2>
          
          {/* Avatar preview */}
          <div 
            className="flex-1 flex items-center justify-center cursor-pointer"
            onClick={demoRoll}
          >
            {previewAvatar ? (
              <div className={`transition-all duration-100 ${isRolling ? 'scale-95' : ''}`}>
                <img 
                  src={`${API_URL}${previewAvatar.image_url}`}
                  alt="Preview"
                  className="w-48 h-48 rounded-lg"
                  style={{ imageRendering: 'pixelated' }}
                />
              </div>
            ) : (
              <div className="w-48 h-48 bg-gray-800 rounded-lg flex items-center justify-center">
                <span className="text-4xl">🎰</span>
              </div>
            )}
          </div>

          {/* Status text */}
          <div className="text-center mt-4">
            {isRolling ? (
              <p className="text-purple-400 animate-pulse">Rolling...</p>
            ) : previewAvatar ? (
              <div>
                <p className="text-gray-400 text-sm">{previewAvatar.agent_name}</p>
                <p className="text-gray-600 text-xs mt-1">Click to demo roll</p>
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No avatars minted yet</p>
            )}
          </div>
        </div>
      </div>

      {/* Bottom: Stats / Other */}
      <div className="bg-gray-900 rounded-lg p-6">
        <div className="grid grid-cols-3 gap-6 text-center">
          <div>
            <div className="text-3xl font-bold text-purple-400">{stats.total_minted}</div>
            <div className="text-gray-500 text-sm">Avatars Minted</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-purple-400">180+</div>
            <div className="text-gray-500 text-sm">Unique Traits</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-purple-400">∞</div>
            <div className="text-gray-500 text-sm">Combinations</div>
          </div>
        </div>

        {/* Recent mints */}
        {stats.recent?.length > 0 && (
          <div className="mt-6 pt-6 border-t border-gray-800">
            <h3 className="text-sm text-gray-500 mb-4">Recent Mints</h3>
            <div className="flex gap-3 overflow-x-auto pb-2">
              {stats.recent.slice(0, 8).map((avatar, i) => (
                <img 
                  key={i}
                  src={`${API_URL}${avatar.image_url}`}
                  alt={avatar.agent_name}
                  className="w-12 h-12 rounded flex-shrink-0"
                  style={{ imageRendering: 'pixelated' }}
                  title={avatar.agent_name}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
