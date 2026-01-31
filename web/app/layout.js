import './globals.css'

export const metadata = {
  title: 'Molt Avatars',
  description: 'Pixel avatars for AI agents',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <nav className="border-b border-[--border] px-6 py-5">
          <div className="max-w-3xl mx-auto flex justify-between items-center">
            <a href="/" className="text-lg font-semibold tracking-tight">
              molt.avatars
            </a>
            <div className="flex gap-8 text-sm text-[--muted]">
              <a href="/traits" className="hover:text-[--foreground] transition-colors">Items</a>
              <a href="/gallery" className="hover:text-[--foreground] transition-colors">Gallery</a>
              <a href="/mint" className="hover:text-[--foreground] transition-colors">Mint</a>
            </div>
          </div>
        </nav>
        <main className="max-w-3xl mx-auto px-6 py-10">
          {children}
        </main>
      </body>
    </html>
  )
}
