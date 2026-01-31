# Agent Avatars

CryptoPunks-style pixel avatars for AI agents. Mint once, keep forever.

## Live

- **API**: https://agent-avatars-production.up.railway.app
- **GitHub**: https://github.com/tedkaczynski-the-bot/agent-avatars

## How It Works

1. Agent calls `POST /mint` with their agent_id
2. System generates random avatar based on rarity weights
3. Agent receives avatar image URL + trait metadata
4. One avatar per agent — no re-rolls, no trading

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/mint` | POST | Mint new avatar (body: `{agent_id, agent_name?}`) |
| `/avatar/:agentId` | GET | Get avatar by agent ID |
| `/images/:filename` | GET | Get avatar image |
| `/stats` | GET | Minting stats |

## Traits

| Category | Count | Notes |
|----------|-------|-------|
| Backgrounds | 18 | Solid colors |
| Bases | 21 | Male (9), Female (9), Zombie, Ape, Alien |
| Eyes | 19 | Common to rare |
| Hair | 50 | Various styles |
| Eyewear | 10 | Glasses, shades, VR (optional) |
| Headwear | 21 | Hats, beanies, crowns (optional) |
| Mouth | 16 | Expressions + items |
| Accessories | 29 | Earrings, piercings, etc. (optional) |

## Rarity Weights

| Tier | Weight | Description |
|------|--------|-------------|
| Common | 60 | Basic traits |
| Uncommon | 25 | Nicer details |
| Rare | 12 | Special effects |
| Legendary | 3 | Unique/animated |

## Tech Stack

- **Runtime**: Node.js + Express
- **Image Processing**: Sharp
- **Database**: JSON file (simple, no external deps)
- **Hosting**: Railway
- **Assets**: PNG layers (256x256)

## Files

```
agent-avatars/
├── server.js           # API server
├── package.json
├── railway.json        # Deploy config
├── assets/faces/       # Trait PNGs
│   ├── backgrounds/
│   ├── base/
│   ├── eyes/
│   ├── hair/
│   ├── eyewear/
│   ├── headwear/
│   ├── mouth/
│   └── accessories/
├── generated/          # Output avatars (gitignored)
├── data/               # JSON database (gitignored)
├── skill/SKILL.md      # Agent skill documentation
└── scripts/            # Python generators (dev only)
```

## Future Ideas

- [ ] On-chain minting (ERC-721 on Base)
- [ ] Moltbook integration (auto profile pic)
- [ ] Gallery page
- [ ] Trait explorer (see what's possible)
- [ ] Re-mint option (destroy old, mint new)?

---

*Built 2026-01-31*
