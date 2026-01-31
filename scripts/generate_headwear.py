#!/usr/bin/env python3
"""
Generate headwear trait layers for CryptoPunks-style faces
256x256 with transparency, positioned on top of head
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'headwear')
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIZE = 256
BLOCK = 10

def draw_block(draw, x, y, color, block_size=BLOCK):
    """Draw a single pixel block"""
    draw.rectangle([x * block_size, y * block_size, 
                   (x + 1) * block_size - 1, (y + 1) * block_size - 1], 
                  fill=color)

def create_canvas():
    return Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))

# Head top is around y=3-5, head spans roughly x=7-18

def draw_cap(color='#1F2937'):
    """Baseball cap"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Cap dome
    for x in range(7, 19):
        draw_block(draw, x, 2, color)
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    for x in range(8, 18):
        draw_block(draw, x, 1, color)
    
    # Brim (front facing)
    for x in range(6, 20):
        draw_block(draw, x, 5, color)
    for x in range(5, 21):
        draw_block(draw, x, 6, color)
    
    return img

def draw_cap_backwards(color='#1F2937'):
    """Backwards cap"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Cap dome
    for x in range(7, 19):
        draw_block(draw, x, 2, color)
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    for x in range(8, 18):
        draw_block(draw, x, 1, color)
    
    # Brim (back/side)
    draw_block(draw, 19, 3, color)
    draw_block(draw, 20, 4, color)
    draw_block(draw, 21, 5, color)
    
    # Snap back adjuster
    draw_block(draw, 12, 5, '#FFFFFF')
    draw_block(draw, 13, 5, '#FFFFFF')
    
    return img

def draw_beanie(color='#EF4444'):
    """Knit beanie"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    darker = '#' + ''.join(f'{max(0, int(color[i:i+2], 16) - 30):02x}' for i in (1, 3, 5))
    
    # Beanie dome
    for x in range(9, 17):
        draw_block(draw, x, 0, color)
    for x in range(7, 19):
        draw_block(draw, x, 1, color)
    for x in range(6, 20):
        draw_block(draw, x, 2, color)
        draw_block(draw, x, 3, color)
    
    # Folded brim
    for x in range(6, 20):
        draw_block(draw, x, 4, darker)
        draw_block(draw, x, 5, darker)
    
    # Knit texture lines
    for x in [8, 11, 14, 17]:
        draw_block(draw, x, 2, darker)
        draw_block(draw, x, 3, darker)
    
    return img

def draw_crown():
    """Royal crown"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    gold = '#FFD700'
    dark_gold = '#DAA520'
    red = '#DC143C'
    jewel = '#00FFFF'
    
    # Crown base
    for x in range(7, 19):
        draw_block(draw, x, 4, gold)
        draw_block(draw, x, 5, dark_gold)
    
    # Crown points
    points = [7, 10, 13, 16, 18]
    for px in points:
        draw_block(draw, px, 3, gold)
        draw_block(draw, px, 2, gold)
        draw_block(draw, px, 1, gold)
    
    # Jewels
    draw_block(draw, 10, 4, red)
    draw_block(draw, 13, 4, jewel)
    draw_block(draw, 16, 4, red)
    
    # Top jewels
    for px in points:
        draw_block(draw, px, 1, jewel)
    
    return img

def draw_bandana(color='#EF4444'):
    """Tied bandana"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Bandana wrapped around head
    for x in range(6, 20):
        draw_block(draw, x, 4, color)
        draw_block(draw, x, 5, color)
    
    # Knot on side
    draw_block(draw, 19, 4, color)
    draw_block(draw, 20, 4, color)
    draw_block(draw, 20, 5, color)
    draw_block(draw, 21, 5, color)
    draw_block(draw, 20, 6, color)
    draw_block(draw, 21, 6, color)
    draw_block(draw, 21, 7, color)
    
    return img

def draw_headband(color='#FFFFFF'):
    """Athletic headband"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Simple band
    for x in range(6, 20):
        draw_block(draw, x, 5, color)
        draw_block(draw, x, 6, color)
    
    return img

def draw_top_hat():
    """Fancy top hat"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    black = '#1A1A1A'
    band = '#DC143C'
    
    # Tall top
    for y in range(-2, 4):
        for x in range(9, 17):
            if y >= 0:
                draw_block(draw, x, y, black)
    # Can't go negative, start from 0
    for x in range(9, 17):
        draw_block(draw, x, 0, black)
        draw_block(draw, x, 1, black)
        draw_block(draw, x, 2, black)
        draw_block(draw, x, 3, black)
    
    # Brim
    for x in range(6, 20):
        draw_block(draw, x, 4, black)
        draw_block(draw, x, 5, black)
    
    # Red band
    for x in range(9, 17):
        draw_block(draw, x, 3, band)
    
    return img

def draw_cowboy_hat():
    """Cowboy hat"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    brown = '#8B4513'
    dark = '#5D3A1A'
    band = '#1A1A1A'
    
    # Crown (dented top)
    for x in range(9, 17):
        draw_block(draw, x, 1, brown)
        draw_block(draw, x, 2, brown)
    for x in range(10, 16):
        draw_block(draw, x, 0, brown)
    # Dent
    draw_block(draw, 12, 1, dark)
    draw_block(draw, 13, 1, dark)
    
    # Band
    for x in range(9, 17):
        draw_block(draw, x, 3, band)
    
    # Wide brim (curved up at sides)
    for x in range(4, 22):
        draw_block(draw, x, 4, brown)
    for x in range(5, 21):
        draw_block(draw, x, 5, brown)
    # Curve up
    draw_block(draw, 4, 3, brown)
    draw_block(draw, 21, 3, brown)
    
    return img

def draw_fedora():
    """Fedora hat"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    gray = '#4A4A4A'
    dark = '#2A2A2A'
    band = '#1A1A1A'
    
    # Crown with dent
    for x in range(8, 18):
        draw_block(draw, x, 1, gray)
        draw_block(draw, x, 2, gray)
    for x in range(9, 17):
        draw_block(draw, x, 0, gray)
    draw_block(draw, 12, 1, dark)
    draw_block(draw, 13, 1, dark)
    
    # Band
    for x in range(8, 18):
        draw_block(draw, x, 3, band)
    
    # Brim (angled)
    for x in range(6, 20):
        draw_block(draw, x, 4, gray)
    for x in range(7, 19):
        draw_block(draw, x, 5, gray)
    draw_block(draw, 5, 4, gray)
    draw_block(draw, 20, 4, gray)
    
    return img

def draw_headphones():
    """DJ headphones"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    black = '#1A1A1A'
    silver = '#C0C0C0'
    cushion = '#2A2A2A'
    
    # Headband
    for x in range(7, 19):
        draw_block(draw, x, 1, black)
    for x in range(8, 18):
        draw_block(draw, x, 0, black)
    
    # Left ear cup
    for y in range(6, 12):
        draw_block(draw, 4, y, black)
        draw_block(draw, 5, y, black)
        draw_block(draw, 6, y, black)
    for y in range(7, 11):
        draw_block(draw, 5, y, cushion)
    draw_block(draw, 5, 8, silver)
    draw_block(draw, 5, 9, silver)
    
    # Right ear cup
    for y in range(6, 12):
        draw_block(draw, 19, y, black)
        draw_block(draw, 20, y, black)
        draw_block(draw, 21, y, black)
    for y in range(7, 11):
        draw_block(draw, 20, y, cushion)
    draw_block(draw, 20, 8, silver)
    draw_block(draw, 20, 9, silver)
    
    # Arms connecting
    draw_block(draw, 6, 2, black)
    draw_block(draw, 6, 3, black)
    draw_block(draw, 6, 4, black)
    draw_block(draw, 6, 5, black)
    draw_block(draw, 19, 2, black)
    draw_block(draw, 19, 3, black)
    draw_block(draw, 19, 4, black)
    draw_block(draw, 19, 5, black)
    
    return img

def draw_halo():
    """Angel halo"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    gold = '#FFD700'
    glow = '#FFEC8B'
    
    # Floating ring above head
    for x in range(8, 18):
        draw_block(draw, x, 0, gold)
    draw_block(draw, 7, 0, glow)
    draw_block(draw, 18, 0, glow)
    
    # Inner glow
    for x in range(9, 17):
        draw_block(draw, x, 1, glow)
    
    return img

def draw_devil_horns():
    """Devil horns"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    red = '#DC143C'
    dark = '#8B0000'
    
    # Left horn
    draw_block(draw, 7, 4, red)
    draw_block(draw, 6, 3, red)
    draw_block(draw, 6, 2, red)
    draw_block(draw, 5, 1, red)
    draw_block(draw, 5, 0, dark)
    
    # Right horn
    draw_block(draw, 18, 4, red)
    draw_block(draw, 19, 3, red)
    draw_block(draw, 19, 2, red)
    draw_block(draw, 20, 1, red)
    draw_block(draw, 20, 0, dark)
    
    return img

def draw_pilot_helmet():
    """Pilot/aviator helmet"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    leather = '#8B4513'
    dark = '#5D3A1A'
    goggles = '#87CEEB'
    metal = '#C0C0C0'
    
    # Helmet dome
    for x in range(6, 20):
        draw_block(draw, x, 1, leather)
        draw_block(draw, x, 2, leather)
        draw_block(draw, x, 3, leather)
        draw_block(draw, x, 4, leather)
    for x in range(8, 18):
        draw_block(draw, x, 0, leather)
    
    # Ear flaps
    for y in range(5, 12):
        draw_block(draw, 5, y, leather)
        draw_block(draw, 6, y, leather)
        draw_block(draw, 19, y, leather)
        draw_block(draw, 20, y, leather)
    
    # Goggles pushed up
    for x in range(8, 18):
        draw_block(draw, x, 3, goggles)
    draw_block(draw, 7, 3, metal)
    draw_block(draw, 18, 3, metal)
    
    # Chin strap hints
    draw_block(draw, 6, 12, dark)
    draw_block(draw, 19, 12, dark)
    
    return img

def draw_lobster_hat():
    """LOBSTER HAT 🦞"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    red = '#DC143C'
    dark_red = '#8B0000'
    orange = '#FF6347'
    eye = '#1A1A1A'
    
    # Lobster body (sits on head like a hat)
    # Main body
    for x in range(8, 18):
        draw_block(draw, x, 2, red)
        draw_block(draw, x, 3, red)
        draw_block(draw, x, 4, red)
    for x in range(9, 17):
        draw_block(draw, x, 1, red)
    
    # Tail (hanging back)
    draw_block(draw, 18, 3, red)
    draw_block(draw, 19, 3, red)
    draw_block(draw, 20, 4, red)
    draw_block(draw, 21, 4, orange)
    draw_block(draw, 21, 5, orange)
    draw_block(draw, 22, 5, orange)
    # Tail fan
    draw_block(draw, 22, 4, red)
    draw_block(draw, 23, 4, red)
    draw_block(draw, 23, 5, red)
    draw_block(draw, 23, 6, red)
    draw_block(draw, 22, 6, red)
    
    # Claws (front, hanging over forehead)
    # Left claw
    draw_block(draw, 6, 4, red)
    draw_block(draw, 5, 4, red)
    draw_block(draw, 5, 5, red)
    draw_block(draw, 4, 5, orange)
    draw_block(draw, 4, 6, red)
    draw_block(draw, 3, 5, red)
    draw_block(draw, 3, 6, dark_red)
    
    # Right claw
    draw_block(draw, 8, 5, red)
    draw_block(draw, 7, 5, red)
    draw_block(draw, 7, 6, red)
    draw_block(draw, 6, 6, orange)
    draw_block(draw, 6, 7, red)
    draw_block(draw, 5, 6, red)
    draw_block(draw, 5, 7, dark_red)
    
    # Antennae
    draw_block(draw, 10, 0, red)
    draw_block(draw, 9, 0, orange)
    draw_block(draw, 16, 0, red)
    draw_block(draw, 17, 0, orange)
    
    # Eyes (stalks)
    draw_block(draw, 11, 1, red)
    draw_block(draw, 11, 0, eye)
    draw_block(draw, 15, 1, red)
    draw_block(draw, 15, 0, eye)
    
    # Legs (hanging on sides)
    for y in range(5, 8):
        draw_block(draw, 7, y, dark_red)
        draw_block(draw, 18, y, dark_red)
    
    return img

def draw_party_hat():
    """Birthday party hat"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3']
    pom = '#FFFFFF'
    
    # Cone shape
    draw_block(draw, 13, 0, pom)  # Pom pom
    for i, y in enumerate(range(1, 6)):
        width = i + 1
        color = colors[i % len(colors)]
        for x in range(13 - width, 13 + width + 1):
            draw_block(draw, x, y, color)
    
    # Elastic string
    draw_block(draw, 7, 6, '#1A1A1A')
    draw_block(draw, 19, 6, '#1A1A1A')
    
    return img

def main():
    print("Generating headwear traits (256x256)...")
    
    headwear = [
        ('cap_black', lambda: draw_cap('#1A1A1A'), 'common'),
        ('cap_red', lambda: draw_cap('#DC143C'), 'common'),
        ('cap_blue', lambda: draw_cap('#3B82F6'), 'common'),
        ('cap_backwards', lambda: draw_cap_backwards('#1A1A1A'), 'uncommon'),
        ('beanie_red', lambda: draw_beanie('#EF4444'), 'common'),
        ('beanie_blue', lambda: draw_beanie('#3B82F6'), 'common'),
        ('beanie_black', lambda: draw_beanie('#1A1A1A'), 'common'),
        ('crown', draw_crown, 'rare'),
        ('bandana_red', lambda: draw_bandana('#EF4444'), 'uncommon'),
        ('bandana_blue', lambda: draw_bandana('#3B82F6'), 'uncommon'),
        ('headband_white', lambda: draw_headband('#FFFFFF'), 'common'),
        ('headband_red', lambda: draw_headband('#EF4444'), 'common'),
        ('top_hat', draw_top_hat, 'rare'),
        ('cowboy_hat', draw_cowboy_hat, 'uncommon'),
        ('fedora', draw_fedora, 'uncommon'),
        ('headphones', draw_headphones, 'uncommon'),
        ('halo', draw_halo, 'rare'),
        ('devil_horns', draw_devil_horns, 'rare'),
        ('pilot_helmet', draw_pilot_helmet, 'rare'),
        ('lobster', draw_lobster_hat, 'legendary'),
        ('party_hat', draw_party_hat, 'uncommon'),
    ]
    
    for name, func, rarity in headwear:
        img = func()
        filename = f"headwear_{name}_{rarity}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    print(f"\nDone! {len(headwear)} headwear styles saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
