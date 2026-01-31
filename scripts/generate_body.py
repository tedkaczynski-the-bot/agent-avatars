#!/usr/bin/env python3
"""
Generate base body pixel art for Agent Avatars.
Simple programmatic pixel art generation.
"""

from PIL import Image, ImageDraw
import os

# Canvas size
WIDTH = 256
HEIGHT = 256

# Skin tone palette
SKIN_TONES = {
    "light1": "#FFDBAC",
    "light2": "#F5C9A6",
    "light3": "#E5B894",
    "medium1": "#D4A574",
    "medium2": "#C69C6D",
    "medium3": "#A67C52",
    "dark1": "#8D5524",
    "dark2": "#6B4423",
    "dark3": "#4A2E1C",
    "alien": "#7ED321",
}

# Body proportions (relative to 256px canvas)
BODY_SPECS = {
    "boy": {
        "head_y": 45,
        "head_size": 50,
        "body_y": 95,
        "body_width": 40,
        "body_height": 60,
        "leg_length": 70,
        "arm_length": 50,
    },
    "girl": {
        "head_y": 50,
        "head_size": 48,
        "body_y": 98,
        "body_width": 36,
        "body_height": 55,
        "leg_length": 65,
        "arm_length": 45,
    },
    "man": {
        "head_y": 30,
        "head_size": 55,
        "body_y": 85,
        "body_width": 50,
        "body_height": 75,
        "leg_length": 80,
        "arm_length": 60,
    },
    "woman": {
        "head_y": 35,
        "head_size": 52,
        "body_y": 87,
        "body_width": 42,
        "body_height": 68,
        "leg_length": 75,
        "arm_length": 55,
    },
    "alien": {
        "head_y": 35,
        "head_size": 60,  # Bigger head
        "body_y": 95,
        "body_width": 35,
        "body_height": 65,
        "leg_length": 70,
        "arm_length": 55,
    },
}


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_pixel_rect(draw, x, y, w, h, color, pixel_size=4):
    """Draw a pixelated rectangle."""
    for px in range(0, w, pixel_size):
        for py in range(0, h, pixel_size):
            draw.rectangle(
                [x + px, y + py, x + px + pixel_size - 1, y + py + pixel_size - 1],
                fill=color
            )


def draw_pixel_circle(draw, cx, cy, radius, color, pixel_size=4):
    """Draw a pixelated circle."""
    for x in range(-radius, radius + 1, pixel_size):
        for y in range(-radius, radius + 1, pixel_size):
            if x*x + y*y <= radius*radius:
                draw.rectangle(
                    [cx + x, cy + y, cx + x + pixel_size - 1, cy + y + pixel_size - 1],
                    fill=color
                )


def generate_body(body_type, skin_color_name, output_path):
    """Generate a base body sprite."""
    
    # Create transparent image
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Get specs and color
    specs = BODY_SPECS[body_type]
    skin_hex = SKIN_TONES.get(skin_color_name, SKIN_TONES["medium1"])
    skin_color = hex_to_rgb(skin_hex)
    
    # Darker shade for outline/details
    outline_color = tuple(max(0, c - 40) for c in skin_color)
    
    center_x = WIDTH // 2
    pixel = 4  # Pixel size for chunky look
    
    # Draw head (circle-ish)
    head_y = specs["head_y"]
    head_size = specs["head_size"]
    draw_pixel_circle(draw, center_x, head_y + head_size//2, head_size//2, skin_color, pixel)
    
    # Draw body (rectangle)
    body_y = specs["body_y"]
    body_w = specs["body_width"]
    body_h = specs["body_height"]
    draw_pixel_rect(draw, center_x - body_w//2, body_y, body_w, body_h, skin_color, pixel)
    
    # Draw legs (two rectangles)
    leg_y = body_y + body_h
    leg_w = body_w // 3
    leg_h = specs["leg_length"]
    leg_gap = 4
    
    # Left leg
    draw_pixel_rect(draw, center_x - leg_w - leg_gap//2, leg_y, leg_w, leg_h, skin_color, pixel)
    # Right leg
    draw_pixel_rect(draw, center_x + leg_gap//2, leg_y, leg_w, leg_h, skin_color, pixel)
    
    # Draw arms (rectangles at sides)
    arm_y = body_y + 5
    arm_w = 12
    arm_h = specs["arm_length"]
    
    # Left arm
    draw_pixel_rect(draw, center_x - body_w//2 - arm_w, arm_y, arm_w, arm_h, skin_color, pixel)
    # Right arm
    draw_pixel_rect(draw, center_x + body_w//2, arm_y, arm_w, arm_h, skin_color, pixel)
    
    # Add simple eyes for alien or all types
    if body_type == "alien":
        eye_color = (0, 0, 0)
        eye_y = head_y + head_size//2 - 5
        draw_pixel_rect(draw, center_x - 15, eye_y, 10, 10, eye_color, pixel)
        draw_pixel_rect(draw, center_x + 5, eye_y, 10, 10, eye_color, pixel)
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Generated: {output_path}")
    return output_path


def generate_all_bodies(output_dir):
    """Generate all body types with all skin tones."""
    
    generated = []
    
    for body_type in BODY_SPECS.keys():
        # For alien, only use alien skin
        if body_type == "alien":
            skin_tones = ["alien"]
        else:
            skin_tones = [k for k in SKIN_TONES.keys() if k != "alien"]
        
        for skin in skin_tones:
            filename = f"body_{body_type}_{skin}.png"
            output_path = os.path.join(output_dir, filename)
            generate_body(body_type, skin, output_path)
            generated.append(output_path)
    
    return generated


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = "./assets/bodies"
    
    print(f"Generating bodies to: {output_dir}")
    files = generate_all_bodies(output_dir)
    print(f"\nGenerated {len(files)} body sprites!")
