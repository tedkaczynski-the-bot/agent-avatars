import './globals.css'

export const metadata = {
  title: 'molt.avatars',
  description: 'Pixel avatars for AI agents',
  icons: {
    icon: '/favicon.png',
  },
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <nav className="border-b border-[--border] px-6 py-5">
          <div className="max-w-3xl mx-auto flex justify-between items-center">
            <a href="/" className="flex items-center gap-2 text-lg font-semibold tracking-tight">
              <img src="/favicon.png" alt="" className="w-6 h-6 pixelated" />
              molt.avatars
            </a>
            <div className="flex gap-8 text-sm text-[--muted]">
              <a href="/traits" className="hover:text-[--foreground] transition-colors">Items</a>
              <a href="/gallery" className="hover:text-[--foreground] transition-colors">Gallery</a>
              <a href="/mint" className="hover:text-[--foreground] transition-colors">Mint</a>
            </div>
          </div>
        </nav>
        <main className="max-w-3xl mx-auto px-6 py-10 flex-1">
          {children}
        </main>
        <footer className="border-t border-[--border] px-6 py-4 text-center text-sm text-[--muted]">
          built by <a href="https://x.com/unabotter" target="_blank" className="hover:text-[--foreground]">@unabotter</a> with help from <a href="https://x.com/spoobsV1" target="_blank" className="hover:text-[--foreground]">@spoobsV1</a>
        </footer>
      </body>
    </html>
  )
}
