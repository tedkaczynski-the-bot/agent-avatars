const TRAITS = [
  { name: 'Backgrounds', count: 18, note: 'Solid colors' },
  { name: 'Base', count: 21, note: 'Male, Female, Zombie, Ape, Alien' },
  { name: 'Eyes', count: 19, note: 'Basic to laser' },
  { name: 'Hair', count: 50, note: 'Various styles' },
  { name: 'Eyewear', count: 10, note: 'Optional, 30% chance' },
  { name: 'Headwear', count: 21, note: 'Optional, 40% chance' },
  { name: 'Mouth', count: 16, note: 'Expressions + items' },
  { name: 'Accessories', count: 29, note: 'Optional, 50% chance' },
]

const RARITY = [
  { tier: 'Common', weight: '60%' },
  { tier: 'Uncommon', weight: '25%' },
  { tier: 'Rare', weight: '12%' },
  { tier: 'Legendary', weight: '3%' },
]

export default function TraitsPage() {
  return (
    <div className="space-y-12">
      <div>
        <h1 className="text-xl font-semibold mb-2">Items</h1>
        <p className="text-[--muted] text-sm mb-8">All possible traits</p>

        <div className="space-y-3">
          {TRAITS.map((t, i) => (
            <div 
              key={i} 
              className="flex justify-between items-center py-3 border-b border-[--border]"
            >
              <div>
                <p className="font-medium">{t.name}</p>
                <p className="text-sm text-[--muted]">{t.note}</p>
              </div>
              <p className="text-sm text-[--muted]">{t.count}</p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-sm font-medium text-[--muted] uppercase tracking-wide mb-4">
          Rarity Weights
        </h2>
        <div className="grid grid-cols-4 gap-4">
          {RARITY.map((r, i) => (
            <div key={i} className="text-center">
              <p className="text-lg font-semibold">{r.weight}</p>
              <p className="text-xs text-[--muted]">{r.tier}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
