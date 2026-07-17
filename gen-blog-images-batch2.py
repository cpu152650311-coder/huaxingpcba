#!/usr/bin/env python3
"""Generate blog images batch 2: Rigid-Flex article (7 images)"""
import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
outdir = "/home/ubuntu/projects/huaxingpcba/generated"

images = [
    ("blog-cover-rigid-flex.webp",
     "Professional technical photography: A flexible PCB bent in a graceful curve showing the transition between rigid green PCB and golden polyimide flex section. Dark background with dramatic lighting, blue and amber accents. High-end electronics manufacturing aesthetic. No people faces, no text, no logos."),
    ("blog-rigid-flex-structure.webp",
     "Technical cross-section diagram showing rigid-flex PCB layer structure: rigid FR-4 section transitioning to flexible polyimide section with continuous copper traces visible. Clean technical illustration on dark background, cross-sectional cutaway view, blue and amber layered colors. No people, no text, no logos."),
    ("blog-rigid-flex-3d-fold.webp",
     "3D visualization of a rigid-flex PCB folding into a compact form factor: multiple rigid board sections connected by flexible arms being folded like origami into a 3D shape. Futuristic tech aesthetic on dark background with amber and blue glowing traces. No people, no text, no logos."),
    ("blog-rigid-flex-materials.webp",
     "Material comparison diagram: three sample strips showing polyimide (golden amber), LCP (translucent pale), and PTFE (white) flex materials side by side with subtle dimensional markers. Clean laboratory aesthetic, dark background, blue accent lighting. No people, no text, no logos."),
    ("blog-rigid-flex-design-rules.webp",
     "Engineering illustration showing rigid-flex PCB design guidelines: bend radius annotation, trace routing patterns across flex zone, rigid-to-flex transition detail with tapered edge. Clean technical drawing style, dark background, amber and blue lines. No people, no text, no logos."),
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

print("BATCH 2 DONE")
