#!/usr/bin/env python3
"""Generate 6 blog images for huaxingpcba telecom/5G PCB article."""
import base64, time, os, sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

OUT_DIR = "/home/ubuntu/projects/huaxingpcba/generated"

images = [
    {
        "path": f"{OUT_DIR}/blog-cover-telecom.webp",
        "prompt": (
            "Professional corporate marketing photo, dark premium aesthetic with subtle blue accent lighting (#0066CC glow). "
            "Photorealistic 3D render of a high-frequency telecom PCB with Rogers substrate visible, golden ENIG pads, "
            "dense differential pair routing, and a 5G base station antenna element integrated into the board surface. "
            "The PCB hovers against a dark gradient background transitioning to deep navy, with abstract wave propagation "
            "visualization rendered as subtle light interference patterns. Clean, minimal, editorial photography style. "
            "No people faces, no text, no logos, no arrows, no diagrams, no charts."
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-telecom-overview.webp",
        "prompt": (
            "Macro photography close-up of a telecommunications PCB assembly under inspection lighting. "
            "A high-density 5G base station PCB with distinctive Rogers RO4350B substrate (cream/off-white color), "
            "gold-plated RF connectors, impedance-controlled differential pairs visible as parallel traces, "
            "and multiple QFN packaged RF ICs. Soft directional lighting from upper-left creates shadows that "
            "emphasize trace geometry. Dark navy background with subtle blue accent rim light. "
            "Photorealistic, sharp focus on PCB surface details, shallow depth of field behind the focal plane. "
            "No people faces, no text, no logos, no arrows, no diagrams, no charts."
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-telecom-rf-materials.webp",
        "prompt": (
            "Photorealistic 3D cross-section render of a hybrid PCB stackup for RF applications. "
            "The top layers show Rogers RO4350B material in cream color with uniform ceramic-filled microstructure, "
            "transitioning to darker FR-4 layers below. Copper traces visible in cross-section as bright orange rectangles "
            "embedded within the dielectric. The cross-section cut is clean and precise, like a metallurgical micrograph. "
            "Individual glass weave pattern faintly visible in the FR-4 region. Dark studio lighting, "
            "macro perspective, scientific documentation style. Rich detail in material texture differences between layers. "
            "No people faces, no text, no logos, no arrows, no labels, no diagrams, no charts."
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-telecom-impedance-tdr.webp",
        "prompt": (
            "Close-up studio macro photo of a precision TDR (Time Domain Reflectometer) probe making contact with "
            "gold-plated test pads on a high-frequency PCB. The probe tip is a fine needle touching a golden ENIG pad, "
            "with the PCB surface showing Rogers substrate and controlled-impedance differential pairs. "
            "Soft blue LED lighting from test equipment in the background creates a cool technical atmosphere. "
            "The probe and PCB are in sharp focus, background blurred. Professional lab equipment aesthetic, "
            "clean and precise. Dark background with subtle blue accent lighting (#0066CC tone). "
            "No people faces, no text, no logos, no arrows, no diagrams, no charts."
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-telecom-high-layer-stackup.webp",
        "prompt": (
            "Photorealistic 3D exploded-view render of a 26-layer PCB stackup for telecommunications. "
            "Each dielectric layer is shown separated vertically with copper layers visible as orange/bronze sheets between them. "
            "The top layers are cream-colored Rogers substrate, middle layers are darker FR-4, bottom layers are heavy copper "
            "(thicker, darker orange). Multiple microvias and through-hole vias connect vertically between layers, "
            "shown as metallic columns. The exploded view reveals the internal structure while maintaining a technical, "
            "engineering documentation aesthetic. Dark gradient background, professional lighting highlighting copper and dielectric contrast. "
            "No people faces, no text, no logos, no arrows, no labels, no diagrams, no charts."
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-cta-telecom.webp",
        "prompt": (
            "Abstract dark background for a CTA section. Smooth gradient from deep navy (#0a0e27) at edges to slightly "
            "brighter blue-black at center. Subtle geometric wave propagation patterns rendered as very faint concentric "
            "interference rings, barely visible at 15% opacity. A single diagonal light beam in accent blue (#0066CC) "
            "sweeps across the composition at 35-degree angle, soft and diffused like RF signal visualization. "
            "The overall feel is premium, technical, and minimal — suitable as a dark backdrop for white text overlay. "
            "No people faces, no text, no logos, no arrows, no diagrams, no charts, no distinct objects."
        ),
    },
]

total = len(images)
for i, img in enumerate(images, 1):
    print(f"[{i}/{total}] Generating: {os.path.basename(img['path'])}")
    start = time.time()
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(img["path"], "wb") as f:
            f.write(base64.b64decode(b64))
        elapsed = time.time() - start
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  Done in {elapsed:.1f}s, {size_kb:.0f} KB")
    except Exception as e:
        print(f"  FAILED: {e}")
    if i < total:
        time.sleep(1.5)

print("\nAll done. Files:")
for img in images:
    if os.path.exists(img["path"]):
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  {os.path.basename(img['path'])}: {size_kb:.0f} KB")
    else:
        print(f"  {os.path.basename(img['path'])}: MISSING")
