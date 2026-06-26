#!/usr/bin/env python3
"""Generate deck.html (Daymark-style) for 15 chosen brands. A4 landscape, print-ready."""
import os

# slug, name, tagline-sentence (bold name embedded), services, palette(list hex), fonts(head,body), group
BRANDS = [
 ("solene","Solène","Crafting <b>Solène</b> into a quiet icon of luxury eyewear.",
  "Visual Identity · Logo System · Packaging · Retail",
  ["#0C0C0C","#C8A24B","#E8DFC8","#F7F4ED"],("Playfair Display","Inter"),"Eyewear"),
 ("luma","Lúma","Giving <b>Lúma</b> a soft, modern voice in vision care.",
  "Visual Identity · Monogram · Packaging · Product",
  ["#2B3A55","#7FB5C9","#E9D8E4","#FBF7F9"],("Poppins","Inter"),"Eyewear"),
 ("owlie","Owlie","Making <b>Owlie</b> a playful friend for little eyes.",
  "Visual Identity · Mascot Mark · Packaging · Retail",
  ["#E8552D","#F2A93B","#3AAE9E","#FFF7EC"],("Poppins","Inter"),"Eyewear"),
 ("optihaus","OptiHaus","Building <b>OptiHaus</b> into a sleek eyewear destination.",
  "Visual Identity · Monogram · Signage · Retail",
  ["#111111","#444444","#9A9A9A","#F2F2F2"],("Inter","Inter"),"Eyewear"),
 ("olive-oak","Olive & Oak","Setting <b>Olive &amp; Oak</b> as a table worth returning to.",
  "Visual Identity · Logo System · Menu · Stationery",
  ["#1C1C18","#3E4A36","#A99368","#F4EFE6"],("Playfair Display","Inter"),"Food & Beverage"),
 ("bru","Bru","Brewing <b>Bru</b> into a daily ritual brand.",
  "Visual Identity · Monogram · Packaging · Cup System",
  ["#2A1A12","#6F4E37","#C8A07A","#F5ECE3"],("Poppins","Inter"),"Food & Beverage"),
 ("kanopi","Kanopi","Rooting <b>Kanopi</b> in nature-led specialty coffee.",
  "Visual Identity · Wordmark · Signage · Packaging",
  ["#1E2A1E","#3F6B3F","#A8763E","#F1EFE6"],("Poppins","Inter"),"Food & Beverage"),
 ("levain","Levain","Shaping <b>Levain</b> into honest, handmade craft.",
  "Visual Identity · Logo System · Packaging · Stationery",
  ["#2B2018","#8A5A2B","#D8B98C","#F7F0E6"],("Playfair Display","Inter"),"Food & Beverage"),
 ("verde","Verde","Pressing <b>Verde</b> into a fresh, plant-led lifestyle.",
  "Visual Identity · Logo System · Bottle · Tote",
  ["#16361F","#3FA34D","#A7D96A","#F3F8EE"],("Poppins","Inter"),"Food & Beverage"),
 ("banh-co","Bánh &amp; Co","Bringing <b>Bánh &amp; Co</b> to the modern Vietnamese street.",
  "Visual Identity · Wordmark · Packaging · Signage",
  ["#1F1206","#C0392B","#E8A33D","#FBF3E7"],("Poppins","Inter"),"Food & Beverage"),
 ("ironclad","Ironclad","Forging <b>Ironclad</b> into a mark of trust on site.",
  "Visual Identity · Monogram · Signage · Workwear",
  ["#141414","#3A3A3A","#C2410C","#EFEFEF"],("Inter","Inter"),"Construction"),
 ("buildcore","BuildCore","Engineering <b>BuildCore</b> for the modern build.",
  "Visual Identity · Logo System · Workwear · Stationery",
  ["#15202B","#2B6CB0","#00A699","#EEF2F5"],("Inter","Inter"),"Construction"),
 ("meridian","Meridian Capital","Positioning <b>Meridian Capital</b> with quiet authority.",
  "Visual Identity · Wordmark · Stationery · Collateral",
  ["#0F1B3D","#1B2A57","#D4AF37","#F4F1E8"],("Playfair Display","Inter"),"Finance"),
 ("vault","Vault","Securing <b>Vault</b> as a modern money brand.",
  "Visual Identity · Logo System · Card · App",
  ["#0A0A0F","#23232E","#6C7BFF","#EDEDF2"],("Inter","Inter"),"Finance"),
 ("terraguard","TerraGuard","Grounding <b>TerraGuard</b> in protection and purpose.",
  "Visual Identity · Wordmark · Report · Tote",
  ["#10241C","#1F6B4F","#3FA9A0","#EEF5F1"],("Poppins","Inter"),"Environment"),
]

GROUPS = ["Eyewear","Food & Beverage","Construction","Finance","Environment"]
GROUP_COLOR = {"Eyewear":"#2B3A55","Food & Beverage":"#3E4A36","Construction":"#C2410C",
               "Finance":"#1B2A57","Environment":"#1F6B4F"}

def mockups(slug):
    out=[]
    for i in (1,2):
        if os.path.exists(f"/home/apple/Apple/portfolio/deck/mockups/{slug}-m{i}.png"):
            out.append(f"mockups/{slug}-m{i}.png")
    return out

def font_link():
    fams=set()
    for b in BRANDS:
        fams.add(b[6-1] if False else b[5][0]); fams.add(b[5][1])
    fams|={"Playfair Display","Inter","Poppins"}
    q="&".join(f"family={f.replace(' ','+')}:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,600" for f in sorted(fams))
    return f"https://fonts.googleapis.com/css2?{q}&display=swap"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#0c0f17}
body{font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;color:#fff}
.slide{width:1122px;height:793px;position:relative;overflow:hidden;page-break-after:always;background:#0c0f17}
.slide:last-child{page-break-after:auto}
.foot{position:absolute;left:48px;right:48px;bottom:26px;display:flex;justify-content:space-between;
  font-size:11px;letter-spacing:.04em;color:rgba(255,255,255,.75);font-weight:500}
.foot .c{position:absolute;left:50%;transform:translateX(-50%)}

/* cover */
.cover{background:radial-gradient(ellipse at 70% 10%,#16243f,#0a0d15 60%)}
.cover .eyebrow{position:absolute;top:48px;left:48px;font-size:13px;letter-spacing:.3em;
  text-transform:uppercase;color:rgba(255,255,255,.7);font-weight:600}
.cover .contact{position:absolute;top:48px;right:48px;text-align:right;font-size:12px;
  line-height:1.7;color:rgba(255,255,255,.7)}
.cover h1{position:absolute;left:44px;bottom:150px;font-size:150px;font-weight:800;
  letter-spacing:-.04em;line-height:.9}
.cover .sub{position:absolute;left:50px;bottom:96px;font-size:18px;color:rgba(255,255,255,.65);font-weight:300;max-width:640px}

/* title card */
.tcard{display:flex;flex-direction:column;justify-content:flex-start;padding:64px}
.tcard .ix{font-size:13px;letter-spacing:.28em;text-transform:uppercase;color:rgba(255,255,255,.55);font-weight:600;margin-bottom:auto}
.tcard h2{font-family:'Playfair Display',serif;font-style:italic;font-weight:500;
  font-size:48px;line-height:1.14;max-width:620px;margin-bottom:18px}
.tcard h2 b{font-style:normal;font-weight:700}
.tcard .svc{font-size:13.5px;letter-spacing:.06em;color:rgba(255,255,255,.7);font-weight:500;margin-bottom:64px;max-width:560px}
.tcard .logo{position:absolute;right:64px;top:120px;width:300px;height:300px;border-radius:18px;
  overflow:hidden;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.tcard .logo img{width:100%;height:100%;object-fit:cover}

/* board (system overview, light) */
.board{background:#f4f3ef;color:#13131a;padding:56px 60px}
.board .label{font-family:'Playfair Display',serif;font-style:italic;font-size:22px;font-weight:600;margin-bottom:4px}
.board .ind{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#8a8a90;font-weight:600;margin-bottom:28px}
.board .grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;height:560px}
.board .cell{background:#fff;border:1px solid #e6e4dd;border-radius:14px;overflow:hidden;position:relative;display:flex;flex-direction:column}
.board .cell .ct{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#9a9a90;font-weight:700;padding:14px 16px 0}
.cell.logo-cell{align-items:center;justify-content:center;background:#fff}
.cell.logo-cell img{width:78%;height:78%;object-fit:contain}
.cell.mock img{width:100%;height:100%;object-fit:cover}
.cell.palette .sw{display:flex;height:100%;width:100%}
.cell.palette .sw div{flex:1}
.pal-wrap{padding:12px 16px 16px;display:flex;flex-direction:column;gap:8px;height:100%}
.pal-row{display:flex;gap:10px;flex:1}
.pal-row .chip{flex:1;border-radius:8px;display:flex;align-items:flex-end;padding:8px;font-size:9px;font-weight:600}
.type-wrap{padding:18px 20px;display:flex;flex-direction:column;justify-content:center;height:100%}
.type-wrap .big{font-size:46px;line-height:1;margin-bottom:6px}
.type-wrap .meta{font-size:11px;color:#8a8a90;letter-spacing:.04em;margin-bottom:14px}
.type-wrap .ag{font-size:13px;color:#444;letter-spacing:.02em}

/* divider */
.divider{display:flex;flex-direction:column;justify-content:flex-start;padding:64px}
.divider .ix{font-size:13px;letter-spacing:.28em;text-transform:uppercase;color:rgba(255,255,255,.6);font-weight:600;margin-bottom:auto}
.divider h2{font-size:72px;font-weight:800;letter-spacing:-.02em;line-height:1.04;max-width:760px}
.divider h2 .lt{font-weight:300;color:rgba(255,255,255,.85)}
.divider .n{font-size:15px;color:rgba(255,255,255,.7);margin-top:18px;font-weight:300}

/* contact */
.contact-slide{background:radial-gradient(ellipse at 30% 0%,#16243f,#0a0d15 60%);
  display:flex;flex-direction:column;justify-content:center;padding:64px}
.contact-slide h1{font-size:120px;font-weight:800;letter-spacing:-.03em;margin-bottom:10px}
.contact-slide p{font-size:18px;color:rgba(255,255,255,.7);font-weight:300;max-width:600px;margin-bottom:40px}
.contact-slide .row{display:flex;gap:60px;font-size:14px;color:rgba(255,255,255,.85)}
.contact-slide .row b{display:block;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.5);margin-bottom:6px;font-weight:600}
@media print{.slide{margin:0}}
"""

def slugcss(b):
    pal=b[4]
    return pal

def chip_text(hex):
    return hex.upper()

def build():
    parts=[]
    # cover
    parts.append("""<section class="slide cover">
  <div class="eyebrow">Logo Portfolio · 2026</div>
  <div class="contact">selected works<br>15 brand identities</div>
  <h1>Logofolio</h1>
  <div class="sub">A curated collection of modern brand identities across eyewear, hospitality, construction, finance &amp; environment.</div>
  <div class="foot"><span>Logofolio</span><span class="c">brand identity</span><span>01</span></div>
</section>""")

    page=2
    for g in GROUPS:
        gb=[b for b in BRANDS if b[6]==g]
        if not gb: continue
        # divider
        gc=GROUP_COLOR[g]
        parts.append(f"""<section class="slide divider" style="background:{gc}">
  <div class="ix">Section · {GROUPS.index(g)+1:02d}</div>
  <h2>{g}.<br><span class="lt">{len(gb)} brand identit{'y' if len(gb)==1 else 'ies'}.</span></h2>
  <div class="n">Selected logo systems and applications.</div>
  <div class="foot"><span>Logofolio</span><span class="c">{g.lower()}</span><span>{page:02d}</span></div>
</section>""")
        page+=1
        for b in gb:
            slug,name,tag,svc,pal,fonts,grp=b
            logo=f"logos/{slug}.png"
            mks=mockups(slug)
            # title card
            parts.append(f"""<section class="slide tcard" style="background:radial-gradient(ellipse at 75% 15%,{pal[1]}33,#0a0d15 62%)">
  <div class="ix">{grp}</div>
  <h2>{tag}</h2>
  <div class="svc">{svc}</div>
  <div class="logo"><img src="{logo}"></div>
  <div class="foot"><span>Logofolio</span><span class="c">{name}</span><span>{page:02d}</span></div>
</section>""")
            page+=1
            # board
            headfont,bodyfont=fonts
            # palette chips
            chips="".join(f'<div class="chip" style="background:{c};color:{"#fff" if i<2 else "#222"}">{chip_text(c)}</div>' for i,c in enumerate(pal))
            mock_cells=""
            if mks:
                mock_cells+=f'<div class="cell mock"><img src="{mks[0]}"></div>'
            if len(mks)>1:
                mock_cells+=f'<div class="cell mock"><img src="{mks[1]}"></div>'
            else:
                # fallback: typography cell duplicate
                mock_cells+=f'''<div class="cell"><div class="ct">Application</div>
                  <div style="flex:1;display:flex;align-items:center;justify-content:center;background:{pal[0]};color:#fff;font-family:'{headfont}';font-size:40px">{name}</div></div>'''
            parts.append(f"""<section class="slide board">
  <div class="label">{name}</div>
  <div class="ind">{grp} · Visual Identity</div>
  <div class="grid">
    <div class="cell logo-cell"><div class="ct" style="position:absolute;top:0;left:0">Logo</div><img src="{logo}"></div>
    <div class="cell"><div class="ct">Color Palette</div>
      <div class="pal-wrap"><div class="pal-row">{chips}</div></div></div>
    <div class="cell"><div class="ct">Typography</div>
      <div class="type-wrap"><div class="big" style="font-family:'{headfont}'">{name}</div>
      <div class="meta">{headfont} · Display &nbsp;/&nbsp; {bodyfont} · Text</div>
      <div class="ag" style="font-family:'{bodyfont}'">ABCDEFGHIJKLM abcdefghijklm 0123456789</div></div></div>
    {mock_cells.split('</div>',0)[0] if False else mock_cells if mks else mock_cells}
  </div>
  <div class="foot" style="color:rgba(0,0,0,.55)"><span>Logofolio</span><span class="c">{name}</span><span>{page:02d}</span></div>
</section>""")
            page+=1

    # contact
    parts.append(f"""<section class="slide contact-slide">
  <h1>Let's talk.</h1>
  <p>Modern brand identity, logo systems and visual direction for ambitious brands.</p>
  <div class="row">
    <div><b>Email</b>hello@logofolio.studio</div>
    <div><b>Web</b>logofolio.studio</div>
    <div><b>Studio</b>Available worldwide</div>
  </div>
  <div class="foot"><span>Logofolio</span><span class="c">thank you</span><span>{page:02d}</span></div>
</section>""")

    html=f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Logofolio — Portfolio Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{font_link()}" rel="stylesheet">
<style>{CSS}</style></head><body>
{''.join(parts)}
</body></html>"""
    with open("/home/apple/Apple/portfolio/deck/index.html","w") as f:
        f.write(html)
    print(f"wrote deck/index.html — {len(parts)} slides")

if __name__=="__main__":
    build()
