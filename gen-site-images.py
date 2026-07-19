#!/usr/bin/env python3
"""
Generate site images using GPT Image 2 API via AIHUBMIX.

Text-to-image:  python gen-site-images.py --prompt "..." --out generated/ --id my-image
Image-to-image: python gen-site-images.py --prompt "enhance..." --source-image photo.jpg --out generated/ --id enhanced
Batch mode:     python gen-site-images.py --prompts image-strategy.json --out generated/

GPT Image 2 params:
  quality: low | medium | high (default: high)
  size: WxH, max edge 3840px, multiple of 16, up to 8.3M pixels
  output_format: png | webp | jpeg
"""
import requests, base64, json, os, sys, time, argparse
from pathlib import Path

# Proxy configuration — required for API access from China
PROXY_URL = os.environ.get('HTTPS_PROXY', os.environ.get('HTTP_PROXY', 'http://localhost:10808'))
PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None

def load_env():
    env_path = Path.home() / '.hermes' / '.env'
    if env_path.exists():
        for line in env_path.read_text(encoding='utf-8').splitlines():
            if line.startswith('AIHUBMIX_API_KEY='):
                os.environ['AIHUBMIX_API_KEY'] = line.split('=', 1)[1].strip()
                break
            if line.startswith('IMAGE_PROXY='):
                global PROXY_URL, PROXIES
                PROXY_URL = line.split('=', 1)[1].strip()
                PROXIES = {"http": PROXY_URL, "https": PROXY_URL}
                break
    return os.environ.get('AIHUBMIX_API_KEY')

def generate_image(prompt, api_key, quality='high', size='1024x1024',
                   output_format='webp', source_image=None):
    """
    Call GPT Image 2 API.
    - Text-to-image: POST /v1/images/generations
    - Image-to-image: POST /v1/images/edits (multipart with image + prompt)
    """
    if source_image:
        return _generate_edit(prompt, api_key, source_image, quality, size, output_format)
    return _generate_text(prompt, api_key, quality, size, output_format)

def _generate_text(prompt, api_key, quality, size, output_format):
    """Text-to-image via /v1/images/generations"""
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {
        'model': 'gpt-image-2',
        'prompt': prompt,
        'size': size,
        'quality': quality,
        'n': 1,
        'output_format': output_format,
    }

    endpoints = [
        ('https://aihubmix.com/v1/images/generations', 'AIHUBMIX'),
        ('https://api.inferera.com/v1/images/generations', 'INFERERA'),
    ]

    last_error = None
    for url, name in endpoints:
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120, proxies=PROXIES)
            if resp.status_code != 200:
                last_error = f"{name} {resp.status_code}: {resp.text[:300]}"
                continue
            data = resp.json()
            img_data = data['data'][0]
            if 'url' in img_data:
                r = requests.get(img_data['url'], timeout=30, proxies=PROXIES)
                r.raise_for_status()
                return r.content
            elif 'b64_json' in img_data:
                return base64.b64decode(img_data['b64_json'])
            else:
                last_error = f"No image data. Keys: {list(img_data.keys())}"
                continue
        except Exception as e:
            last_error = str(e)
            continue

    raise RuntimeError(f'All endpoints failed. Last: {last_error}')

def _generate_edit(prompt, api_key, source_image, quality, size, output_format):
    """Image-to-image via /v1/images/edits (multipart form data)"""
    img_bytes = Path(source_image).read_bytes()
    ext = Path(source_image).suffix.lower()
    mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                '.png': 'image/png', '.webp': 'image/webp', '.bmp': 'image/bmp'}
    mime = mime_map.get(ext, 'image/jpeg')

    # Try multipart form data (OpenAI edits endpoint format)
    files = {'image': (os.path.basename(source_image), img_bytes, mime)}
    data = {
        'model': 'gpt-image-2',
        'prompt': prompt,
        'size': size,
        'quality': quality,
        'n': '1',
        'output_format': output_format,
    }

    endpoints = [
        ('https://aihubmix.com/v1/images/edits', 'AIHUBMIX-EDIT'),
        ('https://api.inferera.com/v1/images/edits', 'INFERERA-EDIT'),
    ]

    last_error = None
    for url, name in endpoints:
        try:
            resp = requests.post(url, headers={'Authorization': f'Bearer {api_key}'},
                                files=files, data=data, timeout=120, proxies=PROXIES)
            if resp.status_code != 200:
                last_error = f"{name} {resp.status_code}: {resp.text[:300]}"
                continue
            data = resp.json()
            img_data = data['data'][0]
            if 'url' in img_data:
                r = requests.get(img_data['url'], timeout=30, proxies=PROXIES)
                r.raise_for_status()
                return r.content
            elif 'b64_json' in img_data:
                return base64.b64decode(img_data['b64_json'])
            else:
                last_error = f"No image data. Keys: {list(img_data.keys())}"
                continue
        except Exception as e:
            last_error = str(e)
            continue

    raise RuntimeError(f'All edit endpoints failed. Last: {last_error}')

def compress_image(filepath):
    import subprocess, shutil
    cwebp = shutil.which('cwebp')
    if not cwebp:
        return
    try:
        tmp = str(filepath) + '.tmp'
        subprocess.run([cwebp, '-q', '82', '-m', '6', str(filepath), '-o', tmp],
                      capture_output=True, timeout=30, check=True)
        Path(tmp).replace(filepath)
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description='GPT Image 2 generator for huaxingpcba.com')
    parser.add_argument('--prompts', help='Path to image-strategy.json (batch mode)')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument('--manifest', default=None, help='Existing manifest path')
    parser.add_argument('--quality', default='high', choices=['low', 'medium', 'high'],
                       help='Image quality (default: high)')
    parser.add_argument('--size', default='1024x1024',
                       help='Output size WxH, e.g. 1536x1024 for landscape hero')
    parser.add_argument('--delay', type=float, default=0.5)
    parser.add_argument('--source-image', help='Source image for img2img editing')
    parser.add_argument('--prompt', help='Prompt (single image mode)')
    parser.add_argument('--id', help='Output filename ID (without extension)')

    args = parser.parse_args()

    api_key = load_env()
    if not api_key:
        print("ERROR: AIHUBMIX_API_KEY not found in ~/.hermes/.env or environment")
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Single image mode ──
    if args.prompt and not args.prompts:
        img_id = args.id or 'single-gen'
        out_file = out_dir / f"{img_id}.webp"

        if out_file.exists():
            print(f"{img_id} — already exists, skipping")
            return

        mode = "img2img" if args.source_image else "t2i"
        print(f"[{mode}] {img_id} ({args.size}, quality={args.quality})...",
              end=' ', flush=True)
        try:
            image_bytes = generate_image(
                args.prompt, api_key,
                quality=args.quality,
                size=args.size,
                output_format='webp',
                source_image=args.source_image,
            )
            out_file.write_bytes(image_bytes)
            compress_image(out_file)
            print(f"OK ({len(out_file.read_bytes()):,} bytes)")
        except Exception as e:
            print(f"FAILED: {e}")
            sys.exit(1)
        return

    # ── Batch mode ──
    if not args.prompts:
        print("ERROR: --prompts or --prompt required")
        sys.exit(1)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"ERROR: {args.prompts} not found")
        sys.exit(1)

    data = json.loads(prompts_path.read_text(encoding='utf-8'))
    images = data.get('images', [])

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
    print("-" * 60)

    for i, img in enumerate(images):
        img_id = img['id']
        out_file = out_dir / f"{img_id}.webp"

        if out_file.exists():
            print(f"[{i+1}/{total}] {img_id} — exists, skip")
            manifest[img_id] = {'file': f"{img_id}.webp", 'role': img['role'],
                               'page': img['page'], 'display': img['display']}
            success += 1
            continue

        img_size = img.get('size', args.size)
        img_quality = img.get('quality', args.quality)
        print(f"[{i+1}/{total}] {img_id} ({img['role']}, {img_size}, q={img_quality})...",
              end=' ', flush=True)

        try:
            source_img = img.get('source_image')
            image_bytes = generate_image(
                img['prompt'], api_key,
                quality=img_quality,
                size=img_size,
                output_format='webp',
                source_image=source_img,
            )
            out_file.write_bytes(image_bytes)
            compress_image(out_file)
            print(f"OK ({len(out_file.read_bytes()):,} bytes)")

            manifest[img_id] = {'file': f"{img_id}.webp", 'role': img['role'],
                               'page': img['page'], 'display': img['display']}
            success += 1

            if i < total - 1:
                time.sleep(args.delay)

        except Exception as e:
            print(f"FAILED: {e}")
            failed.append({'id': img_id, 'error': str(e)})
            time.sleep(2)

    manifest_path = out_dir / 'image-manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

    print("-" * 60)
    print(f"Done: {success}/{total}, {len(failed)} failed")
    if failed:
        for f in failed:
            print(f"  - {f['id']}: {f['error']}")
        (out_dir / 'failed-images.json').write_text(
            json.dumps(failed, indent=2, ensure_ascii=False), encoding='utf-8')

if __name__ == '__main__':
    main()
