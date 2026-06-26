#!/usr/bin/env python3
"""Gen 6 multi-style options for each of 17 brands via Magnific. Concurrency-limited."""
import subprocess, shutil, os, sys, concurrent.futures as cf, threading

GENPY = "/home/apple/magnific_api/.venv/bin/python"
GEN = "/home/apple/magnific_api/gen.py"
CWD = "/home/apple/magnific_api"
FOLDER = "ce42d0ef-277c-4568-a50d-9e5af54daf0b"
OUT = "/home/apple/Apple/portfolio/options"
os.makedirs(OUT, exist_ok=True)

# brand: (slug, display name, concept/industry, color direction)
BRANDS = [
    ("veo","Veo","optical eyewear clinic, optometry, trustworthy clean","fresh light-blue and white medical"),
    ("solene","Solène","high-fashion designer sunglasses, luxury eyewear","warm gold and black luxury"),
    ("luma","Lúma","contact lens brand, fresh youthful soft","soft pastel and white"),
    ("owlie","Owlie","children's eyewear, playful fun kids glasses","cheerful bright playful"),
    ("optihaus","OptiHaus","modern eyewear retail chain store","sleek monochrome black with one accent"),
    ("olive-oak","Olive & Oak","upscale fine-dining restaurant, premium","elegant monochrome black"),
    ("bru","Bru","specialty third-wave coffee roasters","warm monochrome brown"),
    ("kanopi","Kanopi","specialty coffee roastery, canopy nature","earthy green and brown"),
    ("levain","Levain","artisan craft sourdough bakery","rustic warm cream and brown"),
    ("verde","Verde","healthy juice and plant-based cafe","vibrant fresh green"),
    ("banh-co","Bánh & Co","Vietnamese fusion street-food eatery","warm vibrant local palette"),
    ("ironclad","Ironclad","construction company, industrial strong","industrial monochrome black"),
    ("buildcore","BuildCore","construction and engineering firm","monochrome with one accent color"),
    ("meridian","Meridian Capital","finance investment firm, corporate premium","navy and gold premium"),
    ("vault","Vault","modern fintech, secure digital","sleek monochrome with subtle gradient"),
    ("verdant","Verdant","environmental protection nonprofit","fresh green"),
    ("terraguard","TerraGuard","environmental conservation foundation","earthy green and deep teal"),
]

# 6 distinct style angles
STYLES = [
    ("wordmark","clean typographic wordmark logo, no icon, refined custom lettering only"),
    ("lockup","icon-plus-text lockup, a distinctive minimal symbol above a sans-serif wordmark"),
    ("monogram","minimal monogram / initial-based mark using the brand initials in a geometric container"),
    ("emblem","vintage-inspired badge emblem logo, circular crest with the brand name inside"),
    ("minimal","ultra-minimalist single-line-weight abstract mark with small understated wordmark"),
    ("modern","bold modern geometric mark with strong contemporary wordmark, confident"),
]

def build_prompt(name, concept, color, style_desc):
    return (f"Logo design for '{name}', a {concept} brand. Style: {style_desc}. "
            f"Color direction: {color} monochrome palette. "
            f"Single centered logo on a clean neutral background, NO mockups, NO packaging, "
            f"NO paragraph text, just the logo mark and the brand name spelled exactly '{name}', "
            f"professional Behance-style minimal logo presentation, vector style, high quality.")

TASKS = []
for slug, name, concept, color in BRANDS:
    for i,(stag, sdesc) in enumerate(STYLES, 1):
        TASKS.append((slug, name, i, stag, build_prompt(name, concept, color, sdesc)))

print(f"Total tasks: {len(TASKS)}", flush=True)
lock = threading.Lock()
done = [0]; fail = []

def run(task):
    slug, name, idx, stag, prompt = task
    dest = f"{OUT}/{slug}-{idx}.png"
    if os.path.exists(dest):
        with lock: done[0]+=1
        return f"skip {slug}-{idx}"
    try:
        p = subprocess.run([GENPY, GEN, "--prompt", prompt, "--ar","1:1","--res","2k","--folder",FOLDER],
                           cwd=CWD, capture_output=True, text=True, timeout=240)
        out = p.stdout.strip().splitlines()
        path = next((l.strip() for l in reversed(out) if l.strip().endswith(".png")), None)
        if path and os.path.exists(path):
            shutil.copy(path, dest)
            with lock: done[0]+=1
            return f"ok {slug}-{idx} ({done[0]}/{len(TASKS)})"
        else:
            with lock: fail.append(f"{slug}-{idx}")
            return f"FAIL {slug}-{idx}: no path. stderr={p.stderr[-200:]}"
    except Exception as e:
        with lock: fail.append(f"{slug}-{idx}")
        return f"FAIL {slug}-{idx}: {e}"

with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for r in ex.map(run, TASKS):
        print(r, flush=True)

print(f"\nDONE. ok={done[0]} fail={len(fail)} {fail}", flush=True)
