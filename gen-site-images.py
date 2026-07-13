#!/usr/bin/env python3
"""Generate all site images from image-strategy.json using GPT Image 2 API."""
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

def generate_image(prompt, api_key, quality='low'):
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    payload = {'model': 'gpt-image-2', 'prompt': prompt, 'size': '1024x1024'}

    try:
        resp = requests.post('https://aihubmix.com/v1/images/generations',
                            headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Primary endpoint failed ({e}), trying fallback...")
        try:
            resp = requests.post('https://api.inferera.com/v1/images/generations',
                                headers=headers, json=payload, timeout=90)
            resp.raise_for_status()
        except Exception as e2:
            print(f"  Fallback also failed: {e2}")
            raise

    data = resp.json()
    image_data = data['data'][0]

    if 'url' in image_data:
        img_resp = requests.get(image_data['url'], timeout=30)
        img_resp.raise_for_status()
        return img_resp.content
    elif 'b64_json' in image_data:
        return base64.b64decode(image_data['b64_json'])
    else:
        raise ValueError(f'No image data in response. Keys: {list(image_data.keys())}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompts', required=True, help='Path to image-strategy.json')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument('--manifest', default=None, help='Existing manifest to append to')
    parser.add_argument('--quality', default='low', choices=['low', 'medium', 'high'])
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between images (seconds)')
    args = parser.parse_args()

    api_key = load_env()
    if not api_key:
        print("ERROR: AIHUBMIX_API_KEY not found in ~/.hermes/.env or environment")
        sys.exit(1)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"ERROR: {args.prompts} not found")
        sys.exit(1)

    data = json.loads(prompts_path.read_text(encoding='utf-8'))
    images = data.get('images', [])

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load existing manifest if appending
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

        # Skip if already exists
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
            image_bytes = generate_image(img['prompt'], api_key, args.quality)
            out_file.write_bytes(image_bytes)
            file_size = len(image_bytes)
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
            # Continue with next image
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
        # Write failed list for retry
        fail_path = out_dir / 'failed-images.json'
        fail_path.write_text(json.dumps(failed, indent=2, ensure_ascii=False), encoding='utf-8')

if __name__ == '__main__':
    main()
