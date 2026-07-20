#!/usr/bin/env python3
"""Generate RF PCB blog images using GPT Image 2 via AIHUBMIX."""
import base64, os, time, subprocess, sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

OUT_DIR = "/home/ubuntu/projects/huaxingpcba/generated"

images = [
    {
        "path": f"{OUT_DIR}/blog-cover-rf-pcb.webp",
        "prompt": (
            "dark atmospheric macro photograph of an RF printed circuit board with gold-plated microstrip transmission lines "
            "woven across a dark navy substrate, subtle amber and gold trace highlights, shallow depth of field on central traces, "
            "sophisticated technology aesthetic, dramatic studio lighting from above, no people faces, no text, no logos"
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-rf-pcb-cross-section.webp",
        "prompt": (
            "photorealistic 3D cross-section render of an RF PCB microstrip transmission line, showing copper trace on top, "
            "precise dielectric substrate layer in teal-gray, and solid copper ground plane below, "
            "cutaway view revealing precise layer boundaries, scientific visualization style, "
            "clean laboratory lighting, no people faces, no text, no logos"
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-rf-pcb-materials.webp",
        "prompt": (
            "four physical RF PCB substrate samples placed side by side on a dark matte surface: "
            "one white PTFE with subtle texture, one light tan Rogers laminate, one dark gray ceramic-filled composite, "
            "and one greenish standard FR-4, all under soft diffused studio macro lighting revealing surface textures, "
            "product comparison photography style, no people faces, no text, no logos"
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-rf-pcb-testing.webp",
        "prompt": (
            "extreme close-up macro photo of an RF probe needle making contact with a gold-plated microstrip trace on a dark high-frequency PCB, "
            "TDR testing setup visible in background bokeh, precision measurement atmosphere, "
            "controlled blue-tinted laboratory lighting with gold trace reflections, "
            "no people faces, no text, no logos"
        ),
    },
    {
        "path": f"{OUT_DIR}/blog-cta-rf-pcb.webp",
        "prompt": (
            "abstract dark navy background with flowing gold circuit trace patterns radiating from corner, "
            "subtle hexagonal grid pattern in deep charcoal, elegant technology atmosphere, "
            "low contrast suitable for text overlay, brand-appropriate corporate style, "
            "no people faces, no text, no logos"
        ),
    },
]

total = len(images)
print(f"Generating {total} images for RF PCB article...")

for i, img in enumerate(images, 1):
    print(f"[{i}/{total}] {os.path.basename(img['path'])}", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low",
        )
        b64 = resp.data[0].b64_json
        # Write raw first
        raw_path = img["path"]
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))
        raw_size = os.path.getsize(raw_path)

        # Compress with cwebp
        tmp_path = raw_path + ".tmp"
        result = subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", tmp_path],
            capture_output=True, text=True, check=True
        )
        os.replace(tmp_path, raw_path)
        final_size = os.path.getsize(raw_path)
        print(f"  OK: {raw_size//1024}KB → {final_size//1024}KB", flush=True)
    except Exception as e:
        print(f"  FAILED: {e}", flush=True)
        sys.exit(1)
    time.sleep(1.5)

print(f"\nDone. Checking final sizes:")
for img in images:
    sz = os.path.getsize(img["path"])
    flag = "⚠️ >200KB" if sz > 200_000 else "✓"
    print(f"  {os.path.basename(img['path']):45s} {sz//1024:>5}KB  {flag}")
