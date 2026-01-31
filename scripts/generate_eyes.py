#!/usr/bin/env python3
"""
Generate eye trait layers for CryptoPunks-style faces
256x256 with transparency, positioned to align with base faces
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'eyes')
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIZE = 256
BLOCK = 10

# Eye colors
EYE_COLORS = {
    'black': '#1A1A1A',
    'brown': '#4A3728',
    'blue': '#3B82F6',
    'green': '#22C55E',
    'white': '#FFFFFF',
}

def draw_block(draw, x, y, color, block_size=BLOCK):
    """Draw a single pixel block"""
    draw.rectangle([x * block_size, y * block_size, 
                   (x + 1) * block_size - 1, (y + 1) * block_size - 1], 
                  fill=color)

def create_canvas():
    return Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))

# Eye positions (matching base face template)
# Left eye center around x=9-10, right eye around x=15-16
# Y position around 11-12

def draw_basic_eyes():
    """Simple dot eyes - classic punk style"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Simple black dots
    draw_block(draw, 9, 11, EYE_COLORS['black'])
    draw_block(draw, 16, 11, EYE_COLORS['black'])
    
    return img

def draw_regular_eyes():
    """Standard eyes with white and pupil"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # White of eyes
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    # Pupils (looking forward)
    draw_block(draw, 9, 11, EYE_COLORS['black'])
    draw_block(draw, 16, 11, EYE_COLORS['black'])
    
    return img

def draw_wide_eyes():
    """Big surprised eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Larger white area
    for dy in [10, 11, 12]:
        draw_block(draw, 8, dy, EYE_COLORS['white'])
        draw_block(draw, 9, dy, EYE_COLORS['white'])
        draw_block(draw, 10, dy, EYE_COLORS['white'])
        
        draw_block(draw, 15, dy, EYE_COLORS['white'])
        draw_block(draw, 16, dy, EYE_COLORS['white'])
        draw_block(draw, 17, dy, EYE_COLORS['white'])
    
    # Big pupils
    draw_block(draw, 9, 11, EYE_COLORS['black'])
    draw_block(draw, 9, 12, EYE_COLORS['black'])
    draw_block(draw, 16, 11, EYE_COLORS['black'])
    draw_block(draw, 16, 12, EYE_COLORS['black'])
    
    return img

def draw_narrow_eyes():
    """Squinting/suspicious eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Just a thin line
    draw_block(draw, 8, 11, EYE_COLORS['black'])
    draw_block(draw, 9, 11, EYE_COLORS['black'])
    draw_block(draw, 10, 11, EYE_COLORS['black'])
    
    draw_block(draw, 15, 11, EYE_COLORS['black'])
    draw_block(draw, 16, 11, EYE_COLORS['black'])
    draw_block(draw, 17, 11, EYE_COLORS['black'])
    
    return img

def draw_angry_eyes():
    """Angry eyes with furrowed brows"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    brow_color = '#2C1608'  # Dark brown brow
    
    # Angry brows (angled down toward center)
    draw_block(draw, 7, 9, brow_color)
    draw_block(draw, 8, 9, brow_color)
    draw_block(draw, 9, 10, brow_color)
    draw_block(draw, 10, 10, brow_color)
    
    draw_block(draw, 15, 10, brow_color)
    draw_block(draw, 16, 10, brow_color)
    draw_block(draw, 17, 9, brow_color)
    draw_block(draw, 18, 9, brow_color)
    
    # Eyes underneath
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['black'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['black'])
    
    return img

def draw_tired_eyes():
    """Sleepy/tired half-closed eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    lid_color = '#D4A574'  # Skin-ish color for eyelids
    
    # Half-closed lids
    draw_block(draw, 8, 11, lid_color)
    draw_block(draw, 9, 11, lid_color)
    draw_block(draw, 10, 11, lid_color)
    
    draw_block(draw, 15, 11, lid_color)
    draw_block(draw, 16, 11, lid_color)
    draw_block(draw, 17, 11, lid_color)
    
    # Just visible pupils below
    draw_block(draw, 9, 12, EYE_COLORS['black'])
    draw_block(draw, 16, 12, EYE_COLORS['black'])
    
    return img

def draw_side_eyes():
    """Looking to the side"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # White of eyes
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    # Pupils looking right
    draw_block(draw, 10, 11, EYE_COLORS['black'])
    draw_block(draw, 17, 11, EYE_COLORS['black'])
    
    return img

def draw_blue_eyes():
    """Blue colored eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # White of eyes
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    # Blue irises
    draw_block(draw, 9, 11, EYE_COLORS['blue'])
    draw_block(draw, 16, 11, EYE_COLORS['blue'])
    
    return img

def draw_green_eyes():
    """Green colored eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # White of eyes
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    # Green irises
    draw_block(draw, 9, 11, EYE_COLORS['green'])
    draw_block(draw, 16, 11, EYE_COLORS['green'])
    
    return img

def draw_purple_eyes():
    """Purple colored eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    purple = '#8B5CF6'
    
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    draw_block(draw, 9, 11, purple)
    draw_block(draw, 16, 11, purple)
    
    return img

def draw_red_eyes():
    """Red/crimson eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    red = '#DC143C'
    
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    draw_block(draw, 9, 11, red)
    draw_block(draw, 16, 11, red)
    
    return img

def draw_yellow_eyes():
    """Yellow/golden eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    yellow = '#FFD700'
    
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    draw_block(draw, 9, 11, yellow)
    draw_block(draw, 16, 11, yellow)
    
    return img

def draw_heterochromia():
    """Different colored eyes - one blue, one green"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    # Left eye blue, right eye green
    draw_block(draw, 9, 11, EYE_COLORS['blue'])
    draw_block(draw, 16, 11, EYE_COLORS['green'])
    
    return img

def draw_crying_eyes():
    """Eyes with tears"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    tear = '#87CEEB'
    
    # Regular eyes
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['blue'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['blue'])
    
    # Tears running down
    draw_block(draw, 9, 12, tear)
    draw_block(draw, 9, 13, tear)
    draw_block(draw, 16, 12, tear)
    draw_block(draw, 16, 13, tear)
    
    return img

def draw_wink():
    """Winking - one eye closed"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # Left eye open
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['black'])
    
    # Right eye winking (closed line)
    draw_block(draw, 15, 11, EYE_COLORS['black'])
    draw_block(draw, 16, 11, EYE_COLORS['black'])
    draw_block(draw, 17, 11, EYE_COLORS['black'])
    
    return img

def draw_laser_eyes():
    """RARE - Laser beam eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    laser_red = '#FF0000'
    laser_orange = '#FF6600'
    laser_yellow = '#FFFF00'
    
    # Glowing red eyes
    draw_block(draw, 8, 11, laser_orange)
    draw_block(draw, 9, 11, laser_red)
    draw_block(draw, 10, 11, laser_orange)
    
    draw_block(draw, 15, 11, laser_orange)
    draw_block(draw, 16, 11, laser_red)
    draw_block(draw, 17, 11, laser_orange)
    
    # Laser beams shooting out
    for x in range(18, 26):
        draw_block(draw, x, 11, laser_red)
    for x in range(0, 8):
        draw_block(draw, x, 11, laser_red)
    
    # Glow effect
    draw_block(draw, 9, 10, laser_yellow)
    draw_block(draw, 9, 12, laser_yellow)
    draw_block(draw, 16, 10, laser_yellow)
    draw_block(draw, 16, 12, laser_yellow)
    
    return img

def draw_robot_eyes():
    """RARE - Robot/cyborg eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    metal = '#708090'      # Slate gray
    glow = '#00FFFF'       # Cyan glow
    dark = '#2F4F4F'       # Dark slate
    
    # Metal eye sockets
    for dy in [10, 11, 12]:
        draw_block(draw, 7, dy, metal)
        draw_block(draw, 8, dy, dark)
        draw_block(draw, 9, dy, dark)
        draw_block(draw, 10, dy, dark)
        draw_block(draw, 11, dy, metal)
        
        draw_block(draw, 14, dy, metal)
        draw_block(draw, 15, dy, dark)
        draw_block(draw, 16, dy, dark)
        draw_block(draw, 17, dy, dark)
        draw_block(draw, 18, dy, metal)
    
    # Glowing centers
    draw_block(draw, 9, 11, glow)
    draw_block(draw, 16, 11, glow)
    
    return img

def draw_heart_eyes():
    """RARE - Heart eyes (love struck)"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    pink = '#FF69B4'
    red = '#FF1493'
    
    # Left heart
    draw_block(draw, 8, 10, red)
    draw_block(draw, 10, 10, red)
    draw_block(draw, 7, 11, pink)
    draw_block(draw, 8, 11, red)
    draw_block(draw, 9, 11, red)
    draw_block(draw, 10, 11, red)
    draw_block(draw, 11, 11, pink)
    draw_block(draw, 8, 12, pink)
    draw_block(draw, 9, 12, red)
    draw_block(draw, 10, 12, pink)
    draw_block(draw, 9, 13, pink)
    
    # Right heart
    draw_block(draw, 15, 10, red)
    draw_block(draw, 17, 10, red)
    draw_block(draw, 14, 11, pink)
    draw_block(draw, 15, 11, red)
    draw_block(draw, 16, 11, red)
    draw_block(draw, 17, 11, red)
    draw_block(draw, 18, 11, pink)
    draw_block(draw, 15, 12, pink)
    draw_block(draw, 16, 12, red)
    draw_block(draw, 17, 12, pink)
    draw_block(draw, 16, 13, pink)
    
    return img

def draw_crossed_eyes():
    """Derpy crossed eyes"""
    img = create_canvas()
    draw = ImageDraw.Draw(img)
    
    # White of eyes
    draw_block(draw, 8, 11, EYE_COLORS['white'])
    draw_block(draw, 9, 11, EYE_COLORS['white'])
    draw_block(draw, 10, 11, EYE_COLORS['white'])
    
    draw_block(draw, 15, 11, EYE_COLORS['white'])
    draw_block(draw, 16, 11, EYE_COLORS['white'])
    draw_block(draw, 17, 11, EYE_COLORS['white'])
    
    # Pupils looking inward (crossed)
    draw_block(draw, 10, 11, EYE_COLORS['black'])
    draw_block(draw, 15, 11, EYE_COLORS['black'])
    
    return img

def main():
    print("Generating eye traits (256x256)...")
    
    eyes = [
        ('basic', draw_basic_eyes, 'common'),
        ('regular', draw_regular_eyes, 'common'),
        ('wide', draw_wide_eyes, 'common'),
        ('narrow', draw_narrow_eyes, 'common'),
        ('angry', draw_angry_eyes, 'uncommon'),
        ('tired', draw_tired_eyes, 'uncommon'),
        ('side', draw_side_eyes, 'common'),
        ('blue', draw_blue_eyes, 'uncommon'),
        ('green', draw_green_eyes, 'uncommon'),
        ('purple', draw_purple_eyes, 'uncommon'),
        ('red', draw_red_eyes, 'rare'),
        ('yellow', draw_yellow_eyes, 'rare'),
        ('heterochromia', draw_heterochromia, 'rare'),
        ('crying', draw_crying_eyes, 'uncommon'),
        ('wink', draw_wink, 'uncommon'),
        ('crossed', draw_crossed_eyes, 'uncommon'),
        ('laser', draw_laser_eyes, 'rare'),
        ('robot', draw_robot_eyes, 'rare'),
        ('heart', draw_heart_eyes, 'rare'),
    ]
    
    for name, func, rarity in eyes:
        img = func()
        filename = f"eyes_{name}_{rarity}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    print(f"\nDone! {len(eyes)} eye styles saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
