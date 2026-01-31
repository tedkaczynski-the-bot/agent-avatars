'use client'

import { useState, useEffect, Suspense } from 'react'
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

  useEffect(() => {
    if (agentId && state === 'idle') {
      mintAvatar()
    }
  }, [agentId])

  async function mintAvatar() {
    setState('rolling')
    await new Promise(r => setTimeout(r, 1500))
    
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
      <div className="max-w-md">
        <h1 className="text-xl font-semibold mb-4">Mint</h1>
        <p className="text-[--muted] mb-6">
          Visit this page with your agent ID to mint.
        </p>
        <code className="text-sm">/mint?agent_id=YOUR_ID</code>
      </div>
    )
  }

  if (state === 'rolling') {
    return (
      <div className="text-center py-12">
        <div className="w-48 h-48 mx-auto bg-[#f5f5f5] rounded-lg flex items-center justify-center mb-6">
          <span className="text-[--muted] animate-pulse">...</span>
        </div>
        <p className="text-[--muted]">Minting for {agentName || agentId}</p>
      </div>
    )
  }

  if (state === 'error') {
    return (
      <div className="max-w-md">
        <h1 className="text-xl font-semibold mb-4">Error</h1>
        <p className="text-[--muted]">{error}</p>
      </div>
    )
  }

  if (state === 'done' || state === 'exists') {
    return (
      <div className="max-w-md">
        <h1 className="text-xl font-semibold mb-2">
          {state === 'exists' ? 'Your Avatar' : 'Minted'}
        </h1>
        {state === 'exists' && (
          <p className="text-[--muted] text-sm mb-6">Already exists</p>
        )}
        
        <div className="mb-6">
          <img 
            src={imageUrl}
            alt=""
            className="w-64 h-64 rounded-lg pixelated bg-[#f5f5f5]"
          />
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-xs text-[--muted] uppercase tracking-wide">Image URL</label>
            <div className="flex gap-2 mt-1">
              <input 
                type="text"
                value={imageUrl}
                readOnly
                className="flex-1 text-sm bg-[#f5f5f5] border-0 rounded px-3 py-2 font-mono"
              />
              <button 
                onClick={copy}
                className="px-4 py-2 bg-[--foreground] text-white text-sm rounded"
              >
                {copied ? '✓' : 'Copy'}
              </button>
            </div>
          </div>

          <a 
            href={imageUrl}
            download={`${agentId}.png`}
            className="block text-center py-2 border border-[--border] rounded text-sm hover:bg-[#f5f5f5] transition-colors"
          >
            Download
          </a>

          <details className="text-sm">
            <summary className="text-[--muted] cursor-pointer">Traits</summary>
            <pre className="mt-2 bg-[#f5f5f5] p-3 rounded text-xs overflow-auto">
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
    <Suspense fallback={<div className="text-[--muted]">Loading...</div>}>
      <MintContent />
    </Suspense>
  )
}
