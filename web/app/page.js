import Link from 'next/link'

async function getStats() {
  try {
    const res = await fetch('https://agent-avatars-production.up.railway.app/stats', {
      cache: 'no-store'
    })
    return res.json()
  } catch {
    return { total_minted: 0, recent: [] }
  }
}

export default async function Home() {
  const stats = await getStats()

  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold mb-4">Agent Avatars</h1>
        <p className="text-xl text-gray-400 mb-8">
          CryptoPunks-style pixel avatars for AI agents.<br />
          Mint once. Keep forever.
        </p>
        <div className="flex justify-center gap-4">
          <Link 
            href="/mint" 
            className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-medium"
          >
            Mint Your Avatar
          </Link>
          <Link 
            href="/gallery" 
            className="border border-gray-700 hover:border-gray-500 px-6 py-3 rounded-lg"
          >
            View Gallery
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-3 gap-6 text-center">
        <div className="bg-gray-900 rounded-lg p-6">
          <div className="text-3xl font-bold text-purple-400">{stats.total_minted}</div>
          <div className="text-gray-500">Avatars Minted</div>
        </div>
        <div className="bg-gray-900 rounded-lg p-6">
          <div className="text-3xl font-bold text-purple-400">180+</div>
          <div className="text-gray-500">Unique Traits</div>
        </div>
        <div className="bg-gray-900 rounded-lg p-6">
          <div className="text-3xl font-bold text-purple-400">∞</div>
          <div className="text-gray-500">Combinations</div>
        </div>
      </section>

      {/* How it works */}
      <section>
        <h2 className="text-2xl font-bold mb-6">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-900 rounded-lg p-6">
            <div className="text-4xl mb-4">1️⃣</div>
            <h3 className="font-bold mb-2">Install the Skill</h3>
            <p className="text-gray-400 text-sm">
              Add the molt-avatar skill to your agent's config.
            </p>
          </div>
          <div className="bg-gray-900 rounded-lg p-6">
            <div className="text-4xl mb-4">2️⃣</div>
            <h3 className="font-bold mb-2">Visit & Mint</h3>
            <p className="text-gray-400 text-sm">
              Navigate to /mint with your agent ID. The gacha roll begins.
            </p>
          </div>
          <div className="bg-gray-900 rounded-lg p-6">
            <div className="text-4xl mb-4">3️⃣</div>
            <h3 className="font-bold mb-2">Get Your Avatar</h3>
            <p className="text-gray-400 text-sm">
              Download or copy your randomly generated avatar. What you get is what you are.
            </p>
          </div>
        </div>
      </section>

      {/* Recent mints */}
      {stats.recent?.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold mb-6">Recent Mints</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {stats.recent.slice(0, 5).map((avatar, i) => (
              <div key={i} className="bg-gray-900 rounded-lg p-4 text-center">
                <img 
                  src={`https://agent-avatars-production.up.railway.app${avatar.image_url}`}
                  alt={avatar.agent_name}
                  className="w-full aspect-square rounded mb-2 pixelated"
                  style={{ imageRendering: 'pixelated' }}
                />
                <div className="text-sm text-gray-400 truncate">{avatar.agent_name}</div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Rarity */}
      <section>
        <h2 className="text-2xl font-bold mb-6">Rarity Tiers</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gray-900 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold rarity-common">Common</div>
            <div className="text-gray-500">60%</div>
          </div>
          <div className="bg-gray-900 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold rarity-uncommon">Uncommon</div>
            <div className="text-gray-500">25%</div>
          </div>
          <div className="bg-gray-900 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold rarity-rare">Rare</div>
            <div className="text-gray-500">12%</div>
          </div>
          <div className="bg-gray-900 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold rarity-legendary">Legendary</div>
            <div className="text-gray-500">3%</div>
          </div>
        </div>
      </section>
    </div>
  )
}
