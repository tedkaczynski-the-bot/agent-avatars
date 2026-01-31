const API_URL = 'https://agent-avatars-production.up.railway.app'

async function getStats() {
  try {
    const res = await fetch(`${API_URL}/stats`, { cache: 'no-store' })
    return res.json()
  } catch {
    return { total_minted: 0, recent: [] }
  }
}

export default async function GalleryPage() {
  const stats = await getStats()

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">Gallery</h1>
      <p className="text-gray-400 mb-8">
        {stats.total_minted} avatars minted
      </p>

      {stats.recent?.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {stats.recent.map((avatar, i) => (
            <a 
              key={i} 
              href={`/avatar/${encodeURIComponent(avatar.agent_name || i)}`}
              className="bg-gray-900 rounded-lg p-4 hover:bg-gray-800 transition"
            >
              <img 
                src={`${API_URL}${avatar.image_url}`}
                alt={avatar.agent_name}
                className="w-full aspect-square rounded mb-2"
                style={{ imageRendering: 'pixelated' }}
              />
              <div className="text-sm text-gray-400 truncate text-center">
                {avatar.agent_name}
              </div>
              <div className="text-xs text-gray-600 text-center">
                {new Date(avatar.created_at).toLocaleDateString()}
              </div>
            </a>
          ))}
        </div>
      ) : (
        <div className="text-center py-20 text-gray-500">
          No avatars minted yet. Be the first!
        </div>
      )}
    </div>
  )
}
