import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ASSETS_DIR = path.join(__dirname, 'assets', 'faces');
const GENERATED_DIR = path.join(__dirname, 'generated');
const DB_PATH = path.join(__dirname, 'data', 'avatars.json');

// Ensure directories exist
fs.mkdirSync(GENERATED_DIR, { recursive: true });
fs.mkdirSync(path.join(__dirname, 'data'), { recursive: true });

// Simple JSON database
function loadDB() {
  if (!fs.existsSync(DB_PATH)) {
    return { avatars: {} };
  }
  return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
}

function saveDB(data) {
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2));
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
    
    const db = loadDB();
    
    // Check if agent already has an avatar
    if (db.avatars[agent_id]) {
      const existing = db.avatars[agent_id];
      return res.status(409).json({ 
        error: 'Agent already has an avatar',
        avatar: {
          id: existing.id,
          image_url: `/images/${existing.filename}`,
          metadata: existing.traits,
          created_at: existing.created_at
        }
      });
    }
    
    // Generate new avatar
    const avatar = await generateAvatar(agent_id);
    
    // Save to database
    db.avatars[agent_id] = {
      id: avatar.id,
      agent_id,
      agent_name: agent_name || null,
      moltbook_id: moltbook_id || null,
      filename: avatar.filename,
      traits: avatar.traits,
      created_at: new Date().toISOString()
    };
    saveDB(db);
    
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
app.get('/avatar/:agentId', (req, res) => {
  const { agentId } = req.params;
  const db = loadDB();
  const avatar = db.avatars[agentId];
  
  if (!avatar) {
    return res.status(404).json({ error: 'No avatar found for this agent' });
  }
  
  res.json({
    id: avatar.id,
    agent_id: avatar.agent_id,
    agent_name: avatar.agent_name,
    image_url: `/images/${avatar.filename}`,
    metadata: avatar.traits,
    created_at: avatar.created_at
  });
});

// Get stats
app.get('/stats', (req, res) => {
  const db = loadDB();
  const avatars = Object.values(db.avatars);
  const recent = avatars
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 10);
  
  res.json({
    total_minted: avatars.length,
    recent: recent.map(a => ({
      agent_name: a.agent_name || a.agent_id,
      image_url: `/images/${a.filename}`,
      created_at: a.created_at
    }))
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Agent Avatars API running on port ${PORT}`);
});
