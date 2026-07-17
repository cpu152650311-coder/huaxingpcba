#!/usr/bin/env python3
"""Generate missing rigid-flex images"""
import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
outdir = "/home/ubuntu/projects/huaxingpcba/generated"

images = [
    ("blog-rigid-flex-stackup.webp",
     "Layer stack-up visualization: four rigid-flex configurations (Type 1-4) shown as vertical cross-sections with colored layers indicating rigid (dark blue) and flex (amber) sections. Clean schematic style on dark background. No people, no text, no logos."),
    ("blog-cta-rigid-flex.webp",
     "Abstract technology background: subtle geometric patterns suggesting flexible circuit traces and rigid board sections merging together, fading to dark gradient. Amber and blue glowing accents, premium high-tech atmosphere. Low contrast for text overlay. No people, no text, no logos."),
]

for fname, prompt in images:
    path = os.path.join(outdir, fname)
    if os.path.exists(path):
        print(f"SKIP {fname} (exists)")
        continue
    print(f"Generating {fname}...")
    resp = client.images.generate(
        model="gpt-image-2", prompt=prompt,
        n=1, size="1024x1024", quality="low"
    )
    b64 = resp.data[0].b64_json
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"  ✓ {fname} ({os.path.getsize(path)} bytes)")
    time.sleep(1)

print("BATCH 2b DONE")
