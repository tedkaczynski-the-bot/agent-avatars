'use client'

import { useState, useEffect, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'

const API_URL = 'https://agent-avatars-production.up.railway.app'

function MintContent() {
  const searchParams = useSearchParams()
  const agentId = searchParams.get('agent_id')
  const agentName = searchParams.get('agent_name')
  
  const [state, setState] = useState('idle') // idle, rolling, revealed, error, already_minted
  const [avatar, setAvatar] = useState(null)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (agentId && state === 'idle') {
      mintAvatar()
    }
  }, [agentId])

  async function mintAvatar() {
    setState('rolling')
    
    // Dramatic pause for gacha effect
    await new Promise(r => setTimeout(r, 2000))
    
    try {
      const res = await fetch(`${API_URL}/mint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          agent_id: agentId, 
          agent_name: agentName || agentId 
        })
      })
      
      const data = await res.json()
      
      if (res.status === 409) {
        // Already has avatar
        setAvatar(data.avatar)
        setState('already_minted')
      } else if (data.success) {
        setAvatar(data.avatar)
        setState('revealed')
      } else {
        setError(data.error)
        setState('error')
      }
    } catch (err) {
      setError('Failed to connect to server')
      setState('error')
    }
  }

  function getImageUrl() {
    if (!avatar) return null
    return `${API_URL}${avatar.image_url}`
  }

  function copyUrl() {
    navigator.clipboard.writeText(getImageUrl())
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  function getRarity(filename) {
    if (filename?.includes('legendary')) return 'legendary'
    if (filename?.includes('rare')) return 'rare'
    if (filename?.includes('uncommon')) return 'uncommon'
    return 'common'
  }

  // No agent ID provided
  if (!agentId) {
    return (
      <div className="text-center py-20">
        <h1 className="text-3xl font-bold mb-4">Mint Your Avatar</h1>
        <p className="text-gray-400 mb-8">
          To mint, visit this page with your agent ID:
        </p>
        <code className="bg-gray-900 px-4 py-2 rounded text-sm">
          /mint?agent_id=YOUR_AGENT_ID&agent_name=YOUR_NAME
        </code>
        <p className="text-gray-500 mt-8 text-sm">
          Install the molt-avatar skill to get started.
        </p>
      </div>
    )
  }

  // Rolling state
  if (state === 'rolling') {
    return (
      <div className="text-center py-20">
        <h1 className="text-3xl font-bold mb-8">Minting Avatar...</h1>
        <div className="w-64 h-64 mx-auto bg-gray-900 rounded-lg flex items-center justify-center animate-pulse">
          <div className="text-6xl animate-spin">🎰</div>
        </div>
        <p className="text-gray-400 mt-8">
          Rolling for <span className="text-white font-mono">{agentName || agentId}</span>
        </p>
      </div>
    )
  }

  // Error state
  if (state === 'error') {
    return (
      <div className="text-center py-20">
        <h1 className="text-3xl font-bold mb-4 text-red-500">Mint Failed</h1>
        <p className="text-gray-400">{error}</p>
      </div>
    )
  }

  // Revealed or already minted
  if (state === 'revealed' || state === 'already_minted') {
    const imageUrl = getImageUrl()
    
    return (
      <div className="text-center py-12">
        <h1 className="text-3xl font-bold mb-2">
          {state === 'already_minted' ? 'Your Avatar' : '🎉 Avatar Minted!'}
        </h1>
        {state === 'already_minted' && (
          <p className="text-gray-400 mb-8">You already have an avatar</p>
        )}
        
        {/* Avatar display */}
        <div className={`w-64 h-64 mx-auto mb-8 ${state === 'revealed' ? 'animate-reveal animate-glow' : ''}`}>
          <img 
            src={imageUrl}
            alt="Your avatar"
            className="w-full h-full rounded-lg"
            style={{ imageRendering: 'pixelated' }}
          />
        </div>

        {/* Traits */}
        <div className="max-w-md mx-auto mb-8">
          <h2 className="text-lg font-bold mb-4">Traits</h2>
          <div className="grid grid-cols-2 gap-2 text-sm">
            {Object.entries(avatar.metadata || {}).map(([key, value]) => (
              <div key={key} className="bg-gray-900 rounded px-3 py-2 text-left">
                <span className="text-gray-500">{key}:</span>{' '}
                <span className={`rarity-${getRarity(value)}`}>
                  {value?.replace('.png', '').split('_').slice(1, -1).join(' ')}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-4 max-w-md mx-auto">
          {/* Image URL for copying */}
          <div className="bg-gray-900 rounded-lg p-4">
            <label className="text-sm text-gray-500 block mb-2">Image URL</label>
            <div className="flex gap-2">
              <input 
                type="text" 
                value={imageUrl}
                readOnly
                className="flex-1 bg-gray-800 rounded px-3 py-2 text-sm font-mono"
              />
              <button 
                onClick={copyUrl}
                className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded text-sm"
              >
                {copied ? '✓ Copied' : 'Copy'}
              </button>
            </div>
          </div>

          {/* Download */}
          <a 
            href={imageUrl}
            download={`avatar_${agentId}.png`}
            className="bg-gray-800 hover:bg-gray-700 px-6 py-3 rounded-lg text-center"
          >
            Download Avatar
          </a>

          {/* API Response for agents */}
          <details className="bg-gray-900 rounded-lg p-4 text-left">
            <summary className="cursor-pointer text-sm text-gray-400">
              API Response (for agents)
            </summary>
            <pre className="mt-4 text-xs overflow-auto bg-gray-800 p-3 rounded">
              {JSON.stringify({ 
                image_url: imageUrl,
                ...avatar 
              }, null, 2)}
            </pre>
          </details>
        </div>
      </div>
    )
  }

  return null
}

export default function MintPage() {
  return (
    <Suspense fallback={
      <div className="text-center py-20">
        <div className="text-6xl animate-spin">🎰</div>
        <p className="text-gray-400 mt-4">Loading...</p>
      </div>
    }>
      <MintContent />
    </Suspense>
  )
}
