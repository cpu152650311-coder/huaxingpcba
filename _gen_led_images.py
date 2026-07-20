import os, sys, base64, time, subprocess
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
out_dir = "/home/ubuntu/projects/huaxingpcba/generated"
os.makedirs(out_dir, exist_ok=True)

images = [
    {
        "path": f"{out_dir}/blog-cover-led-pcb.webp",
        "prompt": "macro close-up of a high-power LED PCB with warm white light glowing on aluminum MCPCB substrate, gold ENIG pads, matte white solder mask surface, dark industrial background with subtle gold accent reflections, photorealistic product photography style, shallow depth of field, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-led-pcb-hero.webp",
        "prompt": "horizontal array of LED modules on white aluminum PCB substrate, surface-mount LEDs emitting bright neutral white 4000K light, visible copper traces with gold ENIG finish, clean modern laboratory lighting, top-down macro angle, photorealistic 3D render, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-led-pcb-cross-section.webp",
        "prompt": "photorealistic 3D cross-section render of an aluminum MCPCB for LED applications, showing distinct copper circuit layer on top, thin white dielectric bonding layer in middle, thick aluminum base at bottom, microscopic detail revealing the layered structure, clean studio lighting on dark background, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-led-pcb-solder-mask.webp",
        "prompt": "extreme macro photograph of white solder mask surface on LED PCB under raking light, showing the textured matte surface with subtle reflectance, gold ENIG pad edges visible at frame edge, the white surface catching and diffusing light, scientific industrial photography, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-cta-led-pcb.webp",
        "prompt": "abstract warm ambient glow of LED PCB manufacturing environment, dark navy background with warm gold and amber light halos, subtle reflections on polished aluminum substrate surface, low-contrast atmospheric industrial aesthetic, blurred bokeh effect, no people faces, no text, no logos"
    }
]

results = []
for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating: {os.path.basename(img['path'])}...", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1, size="1024x1024", quality="low"
        )
        b64 = resp.data[0].b64_json
        
        # Save raw
        with open(img["path"] + ".raw", "wb") as f:
            f.write(base64.b64decode(b64))
        
        # Compress with cwebp
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", img["path"] + ".raw", "-o", img["path"]],
            check=True, capture_output=True
        )
        os.remove(img["path"] + ".raw")
        
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  ✓ {size_kb:.0f}KB", flush=True)
        results.append({"file": os.path.basename(img["path"]), "size_kb": size_kb, "status": "ok"})
    except Exception as e:
        print(f"  ✗ FAILED: {e}", flush=True)
        results.append({"file": os.path.basename(img["path"]), "error": str(e), "status": "failed"})
    time.sleep(1.5)

# Summary
ok = sum(1 for r in results if r["status"] == "ok")
print(f"\nDone: {ok}/{len(results)} generated", flush=True)
for r in results:
    if r["status"] == "ok":
        print(f"  {r['file']}: {r['size_kb']:.0f}KB", flush=True)
    else:
        print(f"  {r['file']}: FAILED — {r['error'][:80]}", flush=True)
