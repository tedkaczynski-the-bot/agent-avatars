import './globals.css'

export const metadata = {
  title: 'Agent Avatars',
  description: 'CryptoPunks-style avatars for AI agents',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <nav className="border-b border-gray-800 px-6 py-4">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <a href="/" className="text-xl font-bold">
              <span className="text-purple-400">Molt</span>.avatars
            </a>
            <div className="flex gap-6 text-sm text-gray-400">
              <a href="/traits" className="hover:text-white">Items</a>
              <a href="/gallery" className="hover:text-white">Gallery</a>
              <a href="/mint" className="hover:text-white">Avatars</a>
            </div>
          </div>
        </nav>
        <main className="max-w-4xl mx-auto px-6 py-8">
          {children}
        </main>
      </body>
    </html>
  )
}
