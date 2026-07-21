import base64, subprocess, time, os
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

IMAGES = [
    {
        "id": "cover-stackup",
        "prompt": "professional corporate marketing photograph of a multi-layer PCB with gold ENIG pads, viewed from a low angle, showing the intricate copper layer structure visible through a polished cross-section edge, dark blue and gold color palette matching premium electronics manufacturing brand, studio lighting with soft shadows, no people faces, no text, no logos, no robots, no arrows, no diagrams, no charts, no infographics"
    },
    {
        "id": "stackup-hero",
        "prompt": "photorealistic extreme macro photograph of a PCB cross-section under industrial microscope lighting, showing 8 distinct copper layers separated by dark FR-4 dielectric material with visible fiberglass weave pattern, plated through-hole barrel connecting multiple layers, clean polished edge revealing precise layer registration, dark technical background, no people faces, no text, no logos, no arrows, no diagrams, no charts"
    },
    {
        "id": "stackup-materials",
        "prompt": "photorealistic 3D render of a hybrid PCB material stackup cross-section, showing layered construction with dark FR-4 substrate transitioning to lighter Rogers high-frequency laminate on outer layers, visible copper planes with metallic grain texture, sliced cleanly at 45 degree angle revealing internal layer construction, studio macro photography style with shallow depth of field, no people faces, no text, no logos, no arrows, no diagrams, no charts"
    },
    {
        "id": "stackup-copper",
        "prompt": "macro photograph of a thick copper PCB power plane with visible grain texture and surface roughness, golden-orange copper traces on dark green substrate, photographed under angled industrial lighting to emphasize the copper thickness, showing multiple trace widths and pad geometries, electronics manufacturing context, no people faces, no text, no logos, no arrows, no diagrams, no charts"
    },
    {
        "id": "cta-stackup",
        "prompt": "professional dark abstract photograph of precision-engineered PCB stackup layers emerging from a clean manufacturing environment, dark blue and gold color scheme matching premium electronics brand, subtle depth of field showing layered construction, suitable for use as website CTA section background with text overlay space, no people faces, no text, no logos, no arrows, no diagrams, no charts"
    },
]

out_dir = "/home/ubuntu/projects/huaxingpcba/generated"
os.makedirs(out_dir, exist_ok=True)

for img in IMAGES:
    raw_path = os.path.join(out_dir, f"blog-{img['id']}-raw.webp")
    final_path = os.path.join(out_dir, f"blog-{img['id']}.webp")
    
    print(f"Generating {img['id']}...")
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
    print(f"  Raw: {raw_size:.0f}KB")
    
    # Compress with cwebp
    subprocess.run(
        ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
        check=True
    )
    final_size = os.path.getsize(final_path) / 1024
    print(f"  Compressed: {final_size:.0f}KB")
    
    os.remove(raw_path)
    time.sleep(1)

# Verify
print("\n=== Final files ===")
for img in IMAGES:
    fp = os.path.join(out_dir, f"blog-{img['id']}.webp")
    sz = os.path.getsize(fp) / 1024
    print(f"  blog-{img['id']}.webp: {sz:.0f}KB {'OK' if sz < 200 else 'OVER 200KB!'}")

print("\nDone.")
