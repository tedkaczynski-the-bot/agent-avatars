#!/usr/bin/env python3
"""
Generate hair trait layers for CryptoPunks-style faces
256x256 with transparency
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'hair')
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIZE = 256
BLOCK = 10

# Hair colors
HAIR_COLORS = {
    'black': '#090806',
    'dark_brown': '#2C1608',
    'brown': '#6A4E42',
    'auburn': '#B55239',
    'blonde': '#D6B370',
    'gray': '#AFAFAF',
    'white': '#E6E6E6',
    'purple': '#A855F7',
    'pink': '#EC4899',
    'blue': '#3B82F6',
    'green': '#22C55E',
    'red': '#EF4444',
    'orange': '#F97316',
}

def draw_block(draw, x, y, color, block_size=BLOCK):
    """Draw a single pixel block"""
    draw.rectangle([x * block_size, y * block_size, 
                   (x + 1) * block_size - 1, (y + 1) * block_size - 1], 
                  fill=color)

def create_canvas():
    return Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))

def draw_bald():
    """Bald with shine"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Shiny bald spot highlight
    shine = '#FFFFFF'
    draw_block(draw, 11, 5, shine)
    draw_block(draw, 12, 5, shine)
    draw_block(draw, 11, 6, shine)
    
    return img

def draw_buzz(color):
    """Short buzz cut"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Short stubble on top of head
    for x in range(8, 18):
        draw_block(draw, x, 4, color)
        draw_block(draw, x, 5, color)
    for x in range(9, 17):
        draw_block(draw, x, 3, color)
    
    return img

def draw_short(color):
    """Short regular hair"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Darker shade
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    dark = f'#{max(0,r-30):02x}{max(0,g-30):02x}{max(0,b-30):02x}'
    
    # Top of head coverage
    for x in range(7, 19):
        draw_block(draw, x, 4, color)
        draw_block(draw, x, 5, color)
    for x in range(8, 18):
        draw_block(draw, x, 3, color)
    for x in range(9, 17):
        draw_block(draw, x, 2, color)
    
    # Sides
    for y in range(5, 9):
        draw_block(draw, 6, y, color)
        draw_block(draw, 19, y, color)
    
    return img

def draw_spiky(color):
    """Spiky punk hair"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Base hair
    for x in range(7, 19):
        draw_block(draw, x, 4, color)
        draw_block(draw, x, 5, color)
    
    # Spikes going up
    spikes = [8, 10, 12, 14, 16]
    for spike_x in spikes:
        draw_block(draw, spike_x, 3, color)
        draw_block(draw, spike_x, 2, color)
        draw_block(draw, spike_x, 1, color)
    
    # Side spikes
    draw_block(draw, 6, 5, color)
    draw_block(draw, 5, 4, color)
    draw_block(draw, 19, 5, color)
    draw_block(draw, 20, 4, color)
    
    return img

def draw_mohawk(color):
    """Classic mohawk"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Tall center strip
    for y in range(0, 6):
        draw_block(draw, 12, y, color)
        draw_block(draw, 13, y, color)
    
    # Wider at base
    for x in range(11, 15):
        draw_block(draw, x, 5, color)
        draw_block(draw, x, 6, color)
    
    return img

def draw_mohawk_tall(color):
    """Extra tall mohawk"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Very tall center strip
    for y in range(0, 6):
        for x in range(11, 15):
            draw_block(draw, x, y, color)
    
    # Pointed top
    draw_block(draw, 12, -1 if -1 >= 0 else 0, color)  # Can't go negative, skip
    draw_block(draw, 13, 0, color)
    
    return img

def draw_messy(color):
    """Messy/wild hair"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Irregular clumps
    positions = [
        (7, 3), (8, 2), (9, 3), (10, 1), (11, 2), (12, 3), (13, 1), 
        (14, 2), (15, 3), (16, 2), (17, 3), (18, 4),
        (6, 5), (7, 4), (8, 5), (17, 4), (18, 5), (19, 5),
        (6, 6), (19, 6), (5, 7), (20, 7),
    ]
    
    for x, y in positions:
        draw_block(draw, x, y, color)
    
    # Fill base
    for x in range(7, 19):
        draw_block(draw, x, 4, color)
        draw_block(draw, x, 5, color)
    
    return img

def draw_long_male(color):
    """Long flowing hair - for wider male head"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Top - covers male head (face_left=6, face_right=20)
    for x in range(7, 19):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
        draw_block(draw, x, 5, color)
    
    # Sides going down
    for y in range(5, 20):
        draw_block(draw, 5, y, color)
        draw_block(draw, 6, y, color)
        draw_block(draw, 19, y, color)
        draw_block(draw, 20, y, color)
    
    # Widens at bottom
    for y in range(18, 22):
        draw_block(draw, 4, y, color)
        draw_block(draw, 21, y, color)
    
    return img

def draw_long_female(color):
    """Long flowing hair - for female head. Touches face at x=7 and x=18."""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Top - covers female head crown
    for x in range(9, 17):
        draw_block(draw, x, 2, color)
    for x in range(8, 18):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    
    # Sides going down - TIGHT against face (touching x=7 and x=18)
    for y in range(4, 19):
        draw_block(draw, 6, y, color)
        draw_block(draw, 7, y, color)  # Touch face left
        draw_block(draw, 18, y, color)  # Touch face right
        draw_block(draw, 19, y, color)
    
    # Widens at shoulders/ends
    for y in range(16, 21):
        draw_block(draw, 5, y, color)
        draw_block(draw, 20, y, color)
    
    # Ends taper
    for x in [6, 7, 18, 19]:
        draw_block(draw, x, 20, color)
    
    return img

def draw_afro_male(color):
    """Big afro - for wider male head"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Large round shape for male head
    for x in range(9, 17):
        draw_block(draw, x, 0, color)
    for x in range(7, 19):
        draw_block(draw, x, 1, color)
    for x in range(5, 21):
        draw_block(draw, x, 2, color)
    for x in range(4, 22):
        for y in range(3, 6):
            draw_block(draw, x, y, color)
    
    # Sides frame the wider face
    for y in range(6, 11):
        draw_block(draw, 4, y, color)
        draw_block(draw, 5, y, color)
        draw_block(draw, 20, y, color)
        draw_block(draw, 21, y, color)
    
    return img

def draw_afro_female(color):
    """Big afro - for female head. Hair touches face at x=7 and x=18."""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Big round afro shape - top dome
    for x in range(10, 16):
        draw_block(draw, x, 0, color)
    for x in range(8, 18):
        draw_block(draw, x, 1, color)
    for x in range(6, 20):
        draw_block(draw, x, 2, color)
    for x in range(5, 21):
        draw_block(draw, x, 3, color)
    for x in range(4, 22):
        draw_block(draw, x, 4, color)
    
    # Connect to sides - touching face edges
    for x in range(4, 22):
        draw_block(draw, x, 5, color)
    
    # Side puffs - TOUCH the face (x=7 left edge, x=18 right edge)
    for y in range(6, 10):
        draw_block(draw, 4, y, color)
        draw_block(draw, 5, y, color)
        draw_block(draw, 6, y, color)
        draw_block(draw, 7, y, color)  # Touch face left edge
        draw_block(draw, 18, y, color)  # Touch face right edge
        draw_block(draw, 19, y, color)
        draw_block(draw, 20, y, color)
        draw_block(draw, 21, y, color)
    
    return img

def draw_ponytail_female(color):
    """Ponytail - for female head"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Top pulled back - fits female head
    for x in range(8, 18):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    
    # Sides slicked
    draw_block(draw, 7, 5, color)
    draw_block(draw, 18, 5, color)
    
    # Ponytail in back (visible on side)
    for y in range(6, 17):
        draw_block(draw, 19, y, color)
        draw_block(draw, 20, y, color)
    
    # Tie
    draw_block(draw, 19, 7, '#4A4A4A')
    draw_block(draw, 20, 7, '#4A4A4A')
    
    return img

def draw_ponytail_male(color):
    """Ponytail/man bun - for male head"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Top pulled back - fits male head
    for x in range(7, 19):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    
    # Sides slicked
    draw_block(draw, 6, 5, color)
    draw_block(draw, 19, 5, color)
    
    # Man bun at back
    for y in range(5, 10):
        draw_block(draw, 20, y, color)
        draw_block(draw, 21, y, color)
    draw_block(draw, 20, 4, color)
    
    # Tie
    draw_block(draw, 20, 6, '#4A4A4A')
    
    return img

def draw_pigtails_female(color):
    """Pigtails - female only. Hair touches face at x=7 and x=18."""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Top hair covers crown
    for x in range(7, 19):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    
    # Hair flows to sides - touching face
    for x in range(5, 9):  # Goes to x=8, touching face at x=7-8
        draw_block(draw, x, 5, color)
    for x in range(17, 21):  # Goes to x=17, touching face at x=17-18
        draw_block(draw, x, 5, color)
    
    # Left pigtail - touches face edge
    for y in range(6, 15):
        draw_block(draw, 5, y, color)
        draw_block(draw, 6, y, color)
        draw_block(draw, 7, y, color)  # Touch face
    # Puff at end
    draw_block(draw, 4, 12, color)
    draw_block(draw, 4, 13, color)
    draw_block(draw, 4, 14, color)
    draw_block(draw, 5, 15, color)
    draw_block(draw, 6, 15, color)
    
    # Right pigtail - touches face edge
    for y in range(6, 15):
        draw_block(draw, 18, y, color)  # Touch face
        draw_block(draw, 19, y, color)
        draw_block(draw, 20, y, color)
    # Puff at end
    draw_block(draw, 21, 12, color)
    draw_block(draw, 21, 13, color)
    draw_block(draw, 21, 14, color)
    draw_block(draw, 19, 15, color)
    draw_block(draw, 20, 15, color)
    
    # Hair ties (red)
    draw_block(draw, 6, 6, '#EF4444')
    draw_block(draw, 7, 6, '#EF4444')
    draw_block(draw, 18, 6, '#EF4444')
    draw_block(draw, 19, 6, '#EF4444')
    
    return img

def draw_bangs_female(color):
    """Front bangs - for female head"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Top hair - female width
    for x in range(8, 18):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    
    # Bangs hanging over forehead
    for x in range(8, 17):
        draw_block(draw, x, 6, color)
        draw_block(draw, x, 7, color)
    for x in range(9, 16):
        draw_block(draw, x, 8, color)
    
    # Sides
    for y in range(5, 10):
        draw_block(draw, 6, y, color)
        draw_block(draw, 7, y, color)
        draw_block(draw, 18, y, color)
        draw_block(draw, 19, y, color)
    
    return img

def draw_bangs_male(color):
    """Front bangs/fringe - for male head"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Top hair - male width
    for x in range(7, 19):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, color)
    
    # Bangs hanging over forehead
    for x in range(7, 18):
        draw_block(draw, x, 6, color)
        draw_block(draw, x, 7, color)
    for x in range(8, 17):
        draw_block(draw, x, 8, color)
    
    # Sides
    for y in range(5, 9):
        draw_block(draw, 5, y, color)
        draw_block(draw, 6, y, color)
        draw_block(draw, 19, y, color)
        draw_block(draw, 20, y, color)
    
    return img

def draw_curly(color):
    """Curly hair"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Puffy curls pattern
    curl_positions = [
        (8, 2), (10, 1), (12, 2), (14, 1), (16, 2),
        (7, 3), (9, 3), (11, 3), (13, 3), (15, 3), (17, 3),
        (6, 4), (8, 4), (10, 4), (12, 4), (14, 4), (16, 4), (18, 4),
        (6, 5), (7, 5), (8, 5), (17, 5), (18, 5), (19, 5),
        (5, 6), (6, 6), (19, 6), (20, 6),
        (5, 7), (20, 7),
    ]
    
    for x, y in curl_positions:
        draw_block(draw, x, y, color)
    
    # Fill middle
    for x in range(9, 17):
        draw_block(draw, x, 5, color)
    
    return img

def draw_slicked(color):
    """Slicked back hair"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Darker shade for depth
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    dark = f'#{max(0,r-40):02x}{max(0,g-40):02x}{max(0,b-40):02x}'
    
    # Smooth top swept back
    for x in range(8, 18):
        draw_block(draw, x, 3, color)
        draw_block(draw, x, 4, dark)
    
    # Lines showing slick direction
    draw_block(draw, 9, 4, color)
    draw_block(draw, 12, 4, color)
    draw_block(draw, 15, 4, color)
    
    # Sides
    for y in range(5, 8):
        draw_block(draw, 6, y, color)
        draw_block(draw, 19, y, color)
    
    return img

def draw_cap_hair(color):
    """Hair peeking out from under cap (partial)"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Just sides visible
    for y in range(8, 14):
        draw_block(draw, 5, y, color)
        draw_block(draw, 6, y, color)
        draw_block(draw, 19, y, color)
        draw_block(draw, 20, y, color)
    
    return img

def main():
    print("Generating hair traits (256x256)...")
    
    # Unisex styles (work on both)
    unisex = [
        ('bald', draw_bald, None, 'common'),
        ('buzz', draw_buzz, 'black', 'common'),
        ('buzz', draw_buzz, 'blonde', 'common'),
        ('short', draw_short, 'black', 'common'),
        ('short', draw_short, 'brown', 'common'),
        ('short', draw_short, 'blonde', 'common'),
        ('short', draw_short, 'gray', 'uncommon'),
        ('spiky', draw_spiky, 'black', 'uncommon'),
        ('spiky', draw_spiky, 'blonde', 'uncommon'),
        ('spiky', draw_spiky, 'purple', 'rare'),
        ('mohawk', draw_mohawk, 'black', 'uncommon'),
        ('mohawk', draw_mohawk, 'red', 'rare'),
        ('mohawk', draw_mohawk, 'green', 'rare'),
        ('mohawk_tall', draw_mohawk_tall, 'purple', 'rare'),
        ('messy', draw_messy, 'brown', 'common'),
        ('messy', draw_messy, 'auburn', 'common'),
        ('curly', draw_curly, 'brown', 'common'),
        ('curly', draw_curly, 'blonde', 'common'),
        ('slicked', draw_slicked, 'black', 'uncommon'),
        ('cap_hair', draw_cap_hair, 'brown', 'common'),
    ]
    
    # Male-specific styles
    male = [
        ('long_male', draw_long_male, 'black', 'common'),
        ('long_male', draw_long_male, 'brown', 'common'),
        ('afro_male', draw_afro_male, 'black', 'uncommon'),
        ('afro_male', draw_afro_male, 'brown', 'uncommon'),
        ('ponytail_male', draw_ponytail_male, 'black', 'common'),
        ('ponytail_male', draw_ponytail_male, 'brown', 'common'),
        ('bangs_male', draw_bangs_male, 'black', 'common'),
        ('bangs_male', draw_bangs_male, 'brown', 'common'),
    ]
    
    # Female-specific styles
    female = [
        ('long_female', draw_long_female, 'black', 'common'),
        ('long_female', draw_long_female, 'blonde', 'common'),
        ('long_female', draw_long_female, 'pink', 'rare'),
        ('afro_female', draw_afro_female, 'black', 'uncommon'),
        ('afro_female', draw_afro_female, 'brown', 'uncommon'),
        ('ponytail_female', draw_ponytail_female, 'black', 'common'),
        ('ponytail_female', draw_ponytail_female, 'brown', 'common'),
        ('pigtails_female', draw_pigtails_female, 'blonde', 'uncommon'),
        ('pigtails_female', draw_pigtails_female, 'pink', 'rare'),
        ('bangs_female', draw_bangs_female, 'black', 'common'),
        ('bangs_female', draw_bangs_female, 'auburn', 'common'),
    ]
    
    all_styles = unisex + male + female
    
    for name, func, color, rarity in all_styles:
        if color:
            img = func(HAIR_COLORS[color])
            filename = f"hair_{name}_{color}_{rarity}.png"
        else:
            img = func()
            filename = f"hair_{name}_{rarity}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    print(f"\nDone! {len(all_styles)} hair styles saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
