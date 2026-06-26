#!/usr/bin/env python3
"""Gen 4 high-quality mockups per brand for 8 kept brands, using chosen logo as --ref."""
import subprocess, shutil, os, concurrent.futures as cf, threading

GENPY="/home/apple/magnific_api/.venv/bin/python"
GEN="/home/apple/magnific_api/gen.py"
CWD="/home/apple/magnific_api"
FOLDER="ce42d0ef-277c-4568-a50d-9e5af54daf0b"
OUT="/home/apple/Apple/portfolio/deck/mockups"
LOGODIR="/home/apple/Apple/portfolio/deck/logos"
os.makedirs(OUT, exist_ok=True)

# slug, name, concept, [4 mockup scene descriptions]
BRANDS=[
 ("solene","Solène","luxury designer sunglasses brand",[
   "an elegant luxury sunglasses boutique storefront with gold signage at dusk",
   "a premium sunglasses hard case and folded eyewear on marble with soft shadows",
   "a high-fashion magazine ad spread featuring the brand, editorial luxury style",
   "an embossed gold-foil business card and tissue packaging flatlay on black"]),
 ("luma","Lúma","contact lens brand",[
   "a soft pastel contact lens packaging box set with blister packs, clean studio flatlay",
   "a modern pharmacy shelf display of the contact lens products",
   "a branded paper shopping bag and tissue, soft pastel studio mockup",
   "a smartphone showing the brand's clean e-commerce product page"]),
 ("owlie","Owlie","children's eyewear brand",[
   "a playful children's eyewear shop display with colorful kids glasses on a stand",
   "a cute branded kids gift box with tissue paper, bright cheerful studio flatlay",
   "a child-friendly branded tote bag mockup, colorful and fun",
   "a branded sticker sheet and enamel pin set for kids, flatlay"]),
 ("olive-oak","Olive & Oak","upscale fine-dining restaurant, artisanal crafty handmade vibe",[
   "an artisanal letterpress menu on recycled craft paper with wax seal, rustic wood table",
   "a hand-stamped kraft paper bag and twine with the logo, crafty artisan vibe",
   "an embossed leather menu cover and linen napkin on a rustic dining table",
   "ceramic handmade dinnerware with subtle branded detail, warm artisanal photography"]),
 ("bru","Bru","specialty coffee roasters",[
   "a kraft coffee bag packaging with a clear roast-level and single-origin bean label showing Ethiopia Yirgacheffe medium roast",
   "a branded ceramic coffee cup with saucer on a wooden cafe counter",
   "a coffee bag lineup showing different bean origin labels and roast levels on a shelf",
   "a barista apron and branded takeaway cup, cozy cafe scene"]),
 ("kanopi","Kanopi","specialty tea house, cozy English tea room",[
   "a cozy English tea room interior with the brand sign on the wall, warm vintage ambiance",
   "an English afternoon tea set with branded ceramic teapot and cups on a lace tablecloth",
   "a branded tea tin and loose-leaf tea packaging, elegant flatlay",
   "the English tea house storefront exterior with hanging wooden sign and flowers"]),
 ("levain","Levain","artisan sourdough bakery",[
   "an artisan bakery paper bread bag with the logo on a rustic flour-dusted counter",
   "a branded bakery box tied with twine, warm handmade vibe",
   "a chalkboard bakery sign and fresh sourdough loaves, cozy shop interior",
   "branded kraft pastry wrapping and a paper coffee cup, artisan flatlay"]),
 ("buildcore","BuildCore","construction and engineering firm",[
   "a construction worker hi-vis safety vest with the logo, on-site photo",
   "a branded hard hat and project blueprint folder on a site table",
   "a construction site banner and signage with the logo at a building site",
   "a branded engineering business card and letterhead on a concrete surface"]),
]

def prompt(name,concept,mk):
    return (f"Premium professional brand mockup: {mk}. Apply the EXACT logo from the reference image, "
            f"keeping its colors, shapes and wordmark identical and clearly visible. Brand '{name}', a {concept}. "
            f"Realistic high-end commercial photography mockup, beautiful composition, soft natural lighting, "
            f"shallow depth of field, premium Behance-quality presentation, faithful to the reference logo, "
            f"NO garbled text, high resolution, magazine quality.")

TASKS=[]
for slug,name,concept,mks in BRANDS:
    for i,mk in enumerate(mks,1):
        TASKS.append((slug,name,i,prompt(name,concept,mk)))

print(f"Total: {len(TASKS)}",flush=True)
lock=threading.Lock();done=[0];fail=[]
def run(t):
    slug,name,i,pr=t
    dest=f"{OUT}/{slug}-m{i}.png"
    try:
        ref=f"{LOGODIR}/{slug}.png"
        p=subprocess.run([GENPY,GEN,"--prompt",pr,"--ref",ref,"--ar","4:3","--res","2k","--folder",FOLDER],
                         cwd=CWD,capture_output=True,text=True,timeout=300)
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
