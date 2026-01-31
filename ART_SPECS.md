# Agent Avatars — Art Specifications

## Canvas

| Property | Value |
|----------|-------|
| Dimensions | **256 × 256 pixels** |
| Format | PNG with transparency |
| Color depth | 32-bit RGBA |
| Style | **CryptoPunks-inspired pixel faces** |

> **Note:** 256x256 is standard NFT size. Chunky pixel aesthetic but at higher res — faces fill the canvas, not full bodies.

---

## Color Palette

### Skin Tones (10 colors)
```
#FFDBAC - Light 1
#F5C9A6 - Light 2
#E5B894 - Light 3
#D4A574 - Medium 1
#C69C6D - Medium 2
#A67C52 - Medium 3
#8D5524 - Dark 1
#6B4423 - Dark 2
#4A2E1C - Dark 3
#7ED321 - Alien Green
```

### Hair Colors (8 colors)
```
#090806 - Black
#2C1608 - Dark Brown
#6A4E42 - Brown
#B55239 - Auburn
#D6B370 - Blonde
#AFAFAF - Gray
#E6E6E6 - White
#A855F7 - Purple (rare)
```

### Clothing Base Colors (12 colors)
```
#1F2937 - Charcoal
#374151 - Gray
#FFFFFF - White
#000000 - Black
#EF4444 - Red
#3B82F6 - Blue
#22C55E - Green
#F59E0B - Orange
#8B5CF6 - Purple
#EC4899 - Pink
#06B6D4 - Cyan
#84CC16 - Lime
```

### Background Colors (8 colors)
```
#FEF3C7 - Cream
#DBEAFE - Light Blue
#FCE7F3 - Light Pink
#D1FAE5 - Light Green
#E5E7EB - Light Gray
#1F2937 - Dark Gray
#7C3AED - Purple
#F97316 - Orange
```

---

## Layer Order (bottom to top)

| Layer | Z-Index | Category | Notes |
|-------|---------|----------|-------|
| 1 | 0 | Background | Full 256x256, solid color |
| 2 | 1 | Base Head | Face shape + skin tone |
| 3 | 2 | Hair (back) | Hair behind head (ponytails, long hair) |
| 4 | 3 | Ears | Optional, some types |
| 5 | 4 | Face | Eyes, nose, mouth, expression |
| 6 | 5 | Facial Hair | Beards, mustaches |
| 7 | 6 | Hair (front) | Bangs, top hair |
| 8 | 7 | Eyewear | Glasses, shades, VR, 3D glasses |
| 9 | 8 | Accessories | Earrings, piercings |
| 10 | 9 | Headwear | Hats, caps, beanies, headphones |
| 11 | 10 | Mouth Accessories | Cigarette, pipe, mask |

---

## Base Types (Punks)

| Type | Description | Rarity |
|------|-------------|--------|
| Male | Classic male punk face | Common |
| Female | Female punk face | Common |
| Zombie | Green-tinted undead | Rare |
| Ape | Primate face | Rare |
| Alien | Blue/green alien | Legendary |

### Face Template (256x256)

```
┌────────────────────────────────────┐
│                                    │  y: 0-40    ← headwear zone
│         ┌──────────────┐           │
│         │     HAIR     │           │  y: 20-80   ← hair/top of head
│      ┌──┴──────────────┴──┐        │
│      │                    │        │  y: 60-100  ← forehead
│      │   ████      ████   │        │  y: 90-120  ← eyes zone
│      │                    │        │
│      │        ██          │        │  y: 130-150 ← nose
│      │                    │        │
│      │    ██████████      │        │  y: 160-190 ← mouth
│      │                    │        │
│      └────────┬───────────┘        │  y: 190-220 ← jaw/chin
│               │                    │  y: 220-256 ← neck (minimal)
└────────────────────────────────────┘
              x: 128 = center
```

> Face fills ~80% of canvas. Chunky pixels (~8-16px per "pixel block") for CryptoPunks aesthetic.

---

## Layer Specifications

### 1. Background
- Full 256x256 canvas
- Solid color, no transparency
- Limited palette (8-10 colors)

### 2. Base Head
- Face shape with skin tone
- 5 types: Male, Female, Zombie, Ape, Alien
- Each type has distinct silhouette

### 3. Hair (Back)
- Long hair, ponytails that go behind head
- Transparent PNG

### 4. Face Features
- Eyes: various styles (dots, lines, wide, narrow, laser)
- Nose: minimal (1-3 pixels typically)
- Mouth: various expressions

### 5. Facial Hair
- Beards, mustaches, goatees
- Male/Ape types only

### 6. Hair (Front)
- Bangs, mohawks, spiky, bald shine
- Rendered over face but under headwear

### 7. Eyewear
- Regular glasses, shades, 3D glasses
- VR headset (rare)
- Eye patch

### 8. Accessories
- Earrings (gold, silver, diamond)
- Nose ring
- Clown nose (rare)

### 9. Headwear
- Caps, beanies, bandanas
- Crowns, tiaras (rare)
- Headphones
- Pilot helmet (rare)

### 10. Mouth Accessories
- Cigarette, pipe, vape
- Medical mask
- Bubble gum

---

## File Naming Convention

```
{category}_{name}_{rarity}.png

Examples:
- body_boy_common.png
- body_alien_legendary.png
- hair_mohawk_rare.png
- clothing_hoodie_uncommon.png
- hat_crown_legendary.png
- background_sunset_rare.png
```

---

## Rarity Distribution

| Rarity | Drop Rate | Visual Style |
|--------|-----------|--------------|
| Common | 60% | Basic, simple |
| Uncommon | 25% | Nicer details, patterns |
| Rare | 12% | Special effects, unique |
| Legendary | 3% | Animated?, glowing, alien |

---

## Validation Rules

For creator-submitted items:

1. **Dimensions**: Must be exactly 256x256
2. **Format**: PNG with alpha channel
3. **Transparency**: Background must be transparent (except background layer)
4. **Positioning**: Must align with base head template
5. **File size**: Max 500KB
6. **Content**: No offensive/illegal content

---

## Template Files Needed

- [ ] `base_male.png` — Male punk base head
- [ ] `base_female.png` — Female punk base head
- [ ] `base_zombie.png` — Zombie base head
- [ ] `base_ape.png` — Ape base head
- [ ] `base_alien.png` — Alien base head
- [ ] `template_zones.png` — Layer positioning guide (24x24)
- [ ] `palette.ase` — Color palette (Adobe Swatch Exchange)
- [ ] `palette.png` — Visual color swatches

---

*Created: 2026-01-31*
