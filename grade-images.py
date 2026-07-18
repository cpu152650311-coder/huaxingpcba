#!/usr/bin/env python3
"""
Apply dark-gold color grading to real factory photos to match huaxingpcba.com's
"暗金精工" theme: bg #08080b, gold-copper accent #c8963e/#d4a843/#e8c56d.

Usage:
  python grade-images.py --input <file_or_dir> --output <dir> [--preview]
  python grade-images.py --input photo.jpg --output generated/ --size 800
"""
import argparse, os, sys, io
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

# ── Theme palette ──
BG_DARK   = (8, 8, 11)       # #08080b
GOLD_HI   = (232, 197, 109)  # #e8c56d  (bright gold)
GOLD_MID  = (212, 168, 67)   # #d4a843  (mid gold)
GOLD_LO   = (200, 150, 62)   # #c8963e  (deep gold)

def apply_dark_gold_theme(img: Image.Image, strength: float = 1.0) -> Image.Image:
    """
    Transform a photo to match the dark-gold theme.
    strength: 0.0 (no change) to 1.0 (full theme). Default 1.0.
    """
    w, h = img.size
    img = img.convert('RGB')

    # 1. Darken overall brightness (reduce exposure)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.45 + 0.15 * strength)  # 0.45 to 0.60

    # 2. Boost contrast for dramatic look
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3 + 0.2 * strength)

    # 3. Reduce saturation for moody feel (keep warmth)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.5 + 0.2 * strength)

    # 4. Apply warm gold color overlay via pixel-level blending
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            # Darken shadows toward #08080b
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if luminance < 40:
                # Deep shadows → near black with subtle warmth
                blend = min(1.0, (40 - luminance) / 40) * strength
                r = int(r * (1 - blend * 0.85) + BG_DARK[0] * blend * 0.85)
                g = int(g * (1 - blend * 0.85) + BG_DARK[1] * blend * 0.85)
                b = int(b * (1 - blend * 0.85) + BG_DARK[2] * blend * 0.85)
            elif luminance > 100:
                # Highlights → subtle gold tint
                blend = min(1.0, (luminance - 100) / 155) * strength * 0.25
                r = int(r * (1 - blend) + GOLD_MID[0] * blend)
                g = int(g * (1 - blend) + GOLD_MID[1] * blend)
                b = int(b * (1 - blend) + GOLD_MID[2] * blend)
            pixels[x, y] = (min(255, r), min(255, g), min(255, b))

    # 5. Vignette: darken edges
    vignette = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(vignette)
    # Radial gradient: center bright, edges dark
    cx, cy = w / 2, h / 2
    max_dist = (cx ** 2 + cy ** 2) ** 0.5
    for y in range(h):
        for x in range(w):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / max_dist
            # Sigmoid falloff starting at 50% radius
            v = 255 * (1 - max(0, min(1, (dist - 0.4) / 0.6)) ** 1.8 * strength * 0.5)
            draw.point((x, y), fill=int(v))

    img.putalpha(vignette)
    # Composite onto dark background
    bg = Image.new('RGBA', (w, h), (*BG_DARK, 255))
    img = Image.alpha_composite(bg.convert('RGBA'), img.convert('RGBA')).convert('RGB')

    # 6. Subtle sharpening
    img = img.filter(ImageFilter.UnsharpMask(radius=0.5, percent=30, threshold=3))

    return img


def process_single(input_path: str, output_dir: str, size: int = None,
                   quality: int = 82, strength: float = 1.0):
    """Process a single image file."""
    img = Image.open(input_path)

    # Convert RGBA/CMYK to RGB
    if img.mode in ('RGBA', 'P', 'CMYK', 'L'):
        img = img.convert('RGB')

    # Resize if requested (maintains aspect ratio, crops to square if needed)
    if size:
        img.thumbnail((size, size), Image.LANCZOS)

    # Apply dark gold theme
    img = apply_dark_gold_theme(img, strength)

    # Save as optimized webp
    out_name = Path(input_path).stem
    # Clean up filename
    out_name = out_name.replace(' ', '-').lower()
    out_path = Path(output_dir) / f"{out_name}.webp"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, 'WEBP', quality=quality, method=6)
    file_size = os.path.getsize(out_path)
    print(f"  {Path(input_path).name} → {out_path.name} ({file_size:,} bytes)")
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description='Apply dark-gold theme color grading to photos')
    parser.add_argument('--input', required=True, help='Input file or directory')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--size', type=int, default=1024,
                       help='Max dimension (default: 1024)')
    parser.add_argument('--quality', type=int, default=82,
                       help='WebP quality 0-100 (default: 82)')
    parser.add_argument('--strength', type=float, default=1.0,
                       help='Theme strength 0.0-1.0 (default: 1.0)')
    parser.add_argument('--preview', action='store_true',
                       help='Show before/after preview (requires GUI)')
    parser.add_argument('--ext', default='.jpg,.jpeg,.png,.bmp,.webp',
                       help='File extensions to process (comma-separated)')

    args = parser.parse_args()
    input_path = Path(args.input)
    extensions = [e.strip().lower() for e in args.ext.split(',')]

    files = []
    if input_path.is_file():
        files = [input_path]
    elif input_path.is_dir():
        for ext in extensions:
            files.extend(input_path.glob(f'*{ext}'))
            files.extend(input_path.glob(f'*{ext.upper()}'))
        files = sorted(set(files))
    else:
        print(f"ERROR: {args.input} not found")
        sys.exit(1)

    print(f"Processing {len(files)} image(s) with dark-gold theme...")
    print(f"Output: {Path(args.output).absolute()}")
    print(f"Strength: {args.strength}, Size: {args.size}px, Quality: {args.quality}")
    print("-" * 60)

    for i, f in enumerate(files):
        print(f"[{i+1}/{len(files)}]", end=' ')
        try:
            process_single(str(f), args.output, size=args.size,
                          quality=args.quality, strength=args.strength)
        except Exception as e:
            print(f"  FAILED: {e}")

    print("Done!")


if __name__ == '__main__':
    main()
