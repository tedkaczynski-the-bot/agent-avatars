const TRAITS = {
  backgrounds: {
    name: 'Backgrounds',
    count: 18,
    examples: ['cream', 'blue', 'pink', 'green', 'purple', 'coral', 'mint', 'lavender'],
    rarity: 'All common (equal chance)'
  },
  base: {
    name: 'Base Types',
    count: 21,
    examples: ['Male (9 skin tones)', 'Female (9 skin tones)', 'Zombie', 'Ape', 'Alien'],
    rarity: 'Human common, Zombie/Ape rare, Alien legendary'
  },
  eyes: {
    name: 'Eyes',
    count: 19,
    examples: ['Basic', 'Blue', 'Green', 'Angry', 'Wide', 'Narrow', 'Laser', 'Heart', 'Robot'],
    rarity: 'Mixed - laser, heart, robot are rare'
  },
  hair: {
    name: 'Hair',
    count: 50,
    examples: ['Short', 'Long', 'Mohawk', 'Afro', 'Ponytail', 'Pigtails', 'Spiky', 'Bald'],
    rarity: 'Most common, colored mohawks rare'
  },
  eyewear: {
    name: 'Eyewear',
    count: 10,
    examples: ['Glasses', 'Sunglasses', 'Aviators', '3D Glasses', 'VR Headset', 'Eye Patch'],
    rarity: '70% chance of none, VR/monocle rare'
  },
  headwear: {
    name: 'Headwear',
    count: 21,
    examples: ['Cap', 'Beanie', 'Crown', 'Halo', 'Devil Horns', 'Cowboy Hat', 'Headphones'],
    rarity: '60% chance of none, crown/halo rare'
  },
  mouth: {
    name: 'Mouth',
    count: 16,
    examples: ['Smile', 'Frown', 'Neutral', 'Cigarette', 'Pipe', 'Fangs', 'Gold Teeth'],
    rarity: '20% chance of none, fangs/gold rare'
  },
  accessories: {
    name: 'Accessories',
    count: 29,
    examples: ['Earrings', 'Nose Ring', 'Freckles', 'Scar', 'Face Tattoo', 'Clown Nose'],
    rarity: '50% chance of none, tattoos rare'
  }
}

export default function TraitsPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">Traits</h1>
      <p className="text-gray-400 mb-8">
        All possible traits your avatar can have
      </p>

      <div className="space-y-6">
        {Object.entries(TRAITS).map(([key, trait]) => (
          <div key={key} className="bg-gray-900 rounded-lg p-6">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-xl font-bold">{trait.name}</h2>
              <span className="bg-gray-800 px-3 py-1 rounded text-sm">
                {trait.count} variants
              </span>
            </div>
            
            <div className="flex flex-wrap gap-2 mb-4">
              {trait.examples.map((ex, i) => (
                <span key={i} className="bg-gray-800 px-3 py-1 rounded text-sm text-gray-300">
                  {ex}
                </span>
              ))}
            </div>

            <p className="text-sm text-gray-500">
              <span className="text-gray-400">Rarity:</span> {trait.rarity}
            </p>
          </div>
        ))}
      </div>

      {/* Rarity explanation */}
      <div className="mt-12 bg-gray-900 rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">How Rarity Works</h2>
        <p className="text-gray-400 mb-4">
          Each trait category rolls independently. Weights determine how likely each trait is:
        </p>
        <div className="grid grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold rarity-common">60%</div>
            <div className="text-sm text-gray-500">Common</div>
          </div>
          <div>
            <div className="text-2xl font-bold rarity-uncommon">25%</div>
            <div className="text-sm text-gray-500">Uncommon</div>
          </div>
          <div>
            <div className="text-2xl font-bold rarity-rare">12%</div>
            <div className="text-sm text-gray-500">Rare</div>
          </div>
          <div>
            <div className="text-2xl font-bold rarity-legendary">3%</div>
            <div className="text-sm text-gray-500">Legendary</div>
          </div>
        </div>
        <p className="text-gray-500 text-sm mt-4">
          Some categories (eyewear, headwear, accessories) have a chance of being empty.
        </p>
      </div>
    </div>
  )
}
