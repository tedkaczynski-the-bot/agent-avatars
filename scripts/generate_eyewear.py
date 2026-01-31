#!/usr/bin/env python3
"""
Generate eyewear trait layers for CryptoPunks-style faces
256x256 with transparency, positioned over eyes (around y=11)
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'eyewear')
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

# Eyes are around x=8-10 (left) and x=15-17 (right), y=11

def draw_regular_glasses():
    """Simple regular glasses"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#1A1A1A'  # Black frame
    lens = '#AADDFF'   # Light blue tint
    
    # Left lens
    for y in [10, 11, 12]:
        for x in [7, 8, 9, 10, 11]:
            draw_block(draw, x, y, lens)
    # Left frame
    for x in [7, 8, 9, 10, 11]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    draw_block(draw, 6, 10, frame)
    draw_block(draw, 6, 11, frame)
    draw_block(draw, 6, 12, frame)
    draw_block(draw, 12, 10, frame)
    draw_block(draw, 12, 11, frame)
    draw_block(draw, 12, 12, frame)
    
    # Right lens
    for y in [10, 11, 12]:
        for x in [14, 15, 16, 17, 18]:
            draw_block(draw, x, y, lens)
    # Right frame
    for x in [14, 15, 16, 17, 18]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    draw_block(draw, 13, 10, frame)
    draw_block(draw, 13, 11, frame)
    draw_block(draw, 13, 12, frame)
    draw_block(draw, 19, 10, frame)
    draw_block(draw, 19, 11, frame)
    draw_block(draw, 19, 12, frame)
    
    # Bridge
    draw_block(draw, 12, 11, frame)
    draw_block(draw, 13, 11, frame)
    
    # Temples (arms)
    draw_block(draw, 5, 11, frame)
    draw_block(draw, 20, 11, frame)
    
    return img

def draw_sunglasses():
    """Cool dark shades"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#1A1A1A'
    lens = '#2A2A2A'  # Dark lens
    
    # Left lens - darker, sleeker
    for y in [10, 11, 12]:
        for x in [7, 8, 9, 10, 11]:
            draw_block(draw, x, y, lens)
    for x in [7, 8, 9, 10, 11]:
        draw_block(draw, x, 9, frame)
    
    # Right lens
    for y in [10, 11, 12]:
        for x in [14, 15, 16, 17, 18]:
            draw_block(draw, x, y, lens)
    for x in [14, 15, 16, 17, 18]:
        draw_block(draw, x, 9, frame)
    
    # Bridge
    draw_block(draw, 12, 10, frame)
    draw_block(draw, 13, 10, frame)
    
    # Temples
    draw_block(draw, 6, 10, frame)
    draw_block(draw, 5, 11, frame)
    draw_block(draw, 19, 10, frame)
    draw_block(draw, 20, 11, frame)
    
    return img

def draw_aviators():
    """Aviator sunglasses"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#DAA520'  # Gold frame
    lens = '#3A3A3A'   # Dark lens
    
    # Left lens - teardrop shape
    for x in [7, 8, 9, 10, 11]:
        draw_block(draw, x, 10, lens)
        draw_block(draw, x, 11, lens)
    for x in [8, 9, 10]:
        draw_block(draw, x, 12, lens)
    draw_block(draw, 9, 13, lens)
    
    # Right lens
    for x in [14, 15, 16, 17, 18]:
        draw_block(draw, x, 10, lens)
        draw_block(draw, x, 11, lens)
    for x in [15, 16, 17]:
        draw_block(draw, x, 12, lens)
    draw_block(draw, 16, 13, lens)
    
    # Gold frame top
    for x in [6, 7, 8, 9, 10, 11, 12]:
        draw_block(draw, x, 9, frame)
    for x in [13, 14, 15, 16, 17, 18, 19]:
        draw_block(draw, x, 9, frame)
    
    # Bridge
    draw_block(draw, 12, 10, frame)
    draw_block(draw, 13, 10, frame)
    
    # Temples
    draw_block(draw, 5, 10, frame)
    draw_block(draw, 20, 10, frame)
    
    return img

def draw_3d_glasses():
    """Red/blue 3D glasses"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#FFFFFF'  # White frame
    red_lens = '#FF0000'
    blue_lens = '#00FFFF'
    
    # Left lens (red)
    for y in [10, 11, 12]:
        for x in [7, 8, 9, 10, 11]:
            draw_block(draw, x, y, red_lens)
    
    # Right lens (blue/cyan)
    for y in [10, 11, 12]:
        for x in [14, 15, 16, 17, 18]:
            draw_block(draw, x, y, blue_lens)
    
    # White frame
    for x in [6, 7, 8, 9, 10, 11, 12]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    for x in [13, 14, 15, 16, 17, 18, 19]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    
    draw_block(draw, 6, 10, frame)
    draw_block(draw, 6, 11, frame)
    draw_block(draw, 6, 12, frame)
    draw_block(draw, 19, 10, frame)
    draw_block(draw, 19, 11, frame)
    draw_block(draw, 19, 12, frame)
    
    # Bridge
    draw_block(draw, 12, 11, frame)
    draw_block(draw, 13, 11, frame)
    
    return img

def draw_nerd_glasses():
    """Thick black nerd glasses"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#1A1A1A'
    lens = '#E8E8E8'  # Clear-ish
    
    # Left lens - thick frames
    for y in [10, 11, 12]:
        for x in [8, 9, 10]:
            draw_block(draw, x, y, lens)
    # Thick frame
    for x in [7, 8, 9, 10, 11]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    for y in [9, 10, 11, 12, 13]:
        draw_block(draw, 7, y, frame)
        draw_block(draw, 11, y, frame)
    
    # Right lens
    for y in [10, 11, 12]:
        for x in [15, 16, 17]:
            draw_block(draw, x, y, lens)
    # Thick frame
    for x in [14, 15, 16, 17, 18]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    for y in [9, 10, 11, 12, 13]:
        draw_block(draw, 14, y, frame)
        draw_block(draw, 18, y, frame)
    
    # Bridge
    draw_block(draw, 12, 11, frame)
    draw_block(draw, 13, 11, frame)
    
    # Temples
    draw_block(draw, 6, 11, frame)
    draw_block(draw, 5, 11, frame)
    draw_block(draw, 19, 11, frame)
    draw_block(draw, 20, 11, frame)
    
    return img

def draw_eye_patch():
    """Pirate eye patch"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    patch = '#1A1A1A'
    strap = '#4A3728'  # Brown leather
    
    # Patch over left eye
    for y in [9, 10, 11, 12, 13]:
        for x in [7, 8, 9, 10, 11]:
            draw_block(draw, x, y, patch)
    
    # Strap going diagonally
    draw_block(draw, 6, 9, strap)
    draw_block(draw, 5, 8, strap)
    draw_block(draw, 4, 7, strap)
    draw_block(draw, 12, 9, strap)
    draw_block(draw, 13, 8, strap)
    draw_block(draw, 14, 7, strap)
    draw_block(draw, 15, 6, strap)
    draw_block(draw, 16, 5, strap)
    
    return img

def draw_monocle():
    """Fancy monocle"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#DAA520'  # Gold
    lens = '#E8E8FF'   # Slight tint
    chain = '#DAA520'
    
    # Monocle on right eye
    for y in [10, 11, 12]:
        for x in [14, 15, 16, 17]:
            draw_block(draw, x, y, lens)
    
    # Gold rim
    for x in [14, 15, 16, 17]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    draw_block(draw, 13, 10, frame)
    draw_block(draw, 13, 11, frame)
    draw_block(draw, 13, 12, frame)
    draw_block(draw, 18, 10, frame)
    draw_block(draw, 18, 11, frame)
    draw_block(draw, 18, 12, frame)
    
    # Chain hanging down
    draw_block(draw, 18, 14, chain)
    draw_block(draw, 19, 15, chain)
    draw_block(draw, 19, 16, chain)
    draw_block(draw, 18, 17, chain)
    
    return img

def draw_vr_headset():
    """VR headset - rare"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    body = '#2A2A2A'
    screen = '#00FFFF'  # Cyan glow
    accent = '#444444'
    
    # Big VR visor covering eyes
    for y in [8, 9, 10, 11, 12, 13, 14]:
        for x in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
            draw_block(draw, x, y, body)
    
    # Glowing screen area
    for y in [10, 11, 12]:
        for x in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
            draw_block(draw, x, y, screen)
    
    # Top accent
    for x in range(6, 20):
        draw_block(draw, x, 8, accent)
    
    # Strap hints
    draw_block(draw, 4, 10, body)
    draw_block(draw, 4, 11, body)
    draw_block(draw, 21, 10, body)
    draw_block(draw, 21, 11, body)
    
    return img

def draw_goggles():
    """Steampunk/swim goggles"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#8B4513'  # Brown leather
    lens = '#87CEEB'   # Light blue
    metal = '#B8860B'  # Dark gold
    
    # Left goggle (round)
    for y in [9, 10, 11, 12, 13]:
        for x in [7, 8, 9, 10, 11]:
            draw_block(draw, x, y, lens)
    # Frame
    for x in [7, 8, 9, 10, 11]:
        draw_block(draw, x, 8, frame)
        draw_block(draw, x, 14, frame)
    draw_block(draw, 6, 9, frame)
    draw_block(draw, 6, 10, frame)
    draw_block(draw, 6, 11, frame)
    draw_block(draw, 6, 12, frame)
    draw_block(draw, 6, 13, frame)
    draw_block(draw, 12, 9, metal)
    draw_block(draw, 12, 10, metal)
    draw_block(draw, 12, 11, metal)
    draw_block(draw, 12, 12, metal)
    draw_block(draw, 12, 13, metal)
    
    # Right goggle
    for y in [9, 10, 11, 12, 13]:
        for x in [14, 15, 16, 17, 18]:
            draw_block(draw, x, y, lens)
    # Frame
    for x in [14, 15, 16, 17, 18]:
        draw_block(draw, x, 8, frame)
        draw_block(draw, x, 14, frame)
    draw_block(draw, 13, 9, metal)
    draw_block(draw, 13, 10, metal)
    draw_block(draw, 13, 11, metal)
    draw_block(draw, 13, 12, metal)
    draw_block(draw, 13, 13, metal)
    draw_block(draw, 19, 9, frame)
    draw_block(draw, 19, 10, frame)
    draw_block(draw, 19, 11, frame)
    draw_block(draw, 19, 12, frame)
    draw_block(draw, 19, 13, frame)
    
    # Strap
    draw_block(draw, 5, 11, frame)
    draw_block(draw, 4, 11, frame)
    draw_block(draw, 20, 11, frame)
    draw_block(draw, 21, 11, frame)
    
    return img

def draw_clout_goggles():
    """Clout goggles (Kurt Cobain style)"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    frame = '#FFFFFF'
    lens = '#1A1A1A'
    
    # Small round lenses
    # Left
    for y in [10, 11, 12]:
        for x in [8, 9, 10]:
            draw_block(draw, x, y, lens)
    draw_block(draw, 7, 10, frame)
    draw_block(draw, 7, 11, frame)
    draw_block(draw, 7, 12, frame)
    draw_block(draw, 11, 10, frame)
    draw_block(draw, 11, 11, frame)
    draw_block(draw, 11, 12, frame)
    for x in [8, 9, 10]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    
    # Right
    for y in [10, 11, 12]:
        for x in [15, 16, 17]:
            draw_block(draw, x, y, lens)
    draw_block(draw, 14, 10, frame)
    draw_block(draw, 14, 11, frame)
    draw_block(draw, 14, 12, frame)
    draw_block(draw, 18, 10, frame)
    draw_block(draw, 18, 11, frame)
    draw_block(draw, 18, 12, frame)
    for x in [15, 16, 17]:
        draw_block(draw, x, 9, frame)
        draw_block(draw, x, 13, frame)
    
    # Bridge
    draw_block(draw, 12, 11, frame)
    draw_block(draw, 13, 11, frame)
    
    # Temples
    draw_block(draw, 6, 11, frame)
    draw_block(draw, 19, 11, frame)
    
    return img

def main():
    print("Generating eyewear traits (256x256)...")
    
    eyewear = [
        ('glasses', draw_regular_glasses, 'common'),
        ('sunglasses', draw_sunglasses, 'common'),
        ('aviators', draw_aviators, 'uncommon'),
        ('3d_glasses', draw_3d_glasses, 'uncommon'),
        ('nerd_glasses', draw_nerd_glasses, 'common'),
        ('eye_patch', draw_eye_patch, 'uncommon'),
        ('monocle', draw_monocle, 'rare'),
        ('vr_headset', draw_vr_headset, 'rare'),
        ('goggles', draw_goggles, 'uncommon'),
        ('clout_goggles', draw_clout_goggles, 'uncommon'),
    ]
    
    for name, func, rarity in eyewear:
        img = func()
        filename = f"eyewear_{name}_{rarity}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    print(f"\nDone! {len(eyewear)} eyewear styles saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
