#!/usr/bin/env python3
"""Retry the 2 failed mockups until Magnific quota frees up, then rebuild+render+push."""
import subprocess, shutil, os, time

GENPY="/home/apple/magnific_api/.venv/bin/python"
GEN="/home/apple/magnific_api/gen.py"
CWD="/home/apple/magnific_api"
FOLDER="ce42d0ef-277c-4568-a50d-9e5af54daf0b"
MK="/home/apple/Apple/portfolio/deck/mockups"
LOGOS="/home/apple/Apple/portfolio/deck/logos"

JOBS=[
 ("solene","m2","a luxury sunglasses hard case on a marble surface with a folded pair of elegant sunglasses beside it, soft shadows. Apply the EXACT logo from the reference image onto the case lid, colors shapes wordmark identical, clearly readable, undistorted, correct proportions. Brand 'Solène' luxury designer sunglasses. Realistic high-end product photography, soft natural lighting, shallow depth of field, premium Behance quality, NO garbled text, NO distorted logo"),
 ("olive-oak","m4","handmade artisanal ceramic dinnerware on a rustic table, with a SMALL subtle discreet tiny logo printed near the rim of a plate, the logo is small and elegant NOT oversized, occupying a tiny tasteful area. Apply the EXACT logo from the reference image at small scale, colors and shape faithful. Brand 'Olive & Oak' upscale fine dining crafty artisanal. Realistic warm artisanal photography, soft natural lighting, shallow depth of field, premium Behance quality, NO garbled text, small tasteful logo"),
]

def gen(slug,tag,prompt):
    pr=f"Premium professional brand mockup: {prompt}"
    p=subprocess.run([GENPY,GEN,"--prompt",pr,"--ref",f"{LOGOS}/{slug}.png",
                      "--ar","4:3","--res","2k","--folder",FOLDER],
                     cwd=CWD,capture_output=True,text=True,timeout=300)
    out=p.stdout+p.stderr
    path=next((l.strip() for l in reversed(p.stdout.splitlines()) if l.strip().endswith(".png")),None)
    if path and os.path.exists(path):
        shutil.copy(path,f"{MK}/{slug}-{tag}.png")
        return True
    if "429" in out: return "429"
    return False

pending=list(JOBS)
attempt=0
while pending and attempt<40:
    attempt+=1
    still=[]
    for slug,tag,pr in pending:
        r=gen(slug,tag,pr)
        if r is True:
            print(f"OK {slug}-{tag}",flush=True)
        else:
            print(f"retry {slug}-{tag} ({'429' if r=='429' else 'fail'}) attempt {attempt}",flush=True)
            still.append((slug,tag,pr))
        time.sleep(8)
    pending=still
    if pending:
        time.sleep(300)  # wait for quota

if pending:
    print(f"GAVE UP: {[ (s,t) for s,t,_ in pending]}",flush=True)
else:
    # rebuild web images for the 2 updated mockups
    for slug,tag,_ in JOBS:
        subprocess.run(["convert",f"{MK}/{slug}-{tag}.png","-resize","1100x1100>","-quality","85",
                        f"/home/apple/Apple/portfolio/deck/mockups_web/{slug}-{tag}.jpg"])
    P="/home/apple/Apple/portfolio"
    subprocess.run(["python3","build_deck.py"],cwd=P)
    # ensure @page
    idx=f"{P}/deck/index.html"
    s=open(idx).read()
    if "@page" not in s:
        s=s.replace("@media print{.slide{margin:0}}","@page{size:1122px 793px;margin:0}@media print{.slide{margin:0}}")
        open(idx,"w").write(s)
    subprocess.run(["bash","-c",
      f'rm -rf /tmp/cpdfRT && DISPLAY=:0 timeout 120 google-chrome --headless=new --disable-gpu '
      f'--disable-dev-shm-usage --user-data-dir=/tmp/cpdfRT --no-pdf-header-footer '
      f'--print-to-pdf={P}/deck/logofolio-deck.pdf --no-margins "file://{P}/deck/index.html"'])
    subprocess.run(["bash","-c",
      f'cd {P} && git add -A && git commit -qm "Regen Solène case + Olive&Oak plate mockups (smaller logo)" && git push -q'])
    print("DONE_ALL_REGEN",flush=True)
