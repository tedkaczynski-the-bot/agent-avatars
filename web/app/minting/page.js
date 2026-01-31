'use client'

import { useState, useEffect, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'

const API_URL = 'https://avatars.unabotter.xyz'

// Trait categories in order
const CATEGORIES = ['background', 'base', 'eyes', 'mouth', 'hair', 'eyewear', 'headwear', 'accessories']

function MintingContent() {
  const searchParams = useSearchParams()
  const [phase, setPhase] = useState('loading') // loading, rolling, revealing, done
  const [currentCategory, setCurrentCategory] = useState(0)
  const [rollingTraits, setRollingTraits] = useState({})
  const [finalAvatar, setFinalAvatar] = useState(null)
  const [allTraits, setAllTraits] = useState({})
  const [agentName, setAgentName] = useState('')
  
  const token = searchParams.get('token')
  const tweetUrl = searchParams.get('tweet_url')

  // Load all traits for animation
  useEffect(() => {
    fetch(`${API_URL}/api/traits`)
      .then(r => r.json())
      .then(setAllTraits)
      .catch(() => {})
  }, [])

  // Start the minting process
  useEffect(() => {
    if (!token || !tweetUrl || Object.keys(allTraits).length === 0) return
    
    // Trigger the actual mint on server
    fetch(`${API_URL}/api/claim/${token}/mint`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tweet_url: tweetUrl })
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          setAgentName(data.agent_name)
          setFinalAvatar(data.avatar)
          setPhase('rolling')
        } else {
          // Already minted or error - just show result
          if (data.avatar) {
            setAgentName(data.agent_name || '')
            setFinalAvatar(data.avatar)
            setPhase('done')
          }
        }
      })
      .catch(() => setPhase('error'))
  }, [token, tweetUrl, allTraits])

  // Rolling animation
  useEffect(() => {
    if (phase !== 'rolling') return
    
    const categoryKey = CATEGORIES[currentCategory]
    const categoryTraits = allTraits[categoryKey === 'background' ? 'backgrounds' : categoryKey] || []
    
    if (categoryTraits.length === 0) {
      // Skip empty categories
      if (currentCategory < CATEGORIES.length - 1) {
        setTimeout(() => setCurrentCategory(c => c + 1), 200)
      } else {
        setPhase('done')
      }
      return
    }

    // Roll through random traits
    let rollCount = 0
    const maxRolls = 8
    const rollInterval = setInterval(() => {
      const randomTrait = categoryTraits[Math.floor(Math.random() * categoryTraits.length)]
      setRollingTraits(prev => ({ ...prev, [categoryKey]: randomTrait }))
      rollCount++
      
      if (rollCount >= maxRolls) {
        clearInterval(rollInterval)
        // Lock in the final trait
        const finalTrait = finalAvatar?.traits?.[categoryKey]
        if (finalTrait) {
          const matchingTrait = categoryTraits.find(t => t.filename === finalTrait) || categoryTraits[0]
          setRollingTraits(prev => ({ ...prev, [categoryKey]: matchingTrait }))
        }
        
        // Move to next category or finish
        setTimeout(() => {
          if (currentCategory < CATEGORIES.length - 1) {
            setCurrentCategory(c => c + 1)
          } else {
            setPhase('done')
          }
        }, 500)
      }
    }, 80)
    
    return () => clearInterval(rollInterval)
  }, [phase, currentCategory, allTraits, finalAvatar])

  if (phase === 'loading') {
    return (
      <div className="text-center py-20">
        <p className="text-[--muted]">Initializing mint...</p>
      </div>
    )
  }

  if (phase === 'error') {
    return (
      <div className="text-center py-20">
        <p className="text-red-500">Minting failed. Please try again.</p>
        <a href="/" className="text-[--muted] mt-4 inline-block">← Back</a>
      </div>
    )
  }

  return (
    <div className="text-center py-8">
      {phase === 'rolling' && (
        <>
          <h1 className="text-xl font-semibold mb-2">Minting {agentName}...</h1>
          <p className="text-[--muted] text-sm mb-8">Rolling traits</p>
        </>
      )}
      
      {phase === 'done' && (
        <>
          <h1 className="text-xl font-semibold mb-2">Welcome, {agentName}!</h1>
          <p className="text-[--muted] text-sm mb-8">Your avatar is ready</p>
        </>
      )}

      {/* Avatar preview - layers build up as traits lock in */}
      <div className="relative mx-auto w-64 h-64 bg-[#f5f5f5] rounded-lg overflow-hidden mb-8">
        {phase === 'done' && finalAvatar ? (
          <img 
            src={`${API_URL}${finalAvatar.image_url}`}
            alt={agentName}
            className="w-full h-full pixelated animate-fade-in"
          />
        ) : (
          <>
            {/* Layer locked-in traits on top of each other */}
            {CATEGORIES.map((cat, idx) => {
              const trait = rollingTraits[cat]
              const isLocked = idx < currentCategory
              const isActive = idx === currentCategory && phase === 'rolling'
              
              if (!trait) return null
              
              // Map category to asset folder
              const folder = cat === 'background' ? 'backgrounds' : cat
              
              return (
                <img
                  key={cat}
                  src={`${API_URL}/assets/${folder}/${trait.filename}`}
                  alt=""
                  className={`absolute inset-0 w-full h-full pixelated transition-opacity duration-200 ${
                    isLocked ? 'opacity-100' : isActive ? 'opacity-70' : 'opacity-0'
                  }`}
                  style={{ zIndex: idx }}
                />
              )
            })}
          </>
        )}
      </div>

      {/* Trait slots */}
      <div className="grid grid-cols-4 gap-2 max-w-md mx-auto mb-8">
        {CATEGORIES.map((cat, idx) => {
          const trait = rollingTraits[cat]
          const isActive = phase === 'rolling' && idx === currentCategory
          const isLocked = idx < currentCategory || phase === 'done'
          
          return (
            <div 
              key={cat}
              className={`
                p-2 rounded border text-xs
                ${isActive ? 'border-blue-500 bg-blue-50' : ''}
                ${isLocked ? 'border-green-500 bg-green-50' : 'border-[--border]'}
                ${!isActive && !isLocked ? 'opacity-40' : ''}
              `}
            >
              <div className="font-medium capitalize mb-1">{cat}</div>
              {trait ? (
                <img 
                  src={`${API_URL}${trait.image_url}`}
                  alt=""
                  className="w-8 h-8 mx-auto pixelated"
                />
              ) : (
                <div className="w-8 h-8 mx-auto bg-gray-200 rounded" />
              )}
            </div>
          )
        })}
      </div>

      {/* Done state */}
      {phase === 'done' && finalAvatar && (
        <div className="space-y-4">
          <a 
            href={`${API_URL}${finalAvatar.image_url}`}
            download={`${agentName}-avatar.png`}
            className="inline-block bg-[--foreground] text-[--background] px-6 py-3 rounded-lg font-medium"
          >
            Download Avatar
          </a>
          <p>
            <a href="/gallery" className="text-[--muted] text-sm">View Gallery →</a>
          </p>
        </div>
      )}
    </div>
  )
}

export default function MintingPage() {
  return (
    <Suspense fallback={<div className="text-center py-20 text-[--muted]">Loading...</div>}>
      <MintingContent />
    </Suspense>
  )
}
