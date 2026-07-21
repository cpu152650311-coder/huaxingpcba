#!/usr/bin/env python3
"""Generate 5 images for PCB RoHS Compliance blog article."""
import base64, time, os, subprocess, sys
from openai import OpenAI

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
if not API_KEY:
    print("ERROR: AIHUBMIX_API_KEY not set")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url="https://aihubmix.com/v1")
OUT = "/home/ubuntu/projects/huaxingpcba/generated"

IMAGES = [
    {
        "id": "rohs-compliance",
        "role": "cover",
        "prompt": "dark macro photography of lead-free PCB assembly on black workbench, gold ENIG pads reflecting warm industrial light, SAC305 solder joints with characteristic matte silver grain structure, clean modern electronics manufacturing aesthetic, dark background with subtle copper accent lighting, no people faces, no text, no logos, no infographic, no flow diagram, no arrows, no charts"
    },
    {
        "id": "rohs-materials",
        "role": "concept-scene",
        "prompt": "overhead macro shot of RoHS-compliant green FR-4 PCB substrate samples arranged on dark inspection surface, matte green solder mask with uniform surface, halogen-free laminate edge showing fiberglass weave cross-section, subtle gold copper traces visible through mask, color-calibrated industrial photography style, no people faces, no text, no logos, no infographic, no flow diagram, no arrows, no charts"
    },
    {
        "id": "rohs-cross-section",
        "role": "technical-diagram",
        "prompt": "photorealistic 3D cross-section render of lead-free SAC305 solder joint on ENIG PCB pad, distinct intermetallic compound layer visible as thin silver zone between solder and nickel, copper pad structure with 1oz copper thickness, smooth matte solder fillet angle at 15 degrees, dark background with soft directional lighting, scanning electron microscope aesthetic, no people faces, no text, no logos, no infographic, no flow diagram, no arrows, no charts"
    },
    {
        "id": "rohs-inspection",
        "role": "process-illustration",
        "prompt": "close-up of handheld XRF analyzer instrument nozzle pressed against green PCB surface in quality control laboratory, red laser targeting dot visible on solder pad, blurred laboratory background with soft blue ambient light, precision measurement equipment aesthetic, dark industrial table surface, no people faces, no text, no logos, no infographic, no flow diagram, no arrows, no charts"
    },
    {
        "id": "cta-rohs-compliance",
        "role": "cta-bg",
        "prompt": "abstract dark background with subtle geometric circuit board pattern, deep navy black base with copper gold accent lines forming minimal PCB trace patterns, very low contrast texture overlay, warm gold highlights at edges, premium corporate technology aesthetic, moody atmospheric lighting, no people faces, no text, no logos, no infographic, no flow diagram, no arrows, no charts"
    },
]

for i, img in enumerate(IMAGES):
    fname = f"blog-{img['role']}-{img['id']}.webp" if img['role'] != 'cover' and img['role'] != 'cta-bg' else f"blog-{img['role']}-{img['id']}.webp"
    # Fix: proper naming
    if img['role'] == 'cover':
        fname = f"blog-cover-{img['id']}.webp"
    elif img['role'] == 'cta-bg':
        fname = f"blog-cta-{img['id']}.webp"
    else:
        fname = f"blog-{img['id']}.webp"
    
    raw_path = os.path.join(OUT, fname + ".raw")
    final_path = os.path.join(OUT, fname)
    
    print(f"[{i+1}/5] Generating {fname}...")
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
        
        # Compress with cwebp, check=True to avoid silent file loss (pitfall 18a)
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
            check=True, capture_output=True
        )
        os.remove(raw_path)
        
        size_kb = os.path.getsize(final_path) / 1024
        print(f"  OK: {fname} ({size_kb:.0f}KB)")
    except Exception as e:
        print(f"  FAILED: {fname} — {e}")
    
    time.sleep(2)  # rate limit

# Verify all files
print("\n=== Verification ===")
for img in IMAGES:
    if img['role'] == 'cover':
        fname = f"blog-cover-{img['id']}.webp"
    elif img['role'] == 'cta-bg':
        fname = f"blog-cta-{img['id']}.webp"
    else:
        fname = f"blog-{img['id']}.webp"
    path = os.path.join(OUT, fname)
    if os.path.exists(path):
        print(f"  ✓ {fname} ({os.path.getsize(path)/1024:.0f}KB)")
    else:
        print(f"  ✗ {fname} MISSING")
