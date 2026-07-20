#!/usr/bin/env python3
"""Generate blog images for quick-turn-pcb-manufacturing article."""
import os, sys, subprocess, time, base64
from openai import OpenAI

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
if not API_KEY:
    print("ERROR: AIHUBMIX_API_KEY not set", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url="https://aihubmix.com/v1")
OUT = "/home/ubuntu/projects/huaxingpcba/generated"

IMAGES = [
    {
        "id": "cover-quick-turn-pcb",
        "prompt": "A high-speed SMT pick-and-place machine in a modern PCB factory, multiple placement heads operating simultaneously over a green circuit board panel, bright clean industrial lighting, shallow depth of field focusing on the placement nozzles, blue-and-white factory color scheme, professional electronics manufacturing environment, no people faces, no text, no logos"
    },
    {
        "id": "quick-turn-pcb-hero",
        "prompt": "Photorealistic macro shot of a freshly manufactured PCB panel emerging from a solder reflow oven on a conveyor belt, golden ENIG pads gleaming under warm industrial light, steam haze rising from the hot board surface, modern electronics factory background with blue machine status lights, shallow depth of field, cinematic factory atmosphere, no people faces, no text, no logos"
    },
    {
        "id": "quick-turn-pcb-cross-section",
        "prompt": "Photorealistic 3D render of a multi-layer PCB cross-section viewed under macro lens, showing distinct copper trace layers separated by dark dielectric material, bright gold ENIG surface finish on top, multiple plated through-hole vias visible connecting layers, clean geometric precision, dark technical background, scientific visualization style, no people faces, no text, no logos"
    },
    {
        "id": "quick-turn-pcb-aoi",
        "prompt": "Close-up of an Automated Optical Inspection machine examining a bare PCB board, multiple angled camera lenses with blue LED ring illumination focused on the board surface, the PCB showing fine copper traces and gold pads, dark technical environment with blue ambient glow, precision quality control atmosphere, no people faces, no text, no logos"
    },
    {
        "id": "cta-quick-turn-pcb",
        "prompt": "Abstract wide-angle view of a modern PCB production floor at night, rows of SMT machines with blue status indicator lights forming leading lines toward the back of the factory, clean polished floor reflecting the machine lights, dark atmospheric industrial space, professional electronics manufacturing, no people faces, no text, no logos"
    },
]

os.makedirs(OUT, exist_ok=True)

for i, img in enumerate(IMAGES):
    raw_path = os.path.join(OUT, f"blog-{img['id']}.webp")
    print(f"[{i+1}/{len(IMAGES)}] Generating {img['id']}...")
    
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))
        raw_size = os.path.getsize(raw_path) / 1024
        print(f"  ✓ Raw: {raw_size:.0f}KB — compressing...")
        
        # Compress with cwebp
        result = subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", raw_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ⚠ cwebp failed: {result.stderr.strip()}")
        else:
            final_size = os.path.getsize(raw_path) / 1024
            print(f"  ✓ Compressed: {final_size:.0f}KB")
        
        if i < len(IMAGES) - 1:
            time.sleep(1.5)
            
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        # Remove empty file if created
        if os.path.exists(raw_path) and os.path.getsize(raw_path) == 0:
            os.remove(raw_path)

# Verify
print("\n--- Final files ---")
for img in IMAGES:
    name = f"blog-{img['id']}.webp"
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        size = os.path.getsize(path) / 1024
        print(f"  {name}: {size:.0f}KB")
    else:
        print(f"  {name}: MISSING!")
print("Done.")
