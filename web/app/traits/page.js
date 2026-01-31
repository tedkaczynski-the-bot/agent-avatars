'use client'

import { useState, useEffect } from 'react'

const API_URL = 'https://avatars.unabotter.xyz'

const RARITY_COLORS = {
  common: 'bg-gray-100 text-gray-600',
  uncommon: 'bg-green-100 text-green-700',
  rare: 'bg-blue-100 text-blue-700',
  legendary: 'bg-purple-100 text-purple-700',
}

const CATEGORY_ORDER = ['backgrounds', 'base', 'eyes', 'mouth', 'hair', 'eyewear', 'headwear', 'accessories']

export default function TraitsPage() {
  const [traits, setTraits] = useState({})
  const [loading, setLoading] = useState(true)
  const [hoveredTrait, setHoveredTrait] = useState(null)

  useEffect(() => {
    fetch(`${API_URL}/api/traits`)
      .then(r => r.json())
      .then(data => {
        setTraits(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="text-[--muted]">Loading traits...</div>
  }

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-xl font-semibold mb-2">Items</h1>
        <p className="text-[--muted] text-sm mb-6">Hover over items to see rarity</p>
        
        {/* Rarity legend */}
        <div className="flex gap-4 mb-8 text-xs">
          {Object.entries(RARITY_COLORS).map(([rarity, classes]) => (
            <span key={rarity} className={`px-2 py-1 rounded ${classes}`}>
              {rarity}
            </span>
          ))}
        </div>
      </div>

      {CATEGORY_ORDER.map(category => {
        const items = traits[category]
        if (!items?.length) return null
        
        return (
          <div key={category}>
            <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-4">
              {category} <span className="text-xs">({items.length})</span>
            </h2>
            <div className="flex flex-wrap gap-3">
              {items.map((item, i) => (
                <div 
                  key={i}
                  className="relative group"
                  onMouseEnter={() => setHoveredTrait(item)}
                  onMouseLeave={() => setHoveredTrait(null)}
                >
                  <div className={`w-12 h-12 rounded-lg overflow-hidden border-2 transition-all ${
                    item.rarity === 'legendary' ? 'border-purple-400' :
                    item.rarity === 'rare' ? 'border-blue-400' :
                    item.rarity === 'uncommon' ? 'border-green-400' :
                    'border-gray-200'
                  } hover:scale-110 hover:shadow-lg`}>
                    <img 
                      src={`${API_URL}${item.image_url}`}
                      alt={item.name}
                      className="w-full h-full pixelated bg-[#f5f5f5]"
                    />
                  </div>
                  
                  {/* Tooltip on hover */}
                  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 rounded text-xs whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10 bg-black text-white">
                    <span className="font-medium">{item.name}</span>
                    <span className={`ml-2 px-1 rounded ${RARITY_COLORS[item.rarity]}`}>
                      {item.rarity}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}
