import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
out_dir = "/home/ubuntu/projects/huaxingpcba/generated"

images = [
    # === AEROSPACE ===
    {"path": f"{out_dir}/blog-cover-aerospace.webp",
     "prompt": "photorealistic macro view of a dark blue multilayer PCB with gold ENIG pads floating against deep space background, tiny satellite silhouette in distant orbit reflected on board surface, precision aerospace electronics, no people faces, no text, no logos, no arrows, no diagrams, moody atmospheric lighting with blue and gold tones"},
    {"path": f"{out_dir}/blog-aerospace-stackup.webp",
     "prompt": "photorealistic 3D cross-section render of an aerospace multilayer PCB showing distinct material layers - dark polyimide, cream PTFE, copper traces with gold ENIG finish, precision vias connecting layers, microscopic detail showing copper barrel plating, no people faces, no text, no logos, no arrows, no diagrams, clean laboratory lighting"},
    {"path": f"{out_dir}/blog-aerospace-materials.webp",
     "prompt": "macro studio photo of three aerospace PCB substrate material samples on dark surface - creamy white PTFE laminate, dark amber Rogers 4350B, and light gray ceramic-filled substrate, each with gold traces and vias, precision engineering materials, no people faces, no text, no logos, no arrows, no diagrams, even diffused lighting"},
    {"path": f"{out_dir}/blog-aerospace-testing.webp",
     "prompt": "macro closeup of a PCB inspection microscope lens examining a gold ENIG circuit board, blue ambient lighting reflecting off the board surface, precision probe touching a solder joint, cleanroom environment feel, no people faces, no text, no logos, no arrows, no diagrams, sterile laboratory aesthetic"},
    {"path": f"{out_dir}/blog-cta-aerospace.webp",
     "prompt": "abstract dark navy blue industrial texture with subtle gold geometric circuit-like patterns fading into darkness, elegant minimal sci-fi atmosphere, brand mood background, no people faces, no text, no logos, no arrows, no diagrams, gradient dark to black edges"},
    
    # === METAL CORE (first batch continuation) ===
    {"path": f"{out_dir}/blog-cover-metal-core.webp",
     "prompt": "photorealistic macro shot of a high-power LED array mounted on silver aluminum metal core PCB, warm white light glowing from LEDs, visible aluminum substrate edge with slight metallic sheen, thermal management vibe, no people faces, no text, no logos, no arrows, no diagrams, dark background with dramatic rim lighting"},
]

for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating {os.path.basename(img['path'])}...")
    resp = client.images.generate(model="gpt-image-2", prompt=img["prompt"], n=1, size="1024x1024", quality="low")
    b64 = resp.data[0].b64_json
    with open(img["path"], "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"  Saved {os.path.getsize(img['path'])} bytes")
    time.sleep(1)

print("DONE batch 1")
