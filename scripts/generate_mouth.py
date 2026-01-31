#!/usr/bin/env python3
"""
Generate mouth trait layers for CryptoPunks-style faces
256x256 with transparency, positioned around y=17-18
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'mouth')
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

# Mouth is around x=10-16, y=17-18

def draw_smile():
    """Happy smile"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    teeth = '#FFFFFF'
    
    # Curved smile
    draw_block(draw, 10, 17, lip)
    draw_block(draw, 11, 18, lip)
    for x in range(12, 15):
        draw_block(draw, x, 18, teeth)
    draw_block(draw, 15, 18, lip)
    draw_block(draw, 16, 17, lip)
    
    return img

def draw_big_smile():
    """Big toothy grin"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#C06060'
    teeth = '#FFFFFF'
    
    # Wide smile with teeth
    draw_block(draw, 9, 17, lip)
    for x in range(10, 17):
        draw_block(draw, x, 17, teeth)
    draw_block(draw, 17, 17, lip)
    
    # Bottom lip
    for x in range(10, 17):
        draw_block(draw, x, 18, lip)
    
    return img

def draw_frown():
    """Sad frown"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    
    # Downturned mouth
    draw_block(draw, 10, 18, lip)
    draw_block(draw, 11, 17, lip)
    for x in range(12, 15):
        draw_block(draw, x, 17, lip)
    draw_block(draw, 15, 17, lip)
    draw_block(draw, 16, 18, lip)
    
    return img

def draw_neutral():
    """Neutral/straight mouth"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    
    for x in range(11, 16):
        draw_block(draw, x, 17, lip)
    
    return img

def draw_smirk():
    """One-sided smirk"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    
    draw_block(draw, 10, 17, lip)
    for x in range(11, 15):
        draw_block(draw, x, 17, lip)
    draw_block(draw, 15, 17, lip)
    draw_block(draw, 16, 16, lip)  # Raised corner
    
    return img

def draw_open_mouth():
    """Surprised open mouth"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#C06060'
    inside = '#4A1A1A'
    
    # Open O shape
    for x in range(11, 16):
        draw_block(draw, x, 16, lip)
        draw_block(draw, x, 19, lip)
    draw_block(draw, 10, 17, lip)
    draw_block(draw, 10, 18, lip)
    draw_block(draw, 16, 17, lip)
    draw_block(draw, 16, 18, lip)
    
    # Dark inside
    for x in range(11, 16):
        draw_block(draw, x, 17, inside)
        draw_block(draw, x, 18, inside)
    
    return img

def draw_tongue_out():
    """Tongue sticking out"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    tongue = '#FF6B6B'
    
    # Mouth
    for x in range(11, 16):
        draw_block(draw, x, 17, lip)
    
    # Tongue
    draw_block(draw, 12, 18, tongue)
    draw_block(draw, 13, 18, tongue)
    draw_block(draw, 14, 18, tongue)
    draw_block(draw, 13, 19, tongue)
    
    return img

def draw_cigarette():
    """Cigarette in mouth"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    cig_white = '#F5F5F5'
    cig_orange = '#FF8C00'
    smoke = '#CCCCCC'
    
    # Mouth holding cig
    for x in range(11, 14):
        draw_block(draw, x, 17, lip)
    
    # Cigarette
    draw_block(draw, 14, 17, cig_orange)  # Filter
    draw_block(draw, 15, 17, cig_white)
    draw_block(draw, 16, 17, cig_white)
    draw_block(draw, 17, 17, cig_white)
    draw_block(draw, 18, 17, cig_white)
    
    # Lit end
    draw_block(draw, 19, 17, '#FF4500')
    
    # Smoke
    draw_block(draw, 19, 16, smoke)
    draw_block(draw, 20, 15, smoke)
    draw_block(draw, 19, 14, smoke)
    draw_block(draw, 20, 13, smoke)
    
    return img

def draw_pipe():
    """Smoking pipe"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    pipe = '#4A2F1A'
    bowl = '#6B4226'
    smoke = '#CCCCCC'
    
    # Mouth
    for x in range(11, 14):
        draw_block(draw, x, 17, lip)
    
    # Pipe stem
    draw_block(draw, 14, 17, pipe)
    draw_block(draw, 15, 17, pipe)
    draw_block(draw, 16, 17, pipe)
    draw_block(draw, 17, 17, pipe)
    
    # Pipe bowl
    draw_block(draw, 17, 16, bowl)
    draw_block(draw, 18, 16, bowl)
    draw_block(draw, 17, 15, bowl)
    draw_block(draw, 18, 15, bowl)
    draw_block(draw, 18, 17, bowl)
    
    # Smoke
    draw_block(draw, 17, 14, smoke)
    draw_block(draw, 18, 13, smoke)
    draw_block(draw, 17, 12, smoke)
    
    return img

def draw_vape():
    """Vape pen"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    vape = '#2A2A2A'
    led = '#00FF00'
    cloud = '#E8E8E8'
    
    # Mouth
    for x in range(11, 14):
        draw_block(draw, x, 17, lip)
    
    # Vape pen
    draw_block(draw, 14, 17, vape)
    draw_block(draw, 15, 17, vape)
    draw_block(draw, 16, 17, vape)
    draw_block(draw, 17, 17, vape)
    draw_block(draw, 18, 17, led)
    
    # Big vape cloud
    for x in range(17, 22):
        draw_block(draw, x, 15, cloud)
        draw_block(draw, x, 16, cloud)
    for x in range(18, 23):
        draw_block(draw, x, 14, cloud)
    draw_block(draw, 19, 13, cloud)
    draw_block(draw, 20, 13, cloud)
    
    return img

def draw_bubblegum():
    """Bubble gum bubble"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#C06060'
    gum = '#FF69B4'
    highlight = '#FFB6C1'
    
    # Mouth
    for x in range(11, 14):
        draw_block(draw, x, 17, lip)
    
    # Bubble
    for y in range(15, 20):
        for x in range(14, 20):
            draw_block(draw, x, y, gum)
    draw_block(draw, 13, 16, gum)
    draw_block(draw, 13, 17, gum)
    draw_block(draw, 13, 18, gum)
    draw_block(draw, 20, 16, gum)
    draw_block(draw, 20, 17, gum)
    draw_block(draw, 20, 18, gum)
    
    # Highlight
    draw_block(draw, 15, 16, highlight)
    draw_block(draw, 16, 16, highlight)
    
    return img

def draw_medical_mask():
    """Medical face mask"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    mask = '#87CEEB'  # Light blue
    strap = '#FFFFFF'
    fold = '#6BB3D9'
    
    # Mask covering lower face
    for y in range(14, 21):
        for x in range(8, 18):
            draw_block(draw, x, y, mask)
    
    # Folds
    for x in range(8, 18):
        draw_block(draw, x, 16, fold)
        draw_block(draw, x, 18, fold)
    
    # Straps
    draw_block(draw, 7, 14, strap)
    draw_block(draw, 6, 13, strap)
    draw_block(draw, 18, 14, strap)
    draw_block(draw, 19, 13, strap)
    
    return img

def draw_fangs():
    """Vampire fangs"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B0000'  # Dark red
    fang = '#FFFFFF'
    
    # Slightly open mouth
    for x in range(10, 17):
        draw_block(draw, x, 17, lip)
    
    # Fangs
    draw_block(draw, 11, 18, fang)
    draw_block(draw, 11, 19, fang)
    draw_block(draw, 15, 18, fang)
    draw_block(draw, 15, 19, fang)
    
    return img

def draw_gold_teeth():
    """Gold grillz"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#8B4513'
    gold = '#FFD700'
    dark_gold = '#DAA520'
    
    # Smile showing teeth
    draw_block(draw, 9, 17, lip)
    for x in range(10, 17):
        draw_block(draw, x, 17, gold)
    draw_block(draw, 17, 17, lip)
    
    # Gold detail
    draw_block(draw, 11, 17, dark_gold)
    draw_block(draw, 13, 17, dark_gold)
    draw_block(draw, 15, 17, dark_gold)
    
    # Bottom lip
    for x in range(11, 16):
        draw_block(draw, x, 18, lip)
    
    return img

def draw_lipstick():
    """Red lipstick"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    red = '#DC143C'
    dark = '#8B0000'
    
    # Full red lips
    draw_block(draw, 10, 17, dark)
    for x in range(11, 16):
        draw_block(draw, x, 17, red)
    draw_block(draw, 16, 17, dark)
    
    # Bottom lip
    for x in range(11, 16):
        draw_block(draw, x, 18, red)
    
    return img

def draw_buck_teeth():
    """Buck teeth"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lip = '#C06060'
    teeth = '#FFFFFF'
    
    # Lips
    for x in range(10, 17):
        draw_block(draw, x, 17, lip)
    
    # Two big front teeth
    draw_block(draw, 12, 18, teeth)
    draw_block(draw, 13, 18, teeth)
    draw_block(draw, 14, 18, teeth)
    draw_block(draw, 12, 19, teeth)
    draw_block(draw, 13, 19, teeth)
    draw_block(draw, 14, 19, teeth)
    
    return img

def main():
    print("Generating mouth traits (256x256)...")
    
    mouths = [
        ('smile', draw_smile, 'common'),
        ('big_smile', draw_big_smile, 'common'),
        ('frown', draw_frown, 'common'),
        ('neutral', draw_neutral, 'common'),
        ('smirk', draw_smirk, 'common'),
        ('open', draw_open_mouth, 'uncommon'),
        ('tongue', draw_tongue_out, 'uncommon'),
        ('cigarette', draw_cigarette, 'uncommon'),
        ('pipe', draw_pipe, 'uncommon'),
        ('vape', draw_vape, 'uncommon'),
        ('bubblegum', draw_bubblegum, 'uncommon'),
        ('medical_mask', draw_medical_mask, 'uncommon'),
        ('fangs', draw_fangs, 'rare'),
        ('gold_teeth', draw_gold_teeth, 'rare'),
        ('lipstick', draw_lipstick, 'common'),
        ('buck_teeth', draw_buck_teeth, 'uncommon'),
    ]
    
    for name, func, rarity in mouths:
        img = func()
        filename = f"mouth_{name}_{rarity}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    print(f"\nDone! {len(mouths)} mouth styles saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
