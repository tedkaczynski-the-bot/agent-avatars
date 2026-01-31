#!/usr/bin/env python3
"""
Random Punk Generator - creates randomized avatar combinations
"""

from PIL import Image
import os
import random
import json

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'generated')
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIZE = 256

# Background colors (legacy fallback)
BACKGROUNDS = {
    'cream': '#FEF3C7',
    'blue': '#DBEAFE',
    'pink': '#FCE7F3',
    'green': '#D1FAE5',
    'gray': '#E5E7EB',
    'dark': '#1F2937',
    'purple': '#DDD6FE',
    'orange': '#FED7AA',
}

def get_background_files():
    """Get all background PNG files with rarity"""
    bg_dir = os.path.join(ASSETS_DIR, 'backgrounds')
    if not os.path.exists(bg_dir):
        return []
    
    backgrounds = []
    for filename in os.listdir(bg_dir):
        if filename.endswith('.png'):
            # Parse rarity from filename (e.g., "circuit_dark_rare.png")
            parts = filename.replace('.png', '').split('_')
            rarity = parts[-1] if parts[-1] in RARITY_WEIGHTS else 'common'
            backgrounds.append({
                'filename': filename,
                'rarity': rarity,
                'weight': RARITY_WEIGHTS.get(rarity, 60)
            })
    return backgrounds

# Rarity weights (higher = more common)
RARITY_WEIGHTS = {
    'common': 60,
    'uncommon': 25,
    'rare': 12,
    'legendary': 3,
}

def get_traits(category):
    """Get all traits in a category with their rarity"""
    path = os.path.join(ASSETS_DIR, category)
    if not os.path.exists(path):
        return []
    
    traits = []
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            # Parse rarity from filename (e.g., "eyes_blue_uncommon.png")
            parts = filename.replace('.png', '').split('_')
            rarity = parts[-1] if parts[-1] in RARITY_WEIGHTS else 'common'
            traits.append({
                'filename': filename,
                'rarity': rarity,
                'weight': RARITY_WEIGHTS.get(rarity, 60)
            })
    return traits

def weighted_choice(traits, none_chance=0):
    """Pick a trait based on rarity weights, with optional chance of None"""
    if not traits:
        return None
    
    # Add chance for no trait
    if none_chance > 0 and random.randint(1, 100) <= none_chance:
        return None
    
    weights = [t['weight'] for t in traits]
    return random.choices(traits, weights=weights, k=1)[0]

def is_female_base(base_name):
    """Check if base is female type"""
    return 'female' in base_name

def is_male_base(base_name):
    """Check if base is male type"""
    return 'male' in base_name and 'female' not in base_name

def is_special_base(base_name):
    """Check if base is zombie/ape/alien"""
    return any(x in base_name for x in ['zombie', 'ape', 'alien'])

def filter_hair_for_base(hair_traits, base_name):
    """Filter hair traits appropriate for the base type"""
    filtered = []
    is_female = is_female_base(base_name)
    is_male = is_male_base(base_name)
    
    for trait in hair_traits:
        filename = trait['filename']
        
        # Female-specific hair only for females
        if '_female_' in filename and not is_female:
            continue
        # Male-specific hair only for males
        if '_male_' in filename and not is_male:
            continue
        # Skip gendered hair for special types (zombie/ape/alien)
        if is_special_base(base_name) and ('_female_' in filename or '_male_' in filename):
            continue
            
        filtered.append(trait)
    
    return filtered

def create_background(color):
    """Create a solid color background (legacy fallback)"""
    if color.startswith('#'):
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    else:
        rgb = tuple(int(BACKGROUNDS.get(color, '#FEF3C7')[i:i+2], 16) for i in (1, 3, 5))
    return Image.new('RGBA', (SIZE, SIZE), rgb + (255,))

def load_background(bg_filename):
    """Load a background PNG file"""
    bg_path = os.path.join(ASSETS_DIR, 'backgrounds', bg_filename)
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).convert('RGBA')
        return bg
    # Fallback to cream
    return create_background('#FEF3C7')

def composite_layers(base, layers, bg_filename=None, bg_color='cream'):
    """Composite all layers together"""
    # Start with background
    if bg_filename:
        result = load_background(bg_filename)
    elif bg_color.startswith('#'):
        result = create_background(bg_color)
    else:
        result = create_background(BACKGROUNDS.get(bg_color, BACKGROUNDS['cream']))
    
    # Add base
    base_path = os.path.join(ASSETS_DIR, 'base', base)
    if os.path.exists(base_path):
        base_img = Image.open(base_path)
        result.paste(base_img, (0, 0), base_img)
    
    # Layer order
    layer_order = ['eyes', 'mouth', 'accessories', 'hair', 'eyewear', 'headwear']
    
    for category in layer_order:
        if category in layers and layers[category]:
            layer_path = os.path.join(ASSETS_DIR, category, layers[category])
            if os.path.exists(layer_path):
                layer_img = Image.open(layer_path)
                result.paste(layer_img, (0, 0), layer_img)
    
    return result

def generate_punk(punk_id=None):
    """Generate a single random punk"""
    
    # Get all traits
    bases = get_traits('base')
    eyes = get_traits('eyes')
    hair = get_traits('hair')
    eyewear = get_traits('eyewear')
    headwear = get_traits('headwear')
    mouth = get_traits('mouth')
    accessories = get_traits('accessories')
    
    # Pick base (required)
    base_trait = weighted_choice(bases)
    base = base_trait['filename']
    
    # Filter hair for base type
    appropriate_hair = filter_hair_for_base(hair, base)
    
    layers = {}
    
    # Eyes (always)
    if eyes:
        eye_trait = weighted_choice(eyes)
        layers['eyes'] = eye_trait['filename'] if eye_trait else None
    
    # Mouth (80% chance)
    if mouth and random.randint(1, 100) <= 80:
        mouth_trait = weighted_choice(mouth)
        layers['mouth'] = mouth_trait['filename'] if mouth_trait else None
    else:
        layers['mouth'] = None
    
    # Hair (90% chance)
    if appropriate_hair and random.randint(1, 100) <= 90:
        hair_trait = weighted_choice(appropriate_hair)
        layers['hair'] = hair_trait['filename'] if hair_trait else None
    else:
        layers['hair'] = None
    
    # Eyewear (30% chance)
    if eyewear and random.randint(1, 100) <= 30:
        eyewear_trait = weighted_choice(eyewear)
        layers['eyewear'] = eyewear_trait['filename'] if eyewear_trait else None
    else:
        layers['eyewear'] = None
    
    # Headwear (40% chance)
    if headwear and random.randint(1, 100) <= 40:
        headwear_trait = weighted_choice(headwear)
        layers['headwear'] = headwear_trait['filename'] if headwear_trait else None
    else:
        layers['headwear'] = None
    
    # Accessories (50% chance)
    if accessories and random.randint(1, 100) <= 50:
        acc_trait = weighted_choice(accessories)
        layers['accessories'] = acc_trait['filename'] if acc_trait else None
    else:
        layers['accessories'] = None
    
    # Pick background (use files if available, else fallback to colors)
    bg_files = get_background_files()
    if bg_files:
        bg_trait = weighted_choice(bg_files)
        bg_filename = bg_trait['filename'] if bg_trait else None
        bg_color = None
    else:
        bg_filename = None
        bg_color = random.choice(list(BACKGROUNDS.keys()))
    
    # Composite
    punk_img = composite_layers(base, layers, bg_filename=bg_filename, bg_color=bg_color)
    
    # Build metadata
    metadata = {
        'id': punk_id,
        'base': base,
        'background': bg_filename or bg_color,
        'traits': {k: v for k, v in layers.items() if v}
    }
    
    return punk_img, metadata

def generate_batch(count=20):
    """Generate a batch of random punks"""
    print(f"Generating {count} random punks...")
    
    all_metadata = []
    
    for i in range(count):
        punk_img, metadata = generate_punk(punk_id=i+1)
        
        # Save image
        filename = f"punk_{i+1:04d}.png"
        punk_img.save(os.path.join(OUTPUT_DIR, filename))
        
        metadata['filename'] = filename
        all_metadata.append(metadata)
        
        # Count traits
        trait_count = len([v for v in metadata['traits'].values() if v])
        print(f"  ✓ {filename} - {metadata['base'].split('_')[0]} with {trait_count} traits")
    
    # Save metadata
    with open(os.path.join(OUTPUT_DIR, 'metadata.json'), 'w') as f:
        json.dump(all_metadata, f, indent=2)
    
    print(f"\nDone! {count} punks saved to {OUTPUT_DIR}")
    print(f"Metadata saved to {OUTPUT_DIR}/metadata.json")

if __name__ == "__main__":
    generate_batch(20)
