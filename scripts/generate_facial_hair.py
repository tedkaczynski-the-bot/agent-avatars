#!/usr/bin/env python3
"""
Generate facial hair trait layers for CryptoPunks-style faces (male)
256x256 with transparency
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'facial_hair')
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

# Face area: chin around y=20-22, cheeks y=15-19

def draw_stubble(color='#2C1608'):
    """5 o'clock shadow stubble"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Dotted stubble pattern on chin and cheeks
    stubble_positions = [
        (9, 18), (11, 18), (13, 18), (15, 18), (17, 18),
        (10, 19), (12, 19), (14, 19), (16, 19),
        (11, 20), (13, 20), (15, 20),
        (12, 21), (14, 21),
        (8, 16), (8, 18), (17, 16), (17, 18),
    ]
    
    for x, y in stubble_positions:
        draw_block(draw, x, y, color)
    
    return img

def draw_goatee(color='#2C1608'):
    """Goatee (chin beard)"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Chin area
    for x in range(11, 16):
        draw_block(draw, x, 19, color)
        draw_block(draw, x, 20, color)
    for x in range(12, 15):
        draw_block(draw, x, 21, color)
    draw_block(draw, 13, 22, color)
    
    return img

def draw_mustache(color='#2C1608'):
    """Classic mustache"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Mustache above lip
    for x in range(10, 17):
        draw_block(draw, x, 16, color)
    draw_block(draw, 9, 16, color)
    draw_block(draw, 17, 16, color)
    
    # Slight droop at ends
    draw_block(draw, 9, 17, color)
    draw_block(draw, 17, 17, color)
    
    return img

def draw_handlebar(color='#2C1608'):
    """Handlebar mustache"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Center mustache
    for x in range(11, 16):
        draw_block(draw, x, 16, color)
    
    # Curled ends
    draw_block(draw, 10, 16, color)
    draw_block(draw, 9, 15, color)
    draw_block(draw, 8, 14, color)
    draw_block(draw, 7, 14, color)
    
    draw_block(draw, 16, 16, color)
    draw_block(draw, 17, 15, color)
    draw_block(draw, 18, 14, color)
    draw_block(draw, 19, 14, color)
    
    return img

def draw_full_beard(color='#2C1608'):
    """Full beard"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Mustache
    for x in range(10, 17):
        draw_block(draw, x, 16, color)
    
    # Cheek coverage
    for y in range(16, 21):
        draw_block(draw, 8, y, color)
        draw_block(draw, 9, y, color)
        draw_block(draw, 17, y, color)
        draw_block(draw, 18, y, color)
    
    # Chin beard
    for y in range(18, 23):
        for x in range(10, 17):
            draw_block(draw, x, y, color)
    
    # Taper at bottom
    for x in range(11, 16):
        draw_block(draw, x, 23, color)
    for x in range(12, 15):
        draw_block(draw, x, 24, color)
    
    return img

def draw_chinstrap(color='#2C1608'):
    """Chinstrap beard"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Thin line along jaw
    for y in range(14, 20):
        draw_block(draw, 7, y, color)
        draw_block(draw, 18, y, color)
    
    # Under chin
    for x in range(8, 18):
        draw_block(draw, x, 20, color)
    for x in range(10, 16):
        draw_block(draw, x, 21, color)
    
    return img

def draw_soul_patch(color='#2C1608'):
    """Small soul patch"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Small patch under lip
    draw_block(draw, 12, 18, color)
    draw_block(draw, 13, 18, color)
    draw_block(draw, 14, 18, color)
    draw_block(draw, 13, 19, color)
    
    return img

def draw_mutton_chops(color='#2C1608'):
    """Mutton chop sideburns"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Left chop
    for y in range(10, 20):
        draw_block(draw, 6, y, color)
        draw_block(draw, 7, y, color)
    for y in range(14, 20):
        draw_block(draw, 8, y, color)
    for y in range(16, 19):
        draw_block(draw, 9, y, color)
    
    # Right chop
    for y in range(10, 20):
        draw_block(draw, 18, y, color)
        draw_block(draw, 19, y, color)
    for y in range(14, 20):
        draw_block(draw, 17, y, color)
    for y in range(16, 19):
        draw_block(draw, 16, y, color)
    
    return img

def draw_vandyke(color='#2C1608'):
    """Van Dyke (mustache + goatee, no cheeks)"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Pointed mustache
    for x in range(11, 16):
        draw_block(draw, x, 16, color)
    draw_block(draw, 10, 16, color)
    draw_block(draw, 16, 16, color)
    
    # Goatee
    for x in range(11, 16):
        draw_block(draw, x, 19, color)
        draw_block(draw, x, 20, color)
    for x in range(12, 15):
        draw_block(draw, x, 21, color)
    draw_block(draw, 13, 22, color)
    
    return img

def draw_long_beard(color='#2C1608'):
    """Long wizard beard"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Full coverage
    for y in range(16, 22):
        for x in range(8, 18):
            draw_block(draw, x, y, color)
    
    # Long part
    for y in range(22, 26):
        for x in range(10, 16):
            draw_block(draw, x, y, color)
    
    # Taper to point
    for x in range(11, 15):
        draw_block(draw, x, 26, color)
    draw_block(draw, 12, 27, color)
    draw_block(draw, 13, 27, color)
    
    return img

def main():
    print("Generating facial hair traits (256x256)...")
    
    # Generate in multiple colors
    colors = {
        'black': '#1A1A1A',
        'brown': '#4A3728',
        'blonde': '#B8860B',
        'gray': '#808080',
        'red': '#8B4513',
    }
    
    styles = [
        ('stubble', draw_stubble, 'common'),
        ('goatee', draw_goatee, 'common'),
        ('mustache', draw_mustache, 'common'),
        ('handlebar', draw_handlebar, 'uncommon'),
        ('full_beard', draw_full_beard, 'uncommon'),
        ('chinstrap', draw_chinstrap, 'uncommon'),
        ('soul_patch', draw_soul_patch, 'common'),
        ('mutton_chops', draw_mutton_chops, 'rare'),
        ('vandyke', draw_vandyke, 'uncommon'),
        ('long_beard', draw_long_beard, 'rare'),
    ]
    
    count = 0
    for style_name, func, rarity in styles:
        for color_name, color_hex in colors.items():
            img = func(color_hex)
            filename = f"facial_{style_name}_{color_name}_{rarity}.png"
            img.save(os.path.join(OUTPUT_DIR, filename))
            print(f"  ✓ {filename}")
            count += 1
    
    print(f"\nDone! {count} facial hair styles saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
