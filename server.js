import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pg from 'pg';

const { Pool } = pg;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ASSETS_DIR = path.join(__dirname, 'assets', 'faces');
const GENERATED_DIR = path.join(__dirname, 'generated');

// Ensure directories exist
fs.mkdirSync(GENERATED_DIR, { recursive: true });

// PostgreSQL connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.DATABASE_URL?.includes('localhost') ? false : { rejectUnauthorized: false }
});

// Initialize database table
async function initDB() {
  const client = await pool.connect();
  try {
    await client.query(`
      CREATE TABLE IF NOT EXISTS avatars (
        id UUID PRIMARY KEY,
        agent_id VARCHAR(255) UNIQUE NOT NULL,
        agent_name VARCHAR(255),
        moltbook_id VARCHAR(255),
        filename VARCHAR(255) NOT NULL,
        traits JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('Database initialized');
  } finally {
    client.release();
  }
}

const app = express();
app.use(express.json());

// CORS for browser access
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

// Serve generated images
app.use('/images', express.static(GENERATED_DIR));

// Serve SKILL.md
app.get('/skill', (req, res) => {
  const skillPath = path.join(__dirname, 'skill', 'SKILL.md');
  if (fs.existsSync(skillPath)) {
    res.type('text/markdown').send(fs.readFileSync(skillPath, 'utf8'));
  } else {
    res.status(404).send('Skill not found');
  }
});

// Rarity weights
const RARITY_WEIGHTS = {
  common: 60,
  uncommon: 25,
  rare: 12,
  legendary: 3,
};

// Get traits from a category folder
function getTraits(category) {
  const dir = path.join(ASSETS_DIR, category);
  if (!fs.existsSync(dir)) return [];
  
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.png'))
    .map(filename => {
      const parts = filename.replace('.png', '').split('_');
      const rarity = RARITY_WEIGHTS[parts[parts.length - 1]] ? parts[parts.length - 1] : 'common';
      return {
        filename,
        rarity,
        weight: RARITY_WEIGHTS[rarity] || 60
      };
    });
}

// Weighted random choice
function weightedChoice(traits, noneChance = 0) {
  if (!traits.length) return null;
  if (noneChance > 0 && Math.random() * 100 < noneChance) return null;
  
  const totalWeight = traits.reduce((sum, t) => sum + t.weight, 0);
  let random = Math.random() * totalWeight;
  
  for (const trait of traits) {
    random -= trait.weight;
    if (random <= 0) return trait;
  }
  return traits[traits.length - 1];
}

// Generate random avatar
async function generateAvatar(agentId) {
  const bases = getTraits('base');
  const eyes = getTraits('eyes');
  const hair = getTraits('hair');
  const eyewear = getTraits('eyewear');
  const headwear = getTraits('headwear');
  const mouth = getTraits('mouth');
  const accessories = getTraits('accessories');
  const backgrounds = getTraits('backgrounds');
  
  // Pick traits
  const base = weightedChoice(bases);
  const bg = weightedChoice(backgrounds);
  
  const traits = {
    background: bg?.filename || 'solid_cream_common.png',
    base: base?.filename,
    eyes: weightedChoice(eyes)?.filename,
    mouth: weightedChoice(mouth, 20)?.filename,
    hair: weightedChoice(hair, 10)?.filename,
    eyewear: weightedChoice(eyewear, 70)?.filename,
    headwear: weightedChoice(headwear, 60)?.filename,
    accessories: weightedChoice(accessories, 50)?.filename,
  };
  
  // Composite image using sharp
  const SIZE = 256;
  let composite = sharp(path.join(ASSETS_DIR, 'backgrounds', traits.background))
    .resize(SIZE, SIZE);
  
  const layers = [];
  const layerOrder = ['base', 'eyes', 'mouth', 'accessories', 'hair', 'eyewear', 'headwear'];
  
  for (const layer of layerOrder) {
    if (traits[layer]) {
      const layerPath = path.join(ASSETS_DIR, layer, traits[layer]);
      if (fs.existsSync(layerPath)) {
        layers.push({ input: layerPath, top: 0, left: 0 });
      }
    }
  }
  
  if (layers.length > 0) {
    composite = composite.composite(layers);
  }
  
  const avatarId = uuidv4();
  const filename = `avatar_${avatarId}.png`;
  const outputPath = path.join(GENERATED_DIR, filename);
  
  await composite.png().toFile(outputPath);
  
  return {
    id: avatarId,
    filename,
    traits: Object.fromEntries(
      Object.entries(traits).filter(([_, v]) => v != null)
    )
  };
}

// API Routes

app.get('/', (req, res) => {
  res.json({ 
    service: 'agent-avatars',
    status: 'ok',
    endpoints: {
      'POST /mint': 'Mint a new random avatar (body: {agent_id, agent_name?})',
      'GET /avatar/:agentId': 'Get avatar by agent ID',
      'GET /images/:filename': 'Get avatar image',
      'GET /stats': 'Get minting stats'
    }
  });
});

// Mint new avatar
app.post('/mint', async (req, res) => {
  try {
    const { agent_id, agent_name, moltbook_id } = req.body;
    
    if (!agent_id) {
      return res.status(400).json({ error: 'agent_id required' });
    }
    
    // Check if agent already has an avatar
    const existing = await pool.query(
      'SELECT * FROM avatars WHERE agent_id = $1',
      [agent_id]
    );
    
    if (existing.rows.length > 0) {
      const avatar = existing.rows[0];
      return res.status(409).json({ 
        error: 'Agent already has an avatar',
        avatar: {
          id: avatar.id,
          image_url: `/images/${avatar.filename}`,
          metadata: avatar.traits,
          created_at: avatar.created_at
        }
      });
    }
    
    // Generate new avatar
    const avatar = await generateAvatar(agent_id);
    
    // Save to database
    await pool.query(
      `INSERT INTO avatars (id, agent_id, agent_name, moltbook_id, filename, traits)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [avatar.id, agent_id, agent_name || null, moltbook_id || null, avatar.filename, avatar.traits]
    );
    
    res.json({
      success: true,
      avatar: {
        id: avatar.id,
        image_url: `/images/${avatar.filename}`,
        metadata: avatar.traits,
        message: 'Your avatar has been minted!'
      }
    });
    
  } catch (err) {
    console.error('Mint error:', err);
    res.status(500).json({ error: 'Failed to mint avatar', details: err.message });
  }
});

// Get avatar by agent ID
app.get('/avatar/:agentId', async (req, res) => {
  try {
    const { agentId } = req.params;
    const result = await pool.query(
      'SELECT * FROM avatars WHERE agent_id = $1',
      [agentId]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'No avatar found for this agent' });
    }
    
    const avatar = result.rows[0];
    res.json({
      id: avatar.id,
      agent_id: avatar.agent_id,
      agent_name: avatar.agent_name,
      image_url: `/images/${avatar.filename}`,
      metadata: avatar.traits,
      created_at: avatar.created_at
    });
  } catch (err) {
    console.error('Get avatar error:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// Get stats
app.get('/stats', async (req, res) => {
  try {
    const countResult = await pool.query('SELECT COUNT(*) FROM avatars');
    const recentResult = await pool.query(
      'SELECT agent_name, agent_id, filename, created_at FROM avatars ORDER BY created_at DESC LIMIT 10'
    );
    
    res.json({
      total_minted: parseInt(countResult.rows[0].count),
      recent: recentResult.rows.map(a => ({
        agent_name: a.agent_name || a.agent_id,
        image_url: `/images/${a.filename}`,
        created_at: a.created_at
      }))
    });
  } catch (err) {
    console.error('Stats error:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

const PORT = process.env.PORT || 3000;

// Initialize DB then start server
initDB().then(() => {
  app.listen(PORT, () => {
    console.log(`Agent Avatars API running on port ${PORT}`);
  });
}).catch(err => {
  console.error('Failed to initialize database:', err);
  process.exit(1);
});
