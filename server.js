import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pg from 'pg';
import crypto from 'crypto';

const { Pool } = pg;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ASSETS_DIR = path.join(__dirname, 'assets', 'faces');
const GENERATED_DIR = path.join(__dirname, 'generated');
const BASE_URL = process.env.BASE_URL || 'https://agent-avatars-production.up.railway.app';

// Ensure directories exist
fs.mkdirSync(GENERATED_DIR, { recursive: true });

// PostgreSQL connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.DATABASE_URL?.includes('localhost') ? false : { rejectUnauthorized: false }
});

// Generate verification code (word-word format)
const WORDS = ['pixel', 'avatar', 'rare', 'mint', 'trait', 'face', 'eyes', 'punk', 'alien', 'ape', 'zombie', 'crown', 'laser', 'mohawk', 'cyber', 'neon', 'retro', 'glitch', 'vapor', 'synth'];
function generateVerificationCode() {
  const w1 = WORDS[Math.floor(Math.random() * WORDS.length)];
  const w2 = WORDS[Math.floor(Math.random() * WORDS.length)];
  const num = Math.floor(Math.random() * 100);
  return `${w1}-${w2}-${num}`;
}

// Initialize database tables
async function initDB() {
  const client = await pool.connect();
  try {
    // Agents table (registration/claims)
    await client.query(`
      CREATE TABLE IF NOT EXISTS agents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) UNIQUE NOT NULL,
        description TEXT,
        api_key VARCHAR(255) UNIQUE NOT NULL,
        claim_token VARCHAR(255) UNIQUE NOT NULL,
        verification_code VARCHAR(50) NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        claimed_at TIMESTAMP,
        claimed_by VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // Avatars table
    await client.query(`
      CREATE TABLE IF NOT EXISTS avatars (
        id UUID PRIMARY KEY,
        agent_id UUID REFERENCES agents(id),
        agent_name VARCHAR(255),
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

// CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

// Serve generated images
app.use('/images', express.static(GENERATED_DIR));

// Auth middleware
async function authMiddleware(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey) {
    return res.status(401).json({ error: 'API key required. Include X-API-Key header.' });
  }
  
  try {
    const result = await pool.query('SELECT * FROM agents WHERE api_key = $1', [apiKey]);
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Invalid API key' });
    }
    req.agent = result.rows[0];
    next();
  } catch (err) {
    console.error('Auth error:', err);
    res.status(500).json({ error: 'Authentication failed' });
  }
}

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
const RARITY_WEIGHTS = { common: 60, uncommon: 25, rare: 12, legendary: 3 };

function getTraits(category) {
  const dir = path.join(ASSETS_DIR, category);
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.png'))
    .map(filename => {
      const parts = filename.replace('.png', '').split('_');
      const rarity = RARITY_WEIGHTS[parts[parts.length - 1]] ? parts[parts.length - 1] : 'common';
      return { filename, rarity, weight: RARITY_WEIGHTS[rarity] || 60 };
    });
}

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

async function generateAvatar() {
  const traits = {
    background: weightedChoice(getTraits('backgrounds'))?.filename || 'solid_cream_common.png',
    base: weightedChoice(getTraits('base'))?.filename,
    eyes: weightedChoice(getTraits('eyes'))?.filename,
    mouth: weightedChoice(getTraits('mouth'), 20)?.filename,
    hair: weightedChoice(getTraits('hair'), 10)?.filename,
    eyewear: weightedChoice(getTraits('eyewear'), 70)?.filename,
    headwear: weightedChoice(getTraits('headwear'), 60)?.filename,
    accessories: weightedChoice(getTraits('accessories'), 50)?.filename,
  };
  
  const SIZE = 256;
  let composite = sharp(path.join(ASSETS_DIR, 'backgrounds', traits.background)).resize(SIZE, SIZE);
  
  const layers = [];
  for (const layer of ['base', 'eyes', 'mouth', 'accessories', 'hair', 'eyewear', 'headwear']) {
    if (traits[layer]) {
      const layerPath = path.join(ASSETS_DIR, layer, traits[layer]);
      if (fs.existsSync(layerPath)) {
        layers.push({ input: layerPath, top: 0, left: 0 });
      }
    }
  }
  
  if (layers.length > 0) composite = composite.composite(layers);
  
  const avatarId = uuidv4();
  const filename = `avatar_${avatarId}.png`;
  await composite.png().toFile(path.join(GENERATED_DIR, filename));
  
  return {
    id: avatarId,
    filename,
    traits: Object.fromEntries(Object.entries(traits).filter(([_, v]) => v != null))
  };
}

// === API ROUTES ===

app.get('/', (req, res) => {
  res.json({ 
    service: 'agent-avatars',
    status: 'ok',
    endpoints: {
      'POST /api/register': 'Register as an agent (body: {name, description?})',
      'GET /api/agents/status': 'Check your status (requires X-API-Key)',
      'POST /api/mint': 'Mint your avatar (requires X-API-Key, must be claimed)',
      'GET /api/avatar/:name': 'Get avatar by agent name',
      'GET /api/stats': 'Minting stats',
      'GET /claim/:token': 'Claim page for humans'
    }
  });
});

// Register new agent
app.post('/api/register', async (req, res) => {
  try {
    const { name, description } = req.body;
    
    if (!name || name.length < 2 || name.length > 50) {
      return res.status(400).json({ error: 'Name required (2-50 characters)' });
    }
    
    // Check if name exists
    const existing = await pool.query('SELECT id FROM agents WHERE LOWER(name) = LOWER($1)', [name]);
    if (existing.rows.length > 0) {
      return res.status(409).json({ error: 'Agent name already taken' });
    }
    
    const apiKey = `avatar_${crypto.randomBytes(24).toString('hex')}`;
    const claimToken = `avatar_claim_${crypto.randomBytes(16).toString('hex')}`;
    const verificationCode = generateVerificationCode();
    
    const result = await pool.query(
      `INSERT INTO agents (name, description, api_key, claim_token, verification_code)
       VALUES ($1, $2, $3, $4, $5) RETURNING id`,
      [name, description || null, apiKey, claimToken, verificationCode]
    );
    
    res.json({
      success: true,
      agent: {
        id: result.rows[0].id,
        name,
        api_key: apiKey,
        claim_url: `${BASE_URL}/claim/${claimToken}`,
        verification_code: verificationCode
      },
      important: '⚠️ SAVE YOUR API KEY! Send the claim_url to your human. They tweet the verification_code to activate you.',
      next_steps: [
        '1. Save your api_key to ~/.config/molt-avatar/credentials.json',
        '2. Send claim_url to your human',
        '3. Human tweets: "Claiming my molt.avatar agent ' + name + ' 🎨 ' + verificationCode + '"',
        '4. Once claimed, call POST /api/mint to get your avatar!'
      ]
    });
    
  } catch (err) {
    console.error('Register error:', err);
    res.status(500).json({ error: 'Registration failed', details: err.message });
  }
});

// Check agent status
app.get('/api/agents/status', authMiddleware, async (req, res) => {
  const agent = req.agent;
  
  // Check if has avatar
  const avatarResult = await pool.query('SELECT * FROM avatars WHERE agent_id = $1', [agent.id]);
  const avatar = avatarResult.rows[0];
  
  res.json({
    name: agent.name,
    status: agent.status,
    claimed: agent.status === 'claimed',
    claimed_at: agent.claimed_at,
    has_avatar: !!avatar,
    avatar: avatar ? {
      image_url: `/images/${avatar.filename}`,
      traits: avatar.traits,
      created_at: avatar.created_at
    } : null,
    next_action: !agent.claimed_at 
      ? 'Waiting for human to claim you. Share your claim_url!'
      : !avatar 
        ? 'You\'re claimed! Call POST /api/mint to get your avatar.'
        : 'You have your avatar! Use it as your profile pic.'
  });
});

// Claim page (for humans)
app.get('/claim/:token', async (req, res) => {
  try {
    const { token } = req.params;
    const result = await pool.query('SELECT * FROM agents WHERE claim_token = $1', [token]);
    
    if (result.rows.length === 0) {
      return res.status(404).send('Invalid claim link');
    }
    
    const agent = result.rows[0];
    
    if (agent.status === 'claimed') {
      return res.send(`
        <html>
          <head><title>Already Claimed</title></head>
          <body style="font-family: system-ui; max-width: 500px; margin: 50px auto; padding: 20px;">
            <h1>✅ Already Claimed</h1>
            <p><strong>${agent.name}</strong> was claimed on ${new Date(agent.claimed_at).toLocaleDateString()}.</p>
            <p><a href="/">← Back to molt.avatar</a></p>
          </body>
        </html>
      `);
    }
    
    res.send(`
      <html>
        <head><title>Claim ${agent.name}</title></head>
        <body style="font-family: system-ui; max-width: 500px; margin: 50px auto; padding: 20px;">
          <h1>🎨 Claim ${agent.name}</h1>
          <p>To verify you own this agent, tweet the following:</p>
          <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <code>Claiming my molt.avatar agent ${agent.name} 🎨 ${agent.verification_code}</code>
          </div>
          <a href="https://twitter.com/intent/tweet?text=${encodeURIComponent(`Claiming my molt.avatar agent ${agent.name} 🎨 ${agent.verification_code}`)}" 
             target="_blank"
             style="display: inline-block; background: #1da1f2; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none;">
            Tweet to Claim
          </a>
          <form action="/claim/${token}/verify" method="POST" style="margin-top: 30px;">
            <p>After tweeting, paste your tweet URL:</p>
            <input type="text" name="tweet_url" placeholder="https://twitter.com/you/status/..." 
                   style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required>
            <button type="submit" style="margin-top: 10px; padding: 12px 24px; background: #111; color: white; border: none; border-radius: 8px; cursor: pointer;">
              Verify & Claim
            </button>
          </form>
        </body>
      </html>
    `);
    
  } catch (err) {
    console.error('Claim page error:', err);
    res.status(500).send('Error loading claim page');
  }
});

// Verify claim
app.post('/claim/:token/verify', express.urlencoded({ extended: true }), async (req, res) => {
  try {
    const { token } = req.params;
    const { tweet_url } = req.body;
    
    const result = await pool.query('SELECT * FROM agents WHERE claim_token = $1', [token]);
    if (result.rows.length === 0) {
      return res.status(404).send('Invalid claim link');
    }
    
    const agent = result.rows[0];
    if (agent.status === 'claimed') {
      return res.redirect(`/claim/${token}`);
    }
    
    // For now, trust the tweet URL (could verify via Twitter API later)
    await pool.query(
      `UPDATE agents SET status = 'claimed', claimed_at = NOW(), claimed_by = $1 WHERE id = $2`,
      [tweet_url, agent.id]
    );
    
    res.send(`
      <html>
        <head><title>Claimed!</title></head>
        <body style="font-family: system-ui; max-width: 500px; margin: 50px auto; padding: 20px; text-align: center;">
          <h1>🎉 Claimed!</h1>
          <p><strong>${agent.name}</strong> is now verified.</p>
          <p>Your agent can now mint their avatar by calling <code>POST /api/mint</code></p>
          <p><a href="/">← Back to molt.avatar</a></p>
        </body>
      </html>
    `);
    
  } catch (err) {
    console.error('Verify error:', err);
    res.status(500).send('Verification failed');
  }
});

// Mint avatar (requires auth + claimed)
app.post('/api/mint', authMiddleware, async (req, res) => {
  try {
    const agent = req.agent;
    
    if (agent.status !== 'claimed') {
      return res.status(403).json({ 
        error: 'Agent not claimed yet',
        claim_url: `${BASE_URL}/claim/${agent.claim_token}`,
        message: 'Send the claim_url to your human first!'
      });
    }
    
    // Check if already has avatar
    const existing = await pool.query('SELECT * FROM avatars WHERE agent_id = $1', [agent.id]);
    if (existing.rows.length > 0) {
      const avatar = existing.rows[0];
      return res.status(409).json({ 
        error: 'You already have an avatar!',
        avatar: {
          image_url: `/images/${avatar.filename}`,
          full_url: `${BASE_URL}/images/${avatar.filename}`,
          traits: avatar.traits,
          created_at: avatar.created_at
        }
      });
    }
    
    // Generate avatar
    const avatar = await generateAvatar();
    
    await pool.query(
      `INSERT INTO avatars (id, agent_id, agent_name, filename, traits) VALUES ($1, $2, $3, $4, $5)`,
      [avatar.id, agent.id, agent.name, avatar.filename, avatar.traits]
    );
    
    res.json({
      success: true,
      message: '🎨 Your avatar has been minted!',
      avatar: {
        id: avatar.id,
        image_url: `/images/${avatar.filename}`,
        full_url: `${BASE_URL}/images/${avatar.filename}`,
        traits: avatar.traits
      }
    });
    
  } catch (err) {
    console.error('Mint error:', err);
    res.status(500).json({ error: 'Minting failed', details: err.message });
  }
});

// Get avatar by agent name (public)
app.get('/api/avatar/:name', async (req, res) => {
  try {
    const { name } = req.params;
    const result = await pool.query(
      `SELECT a.*, av.filename, av.traits, av.created_at as avatar_created_at 
       FROM agents a 
       LEFT JOIN avatars av ON a.id = av.agent_id 
       WHERE LOWER(a.name) = LOWER($1)`,
      [name]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Agent not found' });
    }
    
    const agent = result.rows[0];
    if (!agent.filename) {
      return res.status(404).json({ error: 'Agent has no avatar yet' });
    }
    
    res.json({
      name: agent.name,
      image_url: `/images/${agent.filename}`,
      full_url: `${BASE_URL}/images/${agent.filename}`,
      traits: agent.traits,
      created_at: agent.avatar_created_at
    });
  } catch (err) {
    console.error('Get avatar error:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// Stats (public)
app.get('/api/stats', async (req, res) => {
  try {
    const agentCount = await pool.query('SELECT COUNT(*) FROM agents WHERE status = $1', ['claimed']);
    const avatarCount = await pool.query('SELECT COUNT(*) FROM avatars');
    const recent = await pool.query(
      `SELECT a.name, av.filename, av.created_at 
       FROM avatars av JOIN agents a ON av.agent_id = a.id 
       ORDER BY av.created_at DESC LIMIT 10`
    );
    
    res.json({
      total_agents: parseInt(agentCount.rows[0].count),
      total_avatars: parseInt(avatarCount.rows[0].count),
      recent: recent.rows.map(r => ({
        name: r.name,
        image_url: `/images/${r.filename}`,
        created_at: r.created_at
      }))
    });
  } catch (err) {
    console.error('Stats error:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

const PORT = process.env.PORT || 3000;

initDB().then(() => {
  app.listen(PORT, () => {
    console.log(`Agent Avatars API running on port ${PORT}`);
  });
}).catch(err => {
  console.error('Failed to initialize database:', err);
  process.exit(1);
});
