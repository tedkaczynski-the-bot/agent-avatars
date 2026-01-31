#!/usr/bin/env python3
"""
Generate CryptoPunks-style base faces at 256x256
Chunky pixel blocks (~10-12px per "pixel") for that iconic look
"""

from PIL import Image, ImageDraw
import os

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'base')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Canvas size
SIZE = 256

# Pixel block size (for chunky pixel art look)
BLOCK = 10  # Each "pixel" is 10x10 real pixels

# Skin tones (from ART_SPECS.md)
SKIN_TONES = {
    'light1': '#FFDBAC',
    'light2': '#F5C9A6', 
    'light3': '#E5B894',
    'medium1': '#D4A574',
    'medium2': '#C69C6D',
    'medium3': '#A67C52',
    'dark1': '#8D5524',
    'dark2': '#6B4423',
    'dark3': '#4A2E1C',
}

# Special skin tones for rare types
SPECIAL_SKINS = {
    'zombie': '#7DB87D',  # Green
    'ape': '#A0522D',     # Brown/sienna  
    'alien': '#7ED321',   # Bright green
}

def draw_block(draw, x, y, color, block_size=BLOCK):
    """Draw a single pixel block"""
    draw.rectangle([x * block_size, y * block_size, 
                   (x + 1) * block_size - 1, (y + 1) * block_size - 1], 
                  fill=color)

def draw_male_face(skin_color, variant='default'):
    """Draw a male punk face"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Darker shade for outline/shadow
    r, g, b = int(skin_color[1:3], 16), int(skin_color[3:5], 16), int(skin_color[5:7], 16)
    shadow = f'#{max(0,r-40):02x}{max(0,g-40):02x}{max(0,b-40):02x}'
    
    # Face shape - blocky rectangular male face
    # Face is roughly 14 blocks wide, 18 blocks tall, centered
    face_left = 6
    face_right = 20
    face_top = 5
    face_bottom = 23
    
    # Draw main face block
    for y in range(face_top + 2, face_bottom - 1):
        for x in range(face_left + 1, face_right - 1):
            draw_block(draw, x, y, skin_color)
    
    # Top of head (slightly narrower)
    for y in range(face_top, face_top + 2):
        for x in range(face_left + 2, face_right - 2):
            draw_block(draw, x, y, skin_color)
    
    # Forehead sides
    for x in [face_left + 1, face_right - 2]:
        for y in range(face_top + 1, face_top + 3):
            draw_block(draw, x, y, skin_color)
    
    # Jaw (slightly narrower at bottom)
    for y in range(face_bottom - 2, face_bottom):
        for x in range(face_left + 2, face_right - 2):
            draw_block(draw, x, y, skin_color)
    
    # Chin
    for x in range(face_left + 3, face_right - 3):
        draw_block(draw, x, face_bottom, skin_color)
    
    # Ears
    for y in range(10, 14):
        draw_block(draw, face_left, y, skin_color)
        draw_block(draw, face_right - 1, y, skin_color)
    
    # Ear inner shadow
    draw_block(draw, face_left, 11, shadow)
    draw_block(draw, face_right - 1, 11, shadow)
    
    # Neck
    for y in range(face_bottom + 1, 25):
        for x in range(10, 16):
            draw_block(draw, x, y, skin_color)
    
    return img

def draw_female_face(skin_color, variant='default'):
    """Draw a female punk face - slightly softer/rounder shape"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Darker shade for outline/shadow
    r, g, b = int(skin_color[1:3], 16), int(skin_color[3:5], 16), int(skin_color[5:7], 16)
    shadow = f'#{max(0,r-40):02x}{max(0,g-40):02x}{max(0,b-40):02x}'
    
    # Face shape - slightly narrower, more oval for female
    face_left = 7
    face_right = 19
    face_top = 5
    face_bottom = 22
    
    # Draw main face block
    for y in range(face_top + 2, face_bottom - 1):
        for x in range(face_left + 1, face_right - 1):
            draw_block(draw, x, y, skin_color)
    
    # Top of head (rounder)
    for y in range(face_top, face_top + 2):
        for x in range(face_left + 2, face_right - 2):
            draw_block(draw, x, y, skin_color)
    
    # Sides near top
    for x in [face_left + 1, face_right - 2]:
        draw_block(draw, x, face_top + 1, skin_color)
    
    # Jaw (more tapered for female)
    for x in range(face_left + 2, face_right - 2):
        draw_block(draw, x, face_bottom - 1, skin_color)
    
    # Chin (smaller/pointer)
    for x in range(face_left + 4, face_right - 4):
        draw_block(draw, x, face_bottom, skin_color)
    
    # Ears (smaller)
    for y in range(10, 13):
        draw_block(draw, face_left, y, skin_color)
        draw_block(draw, face_right - 1, y, skin_color)
    
    # Ear inner shadow
    draw_block(draw, face_left, 11, shadow)
    draw_block(draw, face_right - 1, 11, shadow)
    
    # Neck (thinner)
    for y in range(face_bottom + 1, 24):
        for x in range(11, 15):
            draw_block(draw, x, y, skin_color)
    
    return img

def draw_zombie_face(variant='default'):
    """Draw a zombie punk face - green, decayed look"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    skin = SPECIAL_SKINS['zombie']
    shadow = '#5A8A5A'  # Darker green
    bone = '#E8E8E0'    # Exposed bone color
    
    # Similar to male but with decay details
    face_left = 6
    face_right = 20
    face_top = 5
    face_bottom = 23
    
    # Main face
    for y in range(face_top + 2, face_bottom - 1):
        for x in range(face_left + 1, face_right - 1):
            draw_block(draw, x, y, skin)
    
    # Top of head
    for y in range(face_top, face_top + 2):
        for x in range(face_left + 2, face_right - 2):
            draw_block(draw, x, y, skin)
    
    # Jaw
    for y in range(face_bottom - 2, face_bottom):
        for x in range(face_left + 2, face_right - 2):
            draw_block(draw, x, y, skin)
    
    # Chin
    for x in range(face_left + 3, face_right - 3):
        draw_block(draw, x, face_bottom, skin)
    
    # Ears
    for y in range(10, 14):
        draw_block(draw, face_left, y, skin)
        draw_block(draw, face_right - 1, y, skin)
    
    # Decay patches (darker areas)
    decay_spots = [(8, 8), (17, 12), (9, 18), (16, 7)]
    for dx, dy in decay_spots:
        draw_block(draw, dx, dy, shadow)
    
    # Exposed bone on cheek
    draw_block(draw, 15, 15, bone)
    
    # Neck
    for y in range(face_bottom + 1, 25):
        for x in range(10, 16):
            draw_block(draw, x, y, skin)
    
    return img

def draw_ape_face(variant='default'):
    """Draw an ape punk face - CryptoPunks style primate"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Brown fur tones
    fur_main = '#8B6914'      # Golden brown fur
    fur_dark = '#5D4A1C'      # Darker fur/shadow
    fur_light = '#B8860B'     # Lighter highlights
    face_skin = '#D2A679'     # Lighter face/muzzle area
    nose_color = '#4A3728'    # Dark nose
    
    # Face shape - wider, more primate
    face_left = 5
    face_right = 21
    face_top = 6
    face_bottom = 22
    
    # Main fur/head area
    for y in range(face_top, face_bottom):
        for x in range(face_left + 1, face_right - 1):
            draw_block(draw, x, y, fur_main)
    
    # Top of head - furry, slightly domed
    for x in range(face_left + 2, face_right - 2):
        draw_block(draw, x, face_top - 1, fur_main)
    for x in range(face_left + 3, face_right - 3):
        draw_block(draw, x, face_top - 2, fur_dark)
    
    # Heavy brow ridge (signature ape feature)
    for x in range(face_left + 2, face_right - 2):
        draw_block(draw, x, 9, fur_dark)
        draw_block(draw, x, 10, fur_dark)
    
    # Face/muzzle area (lighter, skin colored)
    for y in range(11, 19):
        for x in range(8, 18):
            draw_block(draw, x, y, face_skin)
    
    # Protruding muzzle (lower face sticks out more)
    for y in range(15, 19):
        for x in range(7, 19):
            draw_block(draw, x, y, face_skin)
    
    # Wide nostrils
    draw_block(draw, 11, 16, nose_color)
    draw_block(draw, 14, 16, nose_color)
    
    # Fur around face edges
    for y in range(11, 18):
        draw_block(draw, 7, y, fur_main)
        draw_block(draw, 18, y, fur_main)
    
    # Big round ears (ape style)
    for y in range(8, 14):
        draw_block(draw, face_left - 1, y, fur_main)
        draw_block(draw, face_left, y, fur_main)
        draw_block(draw, face_right - 1, y, fur_main)
        draw_block(draw, face_right, y, fur_main)
    # Ear centers
    draw_block(draw, face_left, 10, face_skin)
    draw_block(draw, face_left, 11, face_skin)
    draw_block(draw, face_right - 1, 10, face_skin)
    draw_block(draw, face_right - 1, 11, face_skin)
    
    # Jaw/chin
    for x in range(face_left + 3, face_right - 3):
        draw_block(draw, x, face_bottom, fur_main)
    
    # Neck (thick, furry)
    for y in range(face_bottom + 1, 25):
        for x in range(9, 17):
            draw_block(draw, x, y, fur_main)
    
    # Some fur texture highlights
    highlights = [(7, 7), (18, 8), (8, 20), (17, 19)]
    for hx, hy in highlights:
        draw_block(draw, hx, hy, fur_light)
    
    return img

def draw_alien_face(variant='default'):
    """Draw an alien punk face - CryptoPunks style (cyan/blue, big dome)"""
    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Alien colors - cyan/teal like CryptoPunks
    skin = '#61E786'          # Bright green-cyan
    skin_dark = '#4BB86A'     # Darker shade
    skin_light = '#8DFFA8'    # Highlight
    
    # Big domed head, smaller face
    head_center_x = 13
    
    # Large cranium (the iconic alien dome)
    # Top of dome
    for x in range(9, 18):
        draw_block(draw, x, 2, skin)
    for x in range(8, 19):
        draw_block(draw, x, 3, skin)
    for x in range(7, 20):
        draw_block(draw, x, 4, skin)
    for x in range(6, 21):
        for y in range(5, 10):
            draw_block(draw, x, y, skin)
    
    # Dome highlight (shiny head)
    draw_block(draw, 10, 3, skin_light)
    draw_block(draw, 11, 3, skin_light)
    draw_block(draw, 10, 4, skin_light)
    
    # Face narrows down from the dome
    for y in range(10, 13):
        for x in range(7, 20):
            draw_block(draw, x, y, skin)
    
    for y in range(13, 17):
        for x in range(8, 19):
            draw_block(draw, x, y, skin)
    
    for y in range(17, 20):
        for x in range(9, 18):
            draw_block(draw, x, y, skin)
    
    # Narrow jaw
    for x in range(10, 17):
        draw_block(draw, x, 20, skin)
    
    # Small pointed chin
    for x in range(11, 16):
        draw_block(draw, x, 21, skin)
    for x in range(12, 15):
        draw_block(draw, x, 22, skin)
    
    # Thin elegant neck
    for y in range(23, 25):
        for x in range(11, 16):
            draw_block(draw, x, y, skin)
    
    # Subtle shading on sides
    for y in range(6, 15):
        draw_block(draw, 6, y, skin_dark)
        draw_block(draw, 20, y, skin_dark)
    
    return img

def main():
    print("Generating CryptoPunks-style base faces (256x256)...")
    
    # Generate Male faces with all skin tones
    print("\nMale faces:")
    for tone_name, color in SKIN_TONES.items():
        img = draw_male_face(color)
        filename = f"male_{tone_name}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    # Generate Female faces with all skin tones
    print("\nFemale faces:")
    for tone_name, color in SKIN_TONES.items():
        img = draw_female_face(color)
        filename = f"female_{tone_name}.png"
        img.save(os.path.join(OUTPUT_DIR, filename))
        print(f"  ✓ {filename}")
    
    # Generate special types
    print("\nSpecial types:")
    
    img = draw_zombie_face()
    img.save(os.path.join(OUTPUT_DIR, "zombie.png"))
    print("  ✓ zombie.png")
    
    img = draw_ape_face()
    img.save(os.path.join(OUTPUT_DIR, "ape.png"))
    print("  ✓ ape.png")
    
    img = draw_alien_face()
    img.save(os.path.join(OUTPUT_DIR, "alien.png"))
    print("  ✓ alien.png")
    
    print(f"\nDone! Faces saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
