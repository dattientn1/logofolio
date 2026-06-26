#!/usr/bin/env python3
"""Gen 2 realistic mockups per brand (15 brands -> 30 imgs). Concurrency 8."""
import subprocess, shutil, os, concurrent.futures as cf, threading

GENPY="/home/apple/magnific_api/.venv/bin/python"
GEN="/home/apple/magnific_api/gen.py"
CWD="/home/apple/magnific_api"
FOLDER="ce42d0ef-277c-4568-a50d-9e5af54daf0b"
OUT="/home/apple/Apple/portfolio/deck/mockups"
os.makedirs(OUT, exist_ok=True)

# slug, name, concept, color, [mockup1, mockup2]
BRANDS=[
 ("solene","Solène","luxury designer sunglasses","warm gold and black",
   ["an elegant sunglasses retail boutique storefront sign","a premium folded eyewear cleaning cloth and case flatlay"]),
 ("luma","Lúma","contact lens brand","soft pastel and white",
   ["a soft pastel contact lens packaging box and blister pack flatlay","a clean cosmetic-style product display stand"]),
 ("owlie","Owlie","children's eyewear","cheerful bright playful",
   ["a colorful kids eyewear shop display with childrens glasses","a playful branded paper gift bag for kids"]),
 ("optihaus","OptiHaus","modern eyewear retail chain","sleek monochrome black",
   ["a modern minimalist optical store exterior signage","a sleek eyewear shopping bag mockup"]),
 ("olive-oak","Olive & Oak","upscale fine-dining restaurant","elegant black and cream",
   ["an elegant restaurant menu cover on a linen table","a premium embossed restaurant business card on dark surface"]),
 ("bru","Bru","specialty coffee roasters","warm brown",
   ["a specialty coffee cup with branded sleeve on wood table","a kraft coffee bag packaging mockup"]),
 ("kanopi","Kanopi","specialty coffee roastery","earthy green and brown",
   ["a coffee roastery storefront wooden sign with greenery","a branded ceramic coffee mug on cafe table"]),
 ("levain","Levain","artisan sourdough bakery","rustic cream and brown",
   ["an artisan bakery paper bread bag on rustic counter","a branded bakery box with twine string"]),
 ("verde","Verde","healthy juice plant-based cafe","vibrant fresh green",
   ["a fresh cold-pressed juice bottle with branded label","a healthy cafe reusable tote bag mockup"]),
 ("banh-co","Bánh & Co","Vietnamese fusion street food","warm vibrant local",
   ["a modern Vietnamese eatery storefront sign","a branded takeaway food paper bag mockup"]),
 ("ironclad","Ironclad","construction company","industrial black",
   ["a construction site safety helmet with logo","a branded construction company business card on concrete"]),
 ("buildcore","BuildCore","construction engineering firm","monochrome with accent",
   ["a construction worker hi-vis vest with logo","a branded engineering project folder mockup"]),
 ("meridian","Meridian Capital","finance investment firm","navy and gold",
   ["an elegant corporate letterhead and envelope on desk","a premium finance business card navy and gold"]),
 ("vault","Vault","modern fintech","sleek monochrome gradient",
   ["a sleek fintech debit card mockup","a modern banking app on a smartphone screen"]),
 ("terraguard","TerraGuard","environmental conservation foundation","earthy green and teal",
   ["an eco organization tote bag in nature","a branded sustainability report cover mockup"]),
]

def prompt(name,concept,color,mk):
    return (f"Professional brand mockup: {mk}, featuring the logo of '{name}', a {concept} brand. "
            f"Color palette: {color}. Realistic product/environment photography mockup, premium presentation, "
            f"clean composition, soft studio lighting, the brand name '{name}' spelled correctly, "
            f"minimal clutter, NO garbled text, NO paragraph text, high quality, Behance-style mockup.")

TASKS=[]
for slug,name,concept,color,mks in BRANDS:
    for i,mk in enumerate(mks,1):
        TASKS.append((slug,name,i,prompt(name,concept,color,mk)))

print(f"Total: {len(TASKS)}",flush=True)
lock=threading.Lock();done=[0];fail=[]
def run(t):
    slug,name,i,pr=t
    dest=f"{OUT}/{slug}-m{i}.png"
    if os.path.exists(dest):
        with lock:done[0]+=1
        return f"skip {slug}-m{i}"
    try:
        p=subprocess.run([GENPY,GEN,"--prompt",pr,"--ar","4:3","--res","2k","--folder",FOLDER],
                         cwd=CWD,capture_output=True,text=True,timeout=240)
        path=next((l.strip() for l in reversed(p.stdout.splitlines()) if l.strip().endswith(".png")),None)
        if path and os.path.exists(path):
            shutil.copy(path,dest)
            with lock:done[0]+=1
            return f"ok {slug}-m{i} ({done[0]}/{len(TASKS)})"
        with lock:fail.append(f"{slug}-m{i}")
        return f"FAIL {slug}-m{i}: {p.stderr[-150:]}"
    except Exception as e:
        with lock:fail.append(f"{slug}-m{i}")
        return f"FAIL {slug}-m{i}: {e}"

with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for r in ex.map(run,TASKS):print(r,flush=True)
print(f"\nDONE ok={done[0]} fail={len(fail)} {fail}",flush=True)
