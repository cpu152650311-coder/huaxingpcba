#!/usr/bin/env python3
"""Generate 6 images for Flex PCB article — GPT Image 2 via AIHUBMIX"""
import os, base64, time, subprocess, sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

IMAGES = [
    {
        "name": "blog-cover-flex-pcb",
        "prompt": (
            "A single flexible printed circuit board floating diagonally in a dark void, "
            "golden copper traces glowing subtly against amber polyimide substrate, "
            "the board gently curved in an S-shape showing its flexibility, "
            "dramatic studio lighting from above-left casting soft shadows, "
            "photorealistic macro product photography style, dark background #08080b, "
            "gold accent #c8963e on traces, no people faces, no text, no logos, no arrows, no diagram"
        ),
    },
    {
        "name": "blog-flex-pcb-cross-section",
        "prompt": (
            "photorealistic 3D cross-section render of a flex PCB showing distinct material layers: "
            "polyimide base in warm amber, electrodeposited copper trace layer in orange-gold, "
            "acrylic adhesive layer, and transparent polyimide coverlay on top, "
            "the cut edge revealing smooth internal layer boundaries, studio macro shot, "
            "dark technical background, sharp focus on the layer stack, "
            "no people faces, no text, no logos, no arrows, no labels"
        ),
    },
    {
        "name": "blog-flex-pcb-drilling",
        "prompt": (
            "macro close-up of a laser drilling machine creating microvias on a flexible polyimide PCB sheet, "
            "intense focused laser beam hitting the amber substrate, tiny plume of vaporized material, "
            "industrial PCB factory setting with cleanroom atmosphere, the flex sheet held flat on precision stage, "
            "cool blue ambient light with warm laser glow, photorealistic industrial photography, "
            "no people faces, no text, no logos, no arrows"
        ),
    },
    {
        "name": "blog-flex-pcb-dynamic-bend",
        "prompt": (
            "extreme macro photo of a flex PCB bent at a sharp 90-degree angle, "
            "golden copper traces visible through translucent amber polyimide, "
            "the bend radius showing the material's flexibility without cracking, "
            "edge-lit lighting making the substrate glow, dark studio background, "
            "photorealistic product photography, precision manufacturing aesthetic, "
            "no people faces, no text, no logos, no arrows, no diagram"
        ),
    },
    {
        "name": "blog-flex-pcb-wearable",
        "prompt": (
            "a curved flexible PCB conforming to the inner surface of a modern smartwatch wristband, "
            "tiny surface-mount components mounted on the amber flex circuit, "
            "the PCB wrapping naturally around the curved form, sleek consumer electronics context, "
            "soft diffused product photography lighting, dark elegant background, "
            "showing how flex PCB enables compact wearable design, "
            "no watch face visible, no people faces, no text, no logos, no arrows"
        ),
    },
    {
        "name": "blog-cta-flex-pcb",
        "prompt": (
            "abstract close-up of flexible PCB traces forming elegant curved paths on deep dark background, "
            "warm golden copper traces (#c8963e) creating organic flowing patterns against near-black substrate, "
            "shallow depth of field blurring the edges, rich bokeh effect, "
            "photorealistic macro photography, sophisticated dark premium aesthetic, "
            "suitable as a background image with subtle texture, "
            "no people faces, no text, no logos, no arrows, no diagram"
        ),
    },
]

out_dir = os.path.join(os.path.dirname(__file__), "generated")
os.makedirs(out_dir, exist_ok=True)

generated = []
for i, img in enumerate(IMAGES):
    raw_path = os.path.join(out_dir, f"{img['name']}_raw.webp")
    final_path = os.path.join(out_dir, f"{img['name']}.webp")

    if os.path.exists(final_path) and os.path.getsize(final_path) > 1000:
        print(f"[{i+1}/{len(IMAGES)}] SKIP {img['name']}.webp (exists, {os.path.getsize(final_path)} bytes)")
        generated.append(final_path)
        continue

    print(f"[{i+1}/{len(IMAGES)}] Generating {img['name']}... ", end="", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low",
        )
        b64 = resp.data[0].b64_json
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))
        raw_size = os.path.getsize(raw_path)
        print(f"OK ({raw_size} bytes raw)")

        # Compress with cwebp
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
            check=True, capture_output=True,
        )
        os.remove(raw_path)
        final_size = os.path.getsize(final_path)
        print(f"  Compressed: {final_size} bytes ({final_size//1024}KB)")
        generated.append(final_path)

    except Exception as e:
        print(f"FAIL: {e}")
        continue

    time.sleep(1.5)

print(f"\nDone. Generated {len(generated)}/{len(IMAGES)} images.")
for p in generated:
    sz = os.path.getsize(p)
    print(f"  {os.path.basename(p)}: {sz} bytes ({sz//1024}KB)")
