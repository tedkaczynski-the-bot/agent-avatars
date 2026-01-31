#!/usr/bin/env python3
"""
Generate accessory trait layers for CryptoPunks-style faces
256x256 with transparency - earrings, piercings, etc.
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'accessories')
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

# Ears are around x=7 (left) and x=18 (right), y=10-12

def draw_earring_stud(color='#FFD700'):
    """Simple stud earring"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Single stud on left ear
    draw_block(draw, 6, 11, color)
    
    return img

def draw_earring_both_studs(color='#FFD700'):
    """Studs on both ears"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    draw_block(draw, 6, 11, color)
    draw_block(draw, 19, 11, color)
    
    return img

def draw_earring_hoop(color='#FFD700'):
    """Hoop earring"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Left ear hoop
    draw_block(draw, 5, 11, color)
    draw_block(draw, 5, 12, color)
    draw_block(draw, 5, 13, color)
    draw_block(draw, 6, 13, color)
    draw_block(draw, 6, 12, color)
    
    return img

def draw_earring_both_hoops(color='#FFD700'):
    """Hoops on both ears"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Left hoop
    draw_block(draw, 5, 11, color)
    draw_block(draw, 5, 12, color)
    draw_block(draw, 5, 13, color)
    draw_block(draw, 6, 13, color)
    
    # Right hoop
    draw_block(draw, 20, 11, color)
    draw_block(draw, 20, 12, color)
    draw_block(draw, 20, 13, color)
    draw_block(draw, 19, 13, color)
    
    return img

def draw_earring_dangle(color='#FFD700'):
    """Dangling earring"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Chain and gem
    draw_block(draw, 6, 11, color)
    draw_block(draw, 6, 12, '#C0C0C0')  # Silver chain
    draw_block(draw, 6, 13, '#C0C0C0')
    draw_block(draw, 5, 14, color)
    draw_block(draw, 6, 14, color)
    draw_block(draw, 6, 15, color)
    
    return img

def draw_earring_cross():
    """Cross earring"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    silver = '#C0C0C0'
    
    # Cross on left ear
    draw_block(draw, 6, 11, silver)
    draw_block(draw, 6, 12, silver)
    draw_block(draw, 5, 12, silver)
    draw_block(draw, 7, 12, silver)
    draw_block(draw, 6, 13, silver)
    draw_block(draw, 6, 14, silver)
    
    return img

def draw_nose_ring():
    """Nose ring"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    gold = '#FFD700'
    
    # Ring in nose (around y=14-15)
    draw_block(draw, 12, 15, gold)
    draw_block(draw, 13, 15, gold)
    draw_block(draw, 12, 16, gold)
    
    return img

def draw_nose_stud():
    """Small nose stud"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    diamond = '#E0E0E0'
    
    # Small stud on side of nose
    draw_block(draw, 11, 14, diamond)
    
    return img

def draw_septum():
    """Septum piercing"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    silver = '#C0C0C0'
    
    # Ring through septum
    draw_block(draw, 12, 15, silver)
    draw_block(draw, 13, 15, silver)
    draw_block(draw, 11, 16, silver)
    draw_block(draw, 12, 16, silver)
    draw_block(draw, 13, 16, silver)
    draw_block(draw, 14, 16, silver)
    
    return img

def draw_lip_ring():
    """Lip ring piercing"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    silver = '#C0C0C0'
    
    # Ring on lower lip
    draw_block(draw, 14, 18, silver)
    draw_block(draw, 14, 19, silver)
    draw_block(draw, 15, 19, silver)
    
    return img

def draw_eyebrow_piercing():
    """Eyebrow piercing"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    silver = '#C0C0C0'
    ball = '#FFD700'
    
    # Barbell through eyebrow
    draw_block(draw, 16, 9, ball)
    draw_block(draw, 17, 9, silver)
    draw_block(draw, 18, 9, ball)
    
    return img

def draw_clown_nose():
    """Red clown nose"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    red = '#FF0000'
    highlight = '#FF6666'
    
    # Big red nose
    draw_block(draw, 12, 13, red)
    draw_block(draw, 13, 13, red)
    draw_block(draw, 11, 14, red)
    draw_block(draw, 12, 14, red)
    draw_block(draw, 13, 14, red)
    draw_block(draw, 14, 14, red)
    draw_block(draw, 12, 15, red)
    draw_block(draw, 13, 15, red)
    
    # Highlight
    draw_block(draw, 12, 13, highlight)
    
    return img

def draw_face_tattoo():
    """Face tattoo - teardrop"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    ink = '#1A1A1A'
    
    # Teardrop under eye
    draw_block(draw, 8, 13, ink)
    draw_block(draw, 8, 14, ink)
    
    return img

def draw_scar():
    """Facial scar"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    scar = '#D4A574'  # Lighter than skin
    
    # Diagonal scar on cheek
    draw_block(draw, 16, 12, scar)
    draw_block(draw, 17, 13, scar)
    draw_block(draw, 17, 14, scar)
    draw_block(draw, 18, 15, scar)
    
    return img

def draw_blush():
    """Rosy cheeks / blush"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    pink = '#FFB6C1'
    
    # Blush on both cheeks
    draw_block(draw, 8, 15, pink)
    draw_block(draw, 9, 15, pink)
    draw_block(draw, 17, 15, pink)
    draw_block(draw, 18, 15, pink)
    
    return img

def draw_mole():
    """Beauty mark/mole"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    dark = '#3D2314'
    
    # Single mole
    draw_block(draw, 16, 16, dark)
    
    return img

def draw_freckles():
    """Cute freckles"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    freckle = '#B8860B'
    
    # Scattered freckles on cheeks
    positions = [
        (8, 14), (9, 15), (10, 14),
        (16, 14), (17, 15), (18, 14),
        (9, 13), (17, 13),
    ]
    for x, y in positions:
        draw_block(draw, x, y, freckle)
    
    return img

def draw_band_aid():
    """Band-aid on face"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    bandage = '#F5DEB3'
    pad = '#FFFFFF'
    
    # Diagonal band-aid on cheek
    draw_block(draw, 15, 13, bandage)
    draw_block(draw, 16, 14, bandage)
    draw_block(draw, 17, 15, bandage)
    draw_block(draw, 18, 16, bandage)
    
    # White pad in middle
    draw_block(draw, 16, 14, pad)
    draw_block(draw, 17, 15, pad)
    
    return img

def draw_face_paint_star():
    """Star face paint"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    yellow = '#FFD700'
    
    # Star on cheek
    draw_block(draw, 17, 13, yellow)
    draw_block(draw, 16, 14, yellow)
    draw_block(draw, 17, 14, yellow)
    draw_block(draw, 18, 14, yellow)
    draw_block(draw, 17, 15, yellow)
    draw_block(draw, 16, 16, yellow)
    draw_block(draw, 18, 16, yellow)
    
    return img

def draw_face_paint_heart():
    """Heart face paint"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    red = '#FF1493'
    
    # Heart on cheek
    draw_block(draw, 7, 14, red)
    draw_block(draw, 9, 14, red)
    draw_block(draw, 7, 15, red)
    draw_block(draw, 8, 15, red)
    draw_block(draw, 9, 15, red)
    draw_block(draw, 8, 16, red)
    
    return img

def draw_tongue_piercing():
    """Tongue piercing (stud)"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    silver = '#C0C0C0'
    tongue = '#FF6B6B'
    
    # Tongue sticking out with piercing
    draw_block(draw, 12, 18, tongue)
    draw_block(draw, 13, 18, tongue)
    draw_block(draw, 14, 18, tongue)
    draw_block(draw, 13, 18, silver)  # Stud
    
    return img

def draw_cheek_piercing():
    """Cheek/dimple piercings"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    silver = '#C0C0C0'
    
    # Studs on both cheeks
    draw_block(draw, 9, 17, silver)
    draw_block(draw, 17, 17, silver)
    
    return img

def draw_neck_tattoo():
    """Neck tattoo"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    ink = '#1A1A1A'
    
    # Tribal-ish pattern on neck
    draw_block(draw, 11, 23, ink)
    draw_block(draw, 12, 23, ink)
    draw_block(draw, 13, 23, ink)
    draw_block(draw, 14, 23, ink)
    draw_block(draw, 12, 24, ink)
    draw_block(draw, 13, 24, ink)
    
    return img

def draw_choker():
    """Choker necklace"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    black = '#1A1A1A'
    gem = '#DC143C'
    
    # Choker band
    for x in range(9, 17):
        draw_block(draw, x, 22, black)
    
    # Center gem
    draw_block(draw, 13, 22, gem)
    
    return img

def draw_chain_necklace():
    """Gold chain necklace"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    gold = '#FFD700'
    
    # Chain around neck
    draw_block(draw, 9, 23, gold)
    draw_block(draw, 10, 23, gold)
    draw_block(draw, 11, 24, gold)
    draw_block(draw, 12, 24, gold)
    draw_block(draw, 13, 24, gold)
    draw_block(draw, 14, 24, gold)
    draw_block(draw, 15, 23, gold)
    draw_block(draw, 16, 23, gold)
    
    return img

def main():
    print("Generating accessory traits (256x256)...")
    
    accessories = [
        ('earring_gold_stud', lambda: draw_earring_stud('#FFD700'), 'common'),
        ('earring_silver_stud', lambda: draw_earring_stud('#C0C0C0'), 'common'),
        ('earring_diamond_stud', lambda: draw_earring_stud('#E0E0E0'), 'uncommon'),
        ('earring_both_gold', lambda: draw_earring_both_studs('#FFD700'), 'common'),
        ('earring_both_silver', lambda: draw_earring_both_studs('#C0C0C0'), 'common'),
        ('earring_gold_hoop', lambda: draw_earring_hoop('#FFD700'), 'uncommon'),
        ('earring_silver_hoop', lambda: draw_earring_hoop('#C0C0C0'), 'uncommon'),
        ('earring_both_hoops', lambda: draw_earring_both_hoops('#FFD700'), 'uncommon'),
        ('earring_dangle', lambda: draw_earring_dangle('#FFD700'), 'uncommon'),
        ('earring_cross', draw_earring_cross, 'uncommon'),
        ('nose_ring', draw_nose_ring, 'uncommon'),
        ('nose_stud', draw_nose_stud, 'common'),
        ('septum', draw_septum, 'uncommon'),
        ('lip_ring', draw_lip_ring, 'uncommon'),
        ('eyebrow_piercing', draw_eyebrow_piercing, 'uncommon'),
        ('clown_nose', draw_clown_nose, 'rare'),
        ('face_tattoo', draw_face_tattoo, 'rare'),
        ('scar', draw_scar, 'uncommon'),
        ('blush', draw_blush, 'common'),
        ('mole', draw_mole, 'common'),
        ('freckles', draw_freckles, 'common'),
        ('band_aid', draw_band_aid, 'uncommon'),
        ('face_paint_star', draw_face_paint_star, 'uncommon'),
        ('face_paint_heart', draw_face_paint_heart, 'uncommon'),
        ('tongue_piercing', draw_tongue_piercing, 'uncommon'),
        ('cheek_piercing', draw_cheek_piercing, 'uncommon'),
        ('neck_tattoo', draw_neck_tattoo, 'rare'),
        ('choker', draw_choker, 'uncommon'),
        ('chain_necklace', draw_chain_necklace, 'uncommon'),
    ]
    
    for name, func, rarity in accessories:
        img = func()
        filename = f"accessory_{name}_{rarity}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    print(f"\nDone! {len(accessories)} accessories saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
