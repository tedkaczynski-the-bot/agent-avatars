'use client'

import { useState, useEffect, Suspense, useRef } from 'react'
import { useSearchParams } from 'next/navigation'

const API_URL = 'https://agent-avatars-production.up.railway.app'

function MintContent() {
  const searchParams = useSearchParams()
  const agentId = searchParams.get('agent_id')
  const agentName = searchParams.get('agent_name')
  
  const [state, setState] = useState('idle')
  const [avatar, setAvatar] = useState(null)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)
  const [rollImages, setRollImages] = useState([])
  const [currentRollIndex, setCurrentRollIndex] = useState(0)
  const rollIntervalRef = useRef(null)

  // Fetch existing avatars for the gacha roll animation
  useEffect(() => {
    fetch(`${API_URL}/stats`)
      .then(r => r.json())
      .then(data => {
        if (data.recent?.length > 0) {
          setRollImages(data.recent.map(a => `${API_URL}${a.image_url}`))
        }
      })
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (agentId && state === 'idle') {
      mintAvatar()
    }
  }, [agentId])

  // Gacha roll animation
  useEffect(() => {
    if (state === 'rolling' && rollImages.length > 0) {
      let speed = 50
      let slowdowns = 0
      
      const roll = () => {
        setCurrentRollIndex(i => (i + 1) % rollImages.length)
        slowdowns++
        
        // Gradually slow down
        if (slowdowns > 20) speed = 80
        if (slowdowns > 30) speed = 120
        if (slowdowns > 38) speed = 180
        if (slowdowns > 44) speed = 280
        
        if (slowdowns < 50) {
          rollIntervalRef.current = setTimeout(roll, speed)
        }
      }
      
      rollIntervalRef.current = setTimeout(roll, speed)
      
      return () => {
        if (rollIntervalRef.current) clearTimeout(rollIntervalRef.current)
      }
    }
  }, [state, rollImages])

  async function mintAvatar() {
    setState('rolling')
    
    // Let the gacha animation run
    await new Promise(r => setTimeout(r, 3000))
    
    try {
      const res = await fetch(`${API_URL}/mint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent_id: agentId, agent_name: agentName || agentId })
      })
      
      const data = await res.json()
      
      if (res.status === 409) {
        setAvatar(data.avatar)
        setState('exists')
      } else if (data.success) {
        setAvatar(data.avatar)
        setState('done')
      } else {
        setError(data.error)
        setState('error')
      }
    } catch {
      setError('Connection failed')
      setState('error')
    }
  }

  const imageUrl = avatar ? `${API_URL}${avatar.image_url}` : null

  function copy() {
    navigator.clipboard.writeText(imageUrl)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (!agentId) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <h1 className="text-2xl font-semibold mb-4">Mint Your Avatar</h1>
        <p className="text-[--muted] mb-6 max-w-sm">
          Visit this page with your agent ID to mint a unique avatar.
        </p>
        <code className="text-sm bg-[#f5f5f5] px-4 py-2 rounded">/mint?agent_id=YOUR_ID</code>
      </div>
    )
  }

  if (state === 'rolling') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <div className="relative">
          {/* Glow effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 via-pink-500/20 to-purple-500/20 blur-xl rounded-full scale-110 animate-pulse" />
          
          {/* Rolling avatar container */}
          <div className="relative w-64 h-64 bg-[#f5f5f5] rounded-2xl overflow-hidden border-4 border-[--foreground] shadow-2xl">
            {rollImages.length > 0 ? (
              <img 
                src={rollImages[currentRollIndex]}
                alt=""
                className="w-full h-full pixelated transition-none"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-[--foreground] border-t-transparent rounded-full animate-spin" />
              </div>
            )}
          </div>
        </div>
        
        <div className="mt-8 space-y-2">
          <p className="text-lg font-medium animate-pulse">Rolling...</p>
          <p className="text-[--muted] text-sm">{agentName || agentId}</p>
        </div>
      </div>
    )
  }

  if (state === 'error') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <h1 className="text-2xl font-semibold mb-4">Error</h1>
        <p className="text-[--muted]">{error}</p>
      </div>
    )
  }

  if (state === 'done' || state === 'exists') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <h1 className="text-2xl font-semibold mb-2">
          {state === 'exists' ? 'Your Avatar' : '🎉 Minted!'}
        </h1>
        {state === 'exists' && (
          <p className="text-[--muted] text-sm mb-6">Already exists</p>
        )}
        {state === 'done' && (
          <p className="text-[--muted] text-sm mb-6">Your unique avatar is ready</p>
        )}
        
        <div className="mb-8">
          <div className="relative">
            {state === 'done' && (
              <div className="absolute inset-0 bg-gradient-to-r from-green-500/20 via-emerald-500/20 to-green-500/20 blur-xl rounded-full scale-110" />
            )}
            <img 
              src={imageUrl}
              alt=""
              className={`relative w-64 h-64 rounded-2xl pixelated bg-[#f5f5f5] shadow-xl ${state === 'done' ? 'animate-bounce-in' : ''}`}
            />
          </div>
        </div>

        <div className="w-full max-w-md space-y-4">
          <div>
            <label className="text-xs text-[--muted] uppercase tracking-wide">Image URL</label>
            <div className="flex gap-2 mt-1">
              <input 
                type="text"
                value={imageUrl}
                readOnly
                className="flex-1 text-sm bg-[#f5f5f5] border-0 rounded px-3 py-2 font-mono text-center"
              />
              <button 
                onClick={copy}
                className="px-4 py-2 bg-[--foreground] text-white text-sm rounded hover:opacity-80 transition-opacity"
              >
                {copied ? '✓' : 'Copy'}
              </button>
            </div>
          </div>

          <a 
            href={imageUrl}
            download={`${agentId}.png`}
            className="block text-center py-3 border border-[--border] rounded-lg text-sm hover:bg-[#f5f5f5] transition-colors font-medium"
          >
            Download PNG
          </a>

          <details className="text-sm text-left">
            <summary className="text-[--muted] cursor-pointer text-center">View Traits</summary>
            <pre className="mt-2 bg-[#f5f5f5] p-4 rounded-lg text-xs overflow-auto">
{JSON.stringify(avatar.metadata, null, 2)}
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
      <div className="flex items-center justify-center min-h-[60vh] text-[--muted]">
        Loading...
      </div>
    }>
      <MintContent />
    </Suspense>
  )
}
