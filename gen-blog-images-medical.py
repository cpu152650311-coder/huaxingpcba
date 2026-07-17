#!/usr/bin/env python3
"""Generate blog images for huaxingpcba medical-device-pcb article."""
import os, base64, time, sys
from openai import OpenAI

OUTDIR = "/home/ubuntu/projects/huaxingpcba/generated"

# All prompts: no people faces, no text, no logos
# v6.9 blacklist enforced: no infographic/flowchart/arrows/chart/diagram/labeled layers
# Brand colors: dark background (#08080b), gold-copper accent (#c8963e)
# Industrial PCB theme — these are general industrial products, can render PCBs

images = [
    {
        "name": "blog-cover-medical.webp",
        "prompt": (
            "Photorealistic macro close-up of a precision medical-grade PCB with gold ENIG surface finish, "
            "intricate copper traces on dark green solder mask, under dramatic studio lighting with warm golden "
            "highlights. Dark charcoal background with subtle copper reflections. "
            "High-end industrial photography style, shallow depth of field focusing on gold-plated contact pads. "
            "no people faces, no text, no logos, no robots, no product renders"
        )
    },
    {
        "name": "blog-medical-class3.webp",
        "prompt": (
            "Photorealistic 3D cross-section render of a multilayer PCB showing internal copper layers, "
            "plated through-hole barrel with uniform 25 micron copper wall, gold surface finish on top layer. "
            "The cross-section reveals 8 distinct internal layers with perfect registration. "
            "Dark technical background, warm golden edge lighting. Precision engineering aesthetic. "
            "no people faces, no text, no logos, no robots, no product renders"
        )
    },
    {
        "name": "blog-medical-materials.webp",
        "prompt": (
            "Macro photography of multiple PCB material samples arranged on a dark surface: "
            "a rigid polyimide circuit board with gold traces, a High-Tg FR-4 board with dark solder mask, "
            "and a ceramic substrate with precision thin-film gold patterns. "
            "Studio lighting with warm copper-gold reflections on the metallic surfaces. "
            "Dark charcoal background, premium industrial product photography. "
            "no people faces, no text, no logos, no robots, no product renders"
        )
    },
    {
        "name": "blog-medical-cleanroom.webp",
        "prompt": (
            "Photorealistic scene of a PCB under high-magnification optical inspection in a clean manufacturing "
            "environment. A precision green PCB with gold pads under a bright circular inspection light, "
            "surrounded by subtle reflections on polished surfaces. The background is dark and clean, "
            "suggesting a controlled environment. Warm accent lighting from inspection equipment. "
            "no people faces, no text, no logos, no robots, no product renders"
        )
    },
    {
        "name": "blog-medical-testing.webp",
        "prompt": (
            "Macro shot of a precision PCB undergoing automated electrical testing, with gold probe needles "
            "contacting gold-plated test points on a dark green circuit board. Fine copper traces visible under "
            "warm directional lighting. The probe card and test fixture are partially visible in soft focus. "
            "Dark technical background with subtle golden reflections. "
            "no people faces, no text, no logos, no robots, no product renders"
        )
    },
    {
        "name": "blog-cta-medical.webp",
        "prompt": (
            "Abstract dark background with flowing golden-copper geometric patterns suggesting precision "
            "circuit traces and technical excellence. Dark charcoal base (#0f0f14) with warm metallic gold "
            "accents, low contrast, suitable as a text overlay background. Smooth gradients, no sharp edges. "
            "Premium technology aesthetic, subtle and sophisticated. "
            "no people faces, no text, no logos, no robots, no product renders"
        )
    },
]

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

for i, img in enumerate(images):
    path = os.path.join(OUTDIR, img["name"])
    print(f"[{i+1}/{len(images)}] Generating {img['name']}...", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64))
        size_kb = os.path.getsize(path) / 1024
        print(f"  -> OK ({size_kb:.0f} KB)", flush=True)
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)
    time.sleep(1)

print("\nDone. All images saved.", flush=True)
