#!/usr/bin/env python3
"""Generate blog images batch 1: Turnkey article (6 images)"""
import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
outdir = "/home/ubuntu/projects/huaxingpcba/generated"

images = [
    ("blog-cover-turnkey.webp", 
     "Professional industrial photography style: A modern PCB assembly factory floor with automated SMT pick-and-place machines in a clean room environment. Warm amber and blue accent lighting matching a premium dark theme. No people faces, no text, no logos. High-end manufacturing aesthetic."),
    ("blog-turnkey-overview.webp",
     "Clean infographic-style technical diagram showing a turnkey PCB assembly workflow: bare PCB → component procurement → SMT placement → reflow soldering → AOI inspection → conformal coating → box-build. Clean schematic style on dark background with blue and amber accents. No people faces, no text, no logos."),
    ("blog-turnkey-smt-line.webp",
     "Photorealistic SMT production line: multiple high-speed pick-and-place machines in sequence with component feeders visible, conveyor system connecting stations, clean white floor, overhead lighting casting industrial ambiance. Dark theme with amber and blue highlights. No people, no text, no logos."),
    ("blog-turnkey-components.webp",
     "Component inventory and BOM management visualization: neatly organized electronic component reels on shelving, barcode scanners, organized storage system. Modern warehouse aesthetic with subtle blue and amber lighting accents. No people faces, no text, no logos."),
    ("blog-turnkey-cost-comparison.webp",
     "Data visualization style: bar chart comparing costs across volume ranges for turnkey vs consignment PCB assembly. Clean minimalist chart on dark background with blue bars for turnkey and amber for consignment. Abstract financial data visualization. No people, no text, no logos."),
    ("blog-cta-turnkey.webp",
     "Abstract technology background for call-to-action section: subtle geometric circuit board patterns fading to dark gradient, amber and blue glowing traces, premium high-tech atmosphere. Low contrast to not distract from text overlay. No people, no text, no logos."),
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

print("BATCH 1 DONE")
