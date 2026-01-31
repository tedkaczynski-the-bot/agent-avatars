#!/usr/bin/env python3
"""
Generate patterned backgrounds for agent avatars
"""

from PIL import Image, ImageDraw
import os
import random
import math

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'faces', 'backgrounds')
os.makedirs(ASSETS_DIR, exist_ok=True)

SIZE = 256

# Base colors
COLORS = {
    'cream': '#FEF3C7',
    'blue': '#DBEAFE',
    'pink': '#FCE7F3',
    'green': '#D1FAE5',
    'gray': '#E5E7EB',
    'dark': '#1F2937',
    'purple': '#7C3AED',
    'orange': '#F97316',
    'cyan': '#06B6D4',
    'black': '#0A0A0A',
    'navy': '#1E3A5F',
}

def hex_to_rgb(hex_color):
    """Convert hex to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def darken(color, factor=0.8):
    """Darken a color"""
    r, g, b = hex_to_rgb(color) if isinstance(color, str) else color
    return (int(r * factor), int(g * factor), int(b * factor))

def lighten(color, factor=1.2):
    """Lighten a color"""
    r, g, b = hex_to_rgb(color) if isinstance(color, str) else color
    return (min(255, int(r * factor)), min(255, int(g * factor)), min(255, int(b * factor)))

def create_solid(color, name):
    """Create a solid color background"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(color))
    img.save(os.path.join(ASSETS_DIR, f'solid_{name}_common.png'))
    print(f"  ✓ solid_{name}_common.png")

def create_gradient_vertical(color1, color2, name):
    """Create a vertical gradient"""
    img = Image.new('RGB', (SIZE, SIZE))
    draw = ImageDraw.Draw(img)
    
    r1, g1, b1 = hex_to_rgb(color1) if isinstance(color1, str) else color1
    r2, g2, b2 = hex_to_rgb(color2) if isinstance(color2, str) else color2
    
    for y in range(SIZE):
        ratio = y / SIZE
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b))
    
    img.save(os.path.join(ASSETS_DIR, f'gradient_{name}_uncommon.png'))
    print(f"  ✓ gradient_{name}_uncommon.png")

def create_scanlines(base_color, name):
    """Create horizontal scanlines pattern"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    line_color = darken(base_color, 0.85)
    
    for y in range(0, SIZE, 4):
        draw.line([(0, y), (SIZE, y)], fill=line_color, width=1)
    
    img.save(os.path.join(ASSETS_DIR, f'scanlines_{name}_uncommon.png'))
    print(f"  ✓ scanlines_{name}_uncommon.png")

def create_grid(base_color, name, spacing=16):
    """Create a grid pattern"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    line_color = darken(base_color, 0.85)
    
    for x in range(0, SIZE, spacing):
        draw.line([(x, 0), (x, SIZE)], fill=line_color, width=1)
    for y in range(0, SIZE, spacing):
        draw.line([(0, y), (SIZE, y)], fill=line_color, width=1)
    
    img.save(os.path.join(ASSETS_DIR, f'grid_{name}_uncommon.png'))
    print(f"  ✓ grid_{name}_uncommon.png")

def create_hex_grid(base_color, name):
    """Create a hexagonal grid pattern"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    line_color = darken(base_color, 0.8)
    hex_size = 20
    
    def draw_hexagon(cx, cy, size):
        points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, outline=line_color)
    
    h = hex_size * math.sqrt(3)
    for row in range(-1, int(SIZE / h) + 2):
        for col in range(-1, int(SIZE / (hex_size * 1.5)) + 2):
            cx = col * hex_size * 1.5
            cy = row * h + (col % 2) * h / 2
            draw_hexagon(cx, cy, hex_size)
    
    img.save(os.path.join(ASSETS_DIR, f'hexgrid_{name}_rare.png'))
    print(f"  ✓ hexgrid_{name}_rare.png")

def create_circuit(base_color, name):
    """Create a circuit board pattern"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    line_color = darken(base_color, 0.7)
    node_color = lighten(base_color, 1.3)
    
    random.seed(42 + hash(name))  # Deterministic but unique per color
    
    # Draw circuit traces
    grid_size = 16
    for _ in range(30):
        x = random.randint(0, SIZE // grid_size) * grid_size
        y = random.randint(0, SIZE // grid_size) * grid_size
        
        # Random path
        for _ in range(random.randint(2, 6)):
            direction = random.choice(['h', 'v'])
            length = random.randint(1, 4) * grid_size
            
            if direction == 'h':
                new_x = max(0, min(SIZE, x + random.choice([-1, 1]) * length))
                draw.line([(x, y), (new_x, y)], fill=line_color, width=2)
                x = new_x
            else:
                new_y = max(0, min(SIZE, y + random.choice([-1, 1]) * length))
                draw.line([(x, y), (x, new_y)], fill=line_color, width=2)
                y = new_y
        
        # Node at end
        draw.ellipse([x-3, y-3, x+3, y+3], fill=node_color)
    
    img.save(os.path.join(ASSETS_DIR, f'circuit_{name}_rare.png'))
    print(f"  ✓ circuit_{name}_rare.png")

def create_constellation(base_color, name):
    """Create a constellation/network pattern"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    line_color = darken(base_color, 0.75)
    star_color = lighten(base_color, 1.4)
    
    random.seed(123 + hash(name))
    
    # Generate star positions
    stars = [(random.randint(10, SIZE-10), random.randint(10, SIZE-10)) for _ in range(25)]
    
    # Connect nearby stars
    for i, (x1, y1) in enumerate(stars):
        for j, (x2, y2) in enumerate(stars):
            if i < j:
                dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                if dist < 80:
                    # Fade line based on distance
                    alpha = 1 - (dist / 80)
                    draw.line([(x1, y1), (x2, y2)], fill=line_color, width=1)
    
    # Draw stars
    for x, y in stars:
        size = random.choice([2, 3, 4])
        draw.ellipse([x-size, y-size, x+size, y+size], fill=star_color)
    
    img.save(os.path.join(ASSETS_DIR, f'constellation_{name}_rare.png'))
    print(f"  ✓ constellation_{name}_rare.png")

def create_topographic(base_color, name):
    """Create topographic contour lines"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    line_color = darken(base_color, 0.8)
    
    random.seed(456 + hash(name))
    
    # Generate contour centers
    centers = [(random.randint(0, SIZE), random.randint(0, SIZE)) for _ in range(3)]
    
    for cx, cy in centers:
        for radius in range(20, 200, 15):
            # Draw wavy circles
            points = []
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                # Add some noise to radius
                noise = math.sin(angle * 0.1) * 10 + math.cos(angle * 0.15) * 8
                r = radius + noise
                x = cx + r * math.cos(rad)
                y = cy + r * math.sin(rad)
                points.append((x, y))
            
            if len(points) > 2:
                draw.line(points + [points[0]], fill=line_color, width=1)
    
    img.save(os.path.join(ASSETS_DIR, f'topographic_{name}_rare.png'))
    print(f"  ✓ topographic_{name}_rare.png")

def create_geometric(base_color, name):
    """Create geometric triangle tessellation"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    base_rgb = hex_to_rgb(base_color)
    
    random.seed(789 + hash(name))
    
    tri_size = 40
    
    for row in range(-1, SIZE // tri_size + 2):
        for col in range(-1, SIZE // tri_size + 2):
            x = col * tri_size + (row % 2) * (tri_size // 2)
            y = row * tri_size * 0.866
            
            # Random shade variation
            shade = random.uniform(0.85, 1.15)
            color = (
                min(255, int(base_rgb[0] * shade)),
                min(255, int(base_rgb[1] * shade)),
                min(255, int(base_rgb[2] * shade))
            )
            
            # Draw triangle
            points = [
                (x, y),
                (x + tri_size, y),
                (x + tri_size // 2, y + tri_size * 0.866)
            ]
            draw.polygon(points, fill=color)
    
    img.save(os.path.join(ASSETS_DIR, f'geometric_{name}_uncommon.png'))
    print(f"  ✓ geometric_{name}_uncommon.png")

def create_dots(base_color, name):
    """Create polka dot pattern"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    dot_color = darken(base_color, 0.85)
    
    spacing = 24
    radius = 4
    
    for y in range(0, SIZE + spacing, spacing):
        offset = (y // spacing % 2) * (spacing // 2)
        for x in range(0, SIZE + spacing, spacing):
            draw.ellipse([x + offset - radius, y - radius, x + offset + radius, y + radius], fill=dot_color)
    
    img.save(os.path.join(ASSETS_DIR, f'dots_{name}_common.png'))
    print(f"  ✓ dots_{name}_common.png")

def create_noise(base_color, name):
    """Create a subtle noise/grain texture"""
    base_rgb = hex_to_rgb(base_color)
    img = Image.new('RGB', (SIZE, SIZE))
    
    random.seed(111 + hash(name))
    
    for y in range(SIZE):
        for x in range(SIZE):
            noise = random.randint(-15, 15)
            color = (
                max(0, min(255, base_rgb[0] + noise)),
                max(0, min(255, base_rgb[1] + noise)),
                max(0, min(255, base_rgb[2] + noise))
            )
            img.putpixel((x, y), color)
    
    img.save(os.path.join(ASSETS_DIR, f'noise_{name}_common.png'))
    print(f"  ✓ noise_{name}_common.png")

def create_glitch(base_color, name):
    """Create a glitchy/distorted pattern"""
    img = Image.new('RGB', (SIZE, SIZE), hex_to_rgb(base_color))
    draw = ImageDraw.Draw(img)
    
    random.seed(222 + hash(name))
    
    glitch_colors = [
        (255, 0, 100),   # Magenta
        (0, 255, 200),   # Cyan
        (255, 255, 0),   # Yellow
    ]
    
    # Draw glitch bars
    for _ in range(15):
        y = random.randint(0, SIZE)
        height = random.randint(2, 8)
        offset = random.randint(-20, 20)
        color = random.choice(glitch_colors)
        
        draw.rectangle([offset, y, SIZE + offset, y + height], fill=color)
    
    img.save(os.path.join(ASSETS_DIR, f'glitch_{name}_legendary.png'))
    print(f"  ✓ glitch_{name}_legendary.png")

def create_matrix(name):
    """Create matrix rain effect"""
    img = Image.new('RGB', (SIZE, SIZE), (0, 10, 0))
    draw = ImageDraw.Draw(img)
    
    random.seed(333)
    
    for x in range(0, SIZE, 12):
        column_height = random.randint(50, SIZE)
        start_y = random.randint(0, SIZE - 50)
        
        for y in range(start_y, min(start_y + column_height, SIZE), 12):
            brightness = 255 - int((y - start_y) / column_height * 200)
            color = (0, brightness, 0)
            
            # Draw a simple block instead of text
            draw.rectangle([x, y, x+8, y+10], fill=color)
    
    img.save(os.path.join(ASSETS_DIR, f'matrix_{name}_legendary.png'))
    print(f"  ✓ matrix_{name}_legendary.png")

def main():
    print("Generating patterned backgrounds...")
    print()
    
    # Generate solid backgrounds
    print("Solid colors:")
    for name, color in COLORS.items():
        create_solid(color, name)
    print()
    
    # Generate gradients
    print("Gradients:")
    create_gradient_vertical(COLORS['purple'], COLORS['pink'], 'sunset')
    create_gradient_vertical(COLORS['dark'], COLORS['purple'], 'night')
    create_gradient_vertical(COLORS['cyan'], COLORS['blue'], 'ocean')
    create_gradient_vertical(COLORS['orange'], COLORS['pink'], 'peach')
    create_gradient_vertical(COLORS['black'], COLORS['navy'], 'abyss')
    print()
    
    # Generate patterns
    print("Patterns:")
    for name, color in [('dark', COLORS['dark']), ('navy', COLORS['navy']), ('purple', COLORS['purple'])]:
        create_scanlines(color, name)
    
    for name, color in [('gray', COLORS['gray']), ('dark', COLORS['dark']), ('cyan', COLORS['cyan'])]:
        create_grid(color, name)
    
    for name, color in [('dark', COLORS['dark']), ('navy', COLORS['navy']), ('purple', COLORS['purple'])]:
        create_hex_grid(color, name)
    
    for name, color in [('dark', COLORS['dark']), ('navy', COLORS['navy']), ('green', COLORS['green'])]:
        create_circuit(color, name)
    
    for name, color in [('dark', COLORS['dark']), ('navy', COLORS['navy']), ('purple', COLORS['purple'])]:
        create_constellation(color, name)
    
    for name, color in [('cream', COLORS['cream']), ('blue', COLORS['blue']), ('green', COLORS['green'])]:
        create_topographic(color, name)
    
    for name, color in [('purple', COLORS['purple']), ('blue', COLORS['blue']), ('pink', COLORS['pink'])]:
        create_geometric(color, name)
    
    for name, color in [('cream', COLORS['cream']), ('pink', COLORS['pink']), ('blue', COLORS['blue'])]:
        create_dots(color, name)
    
    for name, color in [('gray', COLORS['gray']), ('dark', COLORS['dark'])]:
        create_noise(color, name)
    
    print()
    print("Special effects:")
    create_glitch(COLORS['dark'], 'dark')
    create_glitch(COLORS['black'], 'black')
    create_matrix('green')
    
    print()
    print(f"Done! Backgrounds saved to {ASSETS_DIR}")
    print(f"Total files: {len(os.listdir(ASSETS_DIR))}")

if __name__ == "__main__":
    main()
