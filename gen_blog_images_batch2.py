import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
out_dir = "/home/ubuntu/projects/huaxingpcba/generated"

images = [
    {"path": f"{out_dir}/blog-mcpcb-structure.webp",
     "prompt": "photorealistic 3D cross-section macro render of a metal core PCB edge, showing distinct copper circuit layer on top, thin white dielectric bonding layer in middle, and thick silver aluminum base at bottom, microscopic detail of the material boundaries, precision engineering feel, no people faces, no text, no logos, no arrows, no diagrams, bright clean laboratory lighting"},
    {"path": f"{out_dir}/blog-mcpcb-thermal.webp",
     "prompt": "extreme macro closeup of a white LED chip mounted on aluminum metal core PCB surface, visible thermal glow radiating from the LED junction into the metal substrate, warm orange copper traces on silver aluminum background, heat dissipation concept, no people faces, no text, no logos, no arrows, no diagrams, dark background with warm light"},
    {"path": f"{out_dir}/blog-mcpcb-types.webp",
     "prompt": "studio flat-lay photo of three different PCB samples side by side - a silver aluminum MCPCB with white LED, a standard green FR-4 PCB with chips, and a gold-toned copper-core PCB with power components, all on dark surface, comparison showcase, no people faces, no text, no logos, no arrows, no diagrams, even shadowless lighting"},
    {"path": f"{out_dir}/blog-cta-metal-core.webp",
     "prompt": "abstract warm orange and cool silver metallic texture gradient, soft bokeh circles suggesting LED light points, industrial yet elegant manufacturing mood background, no people faces, no text, no logos, no arrows, no diagrams, smooth gradient from silver to warm amber"},
]

for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating {os.path.basename(img['path'])}...")
    resp = client.images.generate(model="gpt-image-2", prompt=img["prompt"], n=1, size="1024x1024", quality="low")
    b64 = resp.data[0].b64_json
    with open(img["path"], "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"  Saved {os.path.getsize(img['path'])} bytes")
    time.sleep(1)

print("DONE batch 2")
