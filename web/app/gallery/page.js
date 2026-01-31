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
            <div key={i} className="group">
              <div className="aspect-square bg-[#f5f5f5] rounded-lg overflow-hidden">
                <img 
                  src={`${API_URL}${avatar.image_url}`}
                  alt=""
                  className="w-full h-full pixelated"
                />
              </div>
              <p className="text-xs text-[--muted] mt-2 truncate">
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
