const API_URL = 'https://avatars.unabotter.xyz'

async function getStats() {
  try {
    const res = await fetch(`${API_URL}/api/stats`, { cache: 'no-store' })
    return res.json()
  } catch {
    return { total_avatars: 0, recent: [] }
  }
}

export default async function GalleryPage() {
  const stats = await getStats()

  return (
    <div>
      <h1 className="text-xl font-semibold mb-2">Gallery</h1>
      <p className="text-[--muted] text-sm mb-8">{stats.total_avatars || 0} avatars</p>

      {stats.recent?.length > 0 ? (
        <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-4">
          {stats.recent.map((avatar, i) => (
            <div key={i} className="group text-center">
              <div className="aspect-square bg-[#f5f5f5] rounded-lg overflow-hidden relative">
                <img 
                  src={`${API_URL}${avatar.image_url}`}
                  alt={avatar.name}
                  className="w-full h-full pixelated"
                />
                {avatar.rarity_score && (
                  <div className={`absolute top-1 right-1 text-xs px-1.5 py-0.5 rounded font-medium ${
                    avatar.rarity_score >= 30 ? 'bg-purple-500 text-white' :
                    avatar.rarity_score >= 15 ? 'bg-blue-500 text-white' :
                    avatar.rarity_score >= 8 ? 'bg-green-500 text-white' :
                    'bg-gray-200 text-gray-600'
                  }`}>
                    {avatar.rarity_score}
                  </div>
                )}
              </div>
              <p className="text-sm font-medium mt-2 truncate">
                {avatar.name}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-[--muted]">No avatars yet.</p>
      )}
    </div>
  )
}
