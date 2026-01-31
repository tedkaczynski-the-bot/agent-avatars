#!/usr/bin/env python3
"""
Composite punk layers together for preview
"""

from PIL import Image
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'previews')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Background colors
BACKGROUNDS = {
    'cream': '#FEF3C7',
    'blue': '#DBEAFE',
    'pink': '#FCE7F3',
    'green': '#D1FAE5',
    'gray': '#E5E7EB',
    'dark': '#1F2937',
    'purple': '#7C3AED',
    'orange': '#F97316',
}

def create_background(color, size=256):
    """Create a solid color background"""
    img = Image.new('RGBA', (size, size), color)
    return img

def composite_punk(base_name, eyes_name=None, hair_name=None, eyewear_name=None, headwear_name=None, mouth_name=None, facial_hair_name=None, accessory_name=None, bg_color='cream'):
    """Composite a punk from layers"""
    # Start with background
    bg = create_background(BACKGROUNDS.get(bg_color, bg_color))
    
    # Load and composite base
    base_path = os.path.join(ASSETS_DIR, 'base', base_name)
    if os.path.exists(base_path):
        base = Image.open(base_path)
        bg.paste(base, (0, 0), base)
    
    # Load and composite eyes
    if eyes_name:
        eyes_path = os.path.join(ASSETS_DIR, 'eyes', eyes_name)
        if os.path.exists(eyes_path):
            eyes = Image.open(eyes_path)
            bg.paste(eyes, (0, 0), eyes)
    
    # Load and composite mouth
    if mouth_name:
        mouth_path = os.path.join(ASSETS_DIR, 'mouth', mouth_name)
        if os.path.exists(mouth_path):
            mouth = Image.open(mouth_path)
            bg.paste(mouth, (0, 0), mouth)
    
    # Load and composite facial hair (male)
    if facial_hair_name:
        facial_path = os.path.join(ASSETS_DIR, 'facial_hair', facial_hair_name)
        if os.path.exists(facial_path):
            facial = Image.open(facial_path)
            bg.paste(facial, (0, 0), facial)
    
    # Load and composite accessories
    if accessory_name:
        accessory_path = os.path.join(ASSETS_DIR, 'accessories', accessory_name)
        if os.path.exists(accessory_path):
            accessory = Image.open(accessory_path)
            bg.paste(accessory, (0, 0), accessory)
    
    # Load and composite hair
    if hair_name:
        hair_path = os.path.join(ASSETS_DIR, 'hair', hair_name)
        if os.path.exists(hair_path):
            hair = Image.open(hair_path)
            bg.paste(hair, (0, 0), hair)
    
    # Load and composite eyewear (on top of eyes)
    if eyewear_name:
        eyewear_path = os.path.join(ASSETS_DIR, 'eyewear', eyewear_name)
        if os.path.exists(eyewear_path):
            eyewear = Image.open(eyewear_path)
            bg.paste(eyewear, (0, 0), eyewear)
    
    # Load and composite headwear (on top of hair)
    if headwear_name:
        headwear_path = os.path.join(ASSETS_DIR, 'headwear', headwear_name)
        if os.path.exists(headwear_path):
            headwear = Image.open(headwear_path)
            bg.paste(headwear, (0, 0), headwear)
    
    return bg

def main():
    print("Creating preview composites...")
    
    # Generate some sample combinations
    samples = [
        ('male_medium1.png', 'eyes_regular_common.png', 'cream', 'preview_male_regular'),
        ('male_dark2.png', 'eyes_angry_uncommon.png', 'dark', 'preview_male_angry'),
        ('female_light1.png', 'eyes_blue_uncommon.png', 'pink', 'preview_female_blue'),
        ('female_medium2.png', 'eyes_wide_common.png', 'purple', 'preview_female_wide'),
        ('zombie.png', 'eyes_narrow_common.png', 'green', 'preview_zombie'),
        ('ape.png', 'eyes_basic_common.png', 'orange', 'preview_ape'),
        ('alien.png', 'eyes_wide_common.png', 'dark', 'preview_alien'),
        ('male_light2.png', 'eyes_laser_rare.png', 'dark', 'preview_laser'),
        ('female_dark1.png', 'eyes_heart_rare.png', 'pink', 'preview_heart'),
        ('male_medium3.png', 'eyes_robot_rare.png', 'gray', 'preview_robot'),
    ]
    
    for base, eyes, bg, name in samples:
        img = composite_punk(base, eyes, bg)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
        img.save(output_path)
        print(f"  ✓ {name}.png")
    
    print(f"\nDone! Previews saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
