#!/usr/bin/env python3
"""Extract real dominant color palette from each chosen logo. Outputs JSON."""
import os, json
from PIL import Image
from collections import Counter

LOGOS="/home/apple/Apple/portfolio/deck/logos"
SLUGS=["solene","luma","owlie","optihaus","olive-oak","bru","kanopi","levain",
       "verde","banh-co","ironclad","buildcore","meridian","vault","terraguard"]

def near_white(r,g,b): return r>238 and g>238 and b>238
def near_gray_bg(r,g,b):
    # very light neutral background filter
    mx,mn=max(r,g,b),min(r,g,b)
    return mx>235 and (mx-mn)<10

def hexify(c): return "#%02X%02X%02X"%c

def extract(path,k=6):
    im=Image.open(path).convert("RGB")
    im.thumbnail((200,200))
    # quantize to palette
    q=im.quantize(colors=32, method=Image.MEDIANCUT).convert("RGB")
    cnt=Counter(q.getdata())
    ranked=[]
    for col,n in cnt.most_common(40):
        r,g,b=col
        if near_gray_bg(r,g,b): continue
        ranked.append((col,n))
    # dedup similar
    out=[]
    for col,n in ranked:
        if all(sum(abs(a-b) for a,b in zip(col,o))>40 for o in out):
            out.append(col)
        if len(out)>=k: break
    if not out:  # fallback: just take most common
        out=[c for c,_ in cnt.most_common(k)]
    return [hexify(c) for c in out]

res={}
for s in SLUGS:
    p=f"{LOGOS}/{s}.png"
    pal=extract(p)
    res[s]=pal
    print(f"{s}: {pal}")

with open("/home/apple/Apple/portfolio/palettes.json","w") as f:
    json.dump(res,f,indent=2)
print("\nwrote palettes.json")
