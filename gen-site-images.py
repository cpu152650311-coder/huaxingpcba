#!/usr/bin/env python3
"""Generate site images from image-strategy.json using GPT Image 2 API.
Supports text-to-image (default) and image-to-image (--source-image)."""
import requests, base64, json, os, sys, time, argparse
from pathlib import Path

def load_env():
    """Load AIHUBMIX_API_KEY from ~/.hermes/.env or environment."""
    env_path = Path.home() / '.hermes' / '.env'
    if env_path.exists():
        for line in env_path.read_text(encoding='utf-8').splitlines():
            if line.startswith('AIHUBMIX_API_KEY='):
                os.environ['AIHUBMIX_API_KEY'] = line.split('=', 1)[1].strip()
                break
    return os.environ.get('AIHUBMIX_API_KEY')

def generate_image(prompt, api_key, quality='low', source_image=None):
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'model': 'gpt-image-2', 'prompt': prompt, 'size': '1024x1024'}

    if source_image:
        # Image-to-image mode: base64-encode the source image
        img_bytes = Path(source_image).read_bytes()
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        # Detect mime type from extension
        ext = Path(source_image).suffix.lower()
        mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                    '.png': 'image/png', '.webp': 'image/webp', '.bmp': 'image/bmp'}
        mime = mime_map.get(ext, 'image/jpeg')
        payload['image'] = f'data:{mime};base64,{b64}'
        print(f"  [img2img] Source: {source_image} ({len(img_bytes):,} bytes)")

    endpoints = [
        ('https://aihubmix.com/v1/images/generations', 'AIHUBMIX'),
        ('https://api.inferera.com/v1/images/generations', 'INFERERA'),
    ]

    last_error = None
    for url, name in endpoints:
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            if resp.status_code != 200:
                last_error = f"{name} returned {resp.status_code}: {resp.text[:200]}"
                continue
            data = resp.json()
            image_data = data['data'][0]
            if 'url' in image_data:
                img_resp = requests.get(image_data['url'], timeout=30)
                img_resp.raise_for_status()
                return img_resp.content
            elif 'b64_json' in image_data:
                return base64.b64decode(image_data['b64_json'])
            else:
                last_error = f'No image data in response. Keys: {list(image_data.keys())}'
                continue
        except Exception as e:
            last_error = str(e)
            continue

    raise RuntimeError(f'All endpoints failed. Last error: {last_error}')

def compress_image(filepath):
    """Try cwebp compression, keep original on failure."""
    import subprocess, shutil
    cwebp = shutil.which('cwebp')
    if not cwebp:
        return
    try:
        tmp = str(filepath) + '.tmp'
        subprocess.run([cwebp, '-q', '75', '-m', '6', str(filepath), '-o', tmp],
                      capture_output=True, timeout=30, check=True)
        Path(tmp).replace(filepath)
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description='Generate images via GPT Image 2 API')
    parser.add_argument('--prompts', help='Path to image-strategy.json (batch mode)')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument('--manifest', default=None, help='Existing manifest to append to')
    parser.add_argument('--quality', default='low', choices=['low', 'medium', 'high'])
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between images (seconds)')

    # Image-to-image (single image mode)
    parser.add_argument('--source-image', help='Source image to enhance/beautify (img2img)')
    parser.add_argument('--prompt', help='Prompt for single image generation (with --source-image or standalone)')
    parser.add_argument('--id', help='Output filename ID (without extension)')

    args = parser.parse_args()

    api_key = load_env()
    if not api_key:
        print("ERROR: AIHUBMIX_API_KEY not found in ~/.hermes/.env or environment")
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Single-image mode (text-to-image or img2img) ──
    if args.prompt and not args.prompts:
        img_id = args.id or 'single-gen'
        out_file = out_dir / f"{img_id}.webp"

        if out_file.exists():
            print(f"{img_id} — already exists, skipping")
            return

        mode = "img2img" if args.source_image else "text-to-image"
        print(f"[{mode}] {img_id} — generating...", end=' ', flush=True)
        try:
            image_bytes = generate_image(args.prompt, api_key, args.quality,
                                         source_image=args.source_image)
            out_file.write_bytes(image_bytes)
            compress_image(out_file)
            file_size = len(out_file.read_bytes())
            print(f"OK ({file_size:,} bytes)")
        except Exception as e:
            print(f"FAILED: {e}")
            sys.exit(1)
        return

    # ── Batch mode (image-strategy.json) ──
    if not args.prompts:
        print("ERROR: --prompts (image-strategy.json path) or --prompt required")
        sys.exit(1)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"ERROR: {args.prompts} not found")
        sys.exit(1)

    data = json.loads(prompts_path.read_text(encoding='utf-8'))
    images = data.get('images', [])

    # Load existing manifest
    manifest = {}
    manifest_path = out_dir / 'image-manifest.json'
    if args.manifest:
        manifest_path = Path(args.manifest)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    total = len(images)
    success = 0
    failed = []

    print(f"Generating {total} images (quality={args.quality})...")
    print(f"Output: {out_dir.absolute()}")
    print(f"API Key: {api_key[:8]}...{api_key[-4:]}")
    print("-" * 60)

    for i, img in enumerate(images):
        img_id = img['id']
        out_file = out_dir / f"{img_id}.webp"

        if out_file.exists():
            print(f"[{i+1}/{total}] {img_id} — already exists, skipping")
            manifest[img_id] = {
                'file': f"{img_id}.webp",
                'role': img['role'],
                'page': img['page'],
                'display': img['display']
            }
            success += 1
            continue

        print(f"[{i+1}/{total}] {img_id} ({img['role']})...", end=' ', flush=True)

        try:
            source_img = img.get('source_image')
            image_bytes = generate_image(img['prompt'], api_key, args.quality,
                                         source_image=source_img)
            out_file.write_bytes(image_bytes)
            compress_image(out_file)
            file_size = len(out_file.read_bytes())
            print(f"OK ({file_size:,} bytes)")

            manifest[img_id] = {
                'file': f"{img_id}.webp",
                'role': img['role'],
                'page': img['page'],
                'display': img['display']
            }
            success += 1

            if i < total - 1:
                time.sleep(args.delay)

        except Exception as e:
            print(f"FAILED: {e}")
            failed.append({'id': img_id, 'error': str(e)})
            time.sleep(2)

    # Write manifest
    manifest_path = out_dir / 'image-manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

    print("-" * 60)
    print(f"Done: {success}/{total} succeeded, {len(failed)} failed")
    if failed:
        print("Failed images:")
        for f in failed:
            print(f"  - {f['id']}: {f['error']}")
        fail_path = out_dir / 'failed-images.json'
        fail_path.write_text(json.dumps(failed, indent=2, ensure_ascii=False), encoding='utf-8')

if __name__ == '__main__':
    main()
