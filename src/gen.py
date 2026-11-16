#!/usr/bin/env python3
"""Generate the full PTC Creatives static site from the hero/sections blocks + page templates."""
import re, os, shutil
from PIL import Image
from home_sections import apply_home, RAIL, HOME_CSS, HOME_JS
from consent import CONSENT_HTML, CONSENT_CSS, CONSENT_JS
from casestudy import build_case, CS_CSS, CS_JS
from pata_section import (SEC_PATA, PATA_CSS, PATA_JS, PRELUDE_HTML,
                          PAGE_CSS, PAGE_JS, SVG_LOTUS, SVG_FISH, SVG_FEATHER)

OUT = "site"
os.makedirs(f"{OUT}/css", exist_ok=True)
os.makedirs(f"{OUT}/js", exist_ok=True)
os.makedirs(f"{OUT}/img", exist_ok=True)

# ---------- images ----------
IMGS = {"sun": "sun.webp", "figure": "figure.webp", "ribbon": "ribbon_embed.webp",
        "lotus": "lotus.webp", "fish1": "fish1.webp", "fish2": "fish2.webp",
        "peacock": "peacock_embed.webp", "border": "border.webp", "logo": "logo_light.webp"}
for k, f in IMGS.items():
    shutil.copy(f"layers/{f}", f"{OUT}/img/{k}.webp")
shutil.copy("/mnt/user-data/uploads/bcad9c23-image.jpg", f"{OUT}/img/og.jpg")
# ---------- favicon: PTC wordmark on a cream pata-paper tile ----------
def _make_icon(size, out):
    tile = Image.new("RGBA", (size, size), (244, 233, 210, 255))
    mark = Image.open("iconsrc/site-icon.png").convert("RGBA")
    mw = round(size * 0.82)
    mh = round(mark.height * mw / mark.width)
    mark = mark.resize((mw, mh), Image.LANCZOS)
    tile.paste(mark, ((size - mw) // 2, (size - mh) // 2), mark)
    # softly rounded corners
    from PIL import ImageDraw
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size, size], radius=size // 6, fill=255)
    tile.putalpha(m)
    tile.save(f"{OUT}/img/{out}")
if os.path.exists("iconsrc/site-icon.png"):
    _make_icon(192, "favicon.png")
    _make_icon(180, "apple-touch.png")
else:
    sun = Image.open("layers/sun.png")
    sun.resize((64, round(sun.height*64/sun.width)), Image.LANCZOS).save(f"{OUT}/img/favicon.png")

# ---------- team photos: center-crop to 2:3, uniform size ----------
os.makedirs(f"{OUT}/img/team", exist_ok=True)
os.makedirs(f"{OUT}/img/work", exist_ok=True)
for _w in os.listdir("workimg"): shutil.copy("workimg/"+_w, f"{OUT}/img/work/"+_w)
# named per person (from the project uploads) — mapping is verified, website order
_team_src = [("mahfuz.jpg","team1"),("sabitul.jpg","team2"),("yousuf.jpg","team3"),
             ("tanjir.jpg","team4"),("josub.png","team5"),("toufiq.png","team6")]
for _fn,_out in _team_src:
    _p = f"teamsrc/{_fn}"
    if not os.path.exists(_p):
        continue
    _im = Image.open(_p).convert("RGB"); _w,_h = _im.size; _tr = 2/3
    if _w/_h > _tr:
        _nw=int(_h*_tr); _x=(_w-_nw)//2; _im=_im.crop((_x,0,_x+_nw,_h))
    else:
        _nh=int(_w/_tr); _y=max(0,min(int((_h-_nh)*0.42),_h-_nh)); _im=_im.crop((0,_y,_w,_y+_nh))
    _im.resize((560,840), Image.LANCZOS).save(f"{OUT}/img/team/{_out}.webp","WEBP",quality=85,method=6)

# ---------- dark logo variant (for daylight nav) ----------
import numpy as _np
_lp = "/mnt/user-data/uploads/ef9ddb74-image.jpg"
if os.path.exists(_lp):
    _a = _np.asarray(Image.open(_lp).convert("RGB")).astype(_np.float32) / 255.0
    _r, _g, _b = _a[..., 0], _a[..., 1], _a[..., 2]
    _ink = _np.clip(((1.0 - _a.min(axis=2)) - 0.06) / 0.80, 0, 1)
    _mx, _mn = _a.max(axis=2), _a.min(axis=2)
    _sat = _np.where(_mx > 0, (_mx - _mn) / _np.maximum(_mx, 1e-6), 0)
    _teal = (_sat > 0.25) & (_b >= _r) & (_g >= _r)
    _o = _np.zeros((*_ink.shape, 4), _np.float32)
    _o[..., 0] = _np.where(_teal, 0x11/255, 0x24/255)
    _o[..., 1] = _np.where(_teal, 0x8c/255, 0x1e/255)
    _o[..., 2] = _np.where(_teal, 0x87/255, 0x16/255)
    _o[..., 3] = _ink
    _li = Image.fromarray((_o * 255).astype(_np.uint8))
    _aa = _np.asarray(_li)[..., 3]; _ys, _xs = _np.where(_aa > 12)
    _li = _li.crop((_xs.min()-4, _ys.min()-4, _xs.max()+4, _ys.max()+4))
    _li.save(f"{OUT}/img/logo_dark.webp", "WEBP", quality=92, method=6)

TOK = {f"@@{k.upper().replace('_EMBED','')}@@": f"img/{k}.webp" for k in
       ["sun", "figure", "lotus", "fish1", "fish2", "border", "logo"]}
TOK["@@RIBBON@@"] = "img/ribbon.webp"
TOK["@@PEACOCK@@"] = "img/peacock.webp"

def detok(s):
    for t, p in TOK.items():
        s = s.replace(t, p)
    return s

# ---------- extract from existing blocks ----------
hero_src = open("hero_block.html").read()
sect_src = open("sections_block.html").read()

def style_of(s):  return re.search(r"<style>(.*?)</style>", s, re.S).group(1)
def inline_js(s): return re.findall(r"<script>(.*?)</script>", s, re.S)[-1]

hero_css, sect_css = style_of(hero_src), style_of(sect_src)
hero_js,  sect_js  = inline_js(hero_src), inline_js(sect_src)

hero_body = re.search(r"(<section id=\"ptc-hero\">.*?</section>)", hero_src, re.S).group(1)
sect_body = re.search(r"(<div id=\"ptc-main\">.*?)\n</div>\n\n<script>", sect_src, re.S).group(1)
# sect_body currently lacks its closing tag (regex stops before it) — note: we re-open/close per page.

# --- patches: hero ---
hero_body = re.sub(r'[ \t]*<img class="ptc-logo"[^>]*>\n', "", hero_body)   # nav carries the logo now
hero_body = hero_body.replace('href="#work">Get Started</a>  <!-- point this at your Contact page -->',
                              'href="contact.html">Get Started</a>')
hero_js = hero_js.replace("var hero=document.getElementById('ptc-hero');",
                          "var hero=document.getElementById('ptc-hero');\n  if(!hero) return;")

# --- wrap sun + motifs in positioning layers, so cursor/velocity effects (on the wrapper)
#     never fight the entrance/scroll tweens (on the img) ---
for _n, _cls in [("sun", "ptc-sun"), ("lotus", "ptc-motif ptc-lotus"), ("fish1", "ptc-motif ptc-fish1"),
                 ("fish2", "ptc-motif ptc-fish2"), ("peacock", "ptc-motif ptc-peacock")]:
    hero_body = re.sub(r'(<img class="' + re.escape(_cls) + r'"[^>]*>)',
                       r'<span class="lyr lyr-' + _n + r'">\1</span>', hero_body)
for _n in ["sun", "lotus", "fish1", "fish2", "peacock"]:
    hero_css = hero_css.replace("#ptc-hero .ptc-" + _n + "{", "#ptc-hero .lyr-" + _n + "{")
hero_css += """
#ptc-hero .lyr{position:absolute;display:block;}
#ptc-hero .lyr img{position:relative!important;left:auto!important;top:auto!important;width:100%!important;display:block;height:auto;}
#ptc-hero .lyr-sun{z-index:2;}
#ptc-hero .lyr-lotus,#ptc-hero .lyr-fish1,#ptc-hero .lyr-fish2,#ptc-hero .lyr-peacock{z-index:5;}
"""

# --- patches: sections ---
sect_body = sect_body.replace('href="#">Learn More', 'href="about.html">Learn More')
sect_body = sect_body.replace('href="#">Contact Us', 'href="contact.html">Contact Us')
sect_body = sect_body.replace('<a class="card ptc-reveal" href="#">',
                              '<a class="card ptc-reveal" href="case-studies.html">')
# --- clients: smooth-scrolling two-row marquee (text now; swap spans for <img> when logo files arrive) ---
CLIENTS = [
    "YGEN Engineering Ltd", "Shonar Bangla Foundation", "United Securities Limited",
    "Fiber at Home", "OFA", "Felicity IDC",
    "Airwrk", "Vendy", "ORCA",
    "Munzer Bangladesh Pvt", "Samuda Chemical Complex Ltd", "Japanese Cars & Motorcycles",
    "Samuda Construction Ltd", "Edventure", "Terre Armee",
    "Volt Mills Energy Ltd", "Wagely", "Helmsman Consulting Ltd",
    "Ex Cadets Forum", "Rock Rankers Ltd", "BEXCA",
    "The Paper Boutique", "Hasan International", "Banglay Likhi",
    "Finesse Nutrition", "Omnicare Diagnostic Limited", "Industry Insider",
    "Jute Alliance Bangladesh", "Shomokal", "Feni Girls Cadet College",
    "Kaler Kontho", "Eventshark", "Krishnopokkho",
    "Young Founders School", "Joyeeta", "Fiverr",
    "Barishal Cadet College", "The Bangladesh Dialogue", "Bioenclave",
    "Chords", "On Record", "WeGro",
]
def mq_row(names, rev=False):
    items = "".join(f"<span>{n}</span>" for n in names)
    return f'<div class="mq-track{" rev" if rev else ""}">{items}{items}</div>'
MQ = f'<div class="mq ptc-reveal">{mq_row(CLIENTS[0::2])}{mq_row(CLIENTS[1::2], True)}</div>'
sect_body = re.sub(r'<div class="client-row ptc-reveal">.*?</div>', MQ, sect_body, flags=re.S)
sect_body = sect_body.replace('<section class="dots">\n    <p class="ptc-eyeb ptc-reveal">Our Services</p>',
                              '<section class="dots" id="services">\n    <p class="ptc-eyeb ptc-reveal">Our Services</p>')

sect_js = (sect_js
    .replace("'#ptc-main .ptc-reveal'", "'.ptc-reveal'")
    .replace("gsap.fromTo('#ptc-main .ptc-proc-bar'",
             "if(document.querySelector('.ptc-proc-bar')) gsap.fromTo('.ptc-proc-bar'")
    .replace("'#ptc-main .ptc-process'", "'.ptc-process'")
    .replace("'#ptc-main .ptc-num'", "'.ptc-num'"))
_OLD_COUNTER = """  /* counters */
  gsap.utils.toArray('.ptc-num').forEach(function(el){
    var end=parseInt(el.getAttribute('data-count'),10)||0;
    ScrollTrigger.create({trigger:el,start:'top 90%',once:true,onEnter:function(){
      var o={v:0};
      gsap.to(o,{v:end,duration:1.6,ease:'power1.out',onUpdate:function(){el.textContent=Math.round(o.v);}});
    }});
  });
"""
assert _OLD_COUNTER in sect_js, "counter block not found in sect_js"
sect_js = sect_js.replace(_OLD_COUNTER, "")

# split sections for reuse on inner pages
def grab(name, pat):
    m = re.search(pat, sect_body, re.S)
    return m.group(1)
# featured film section (YouTube facade: themed poster -> click loads the real embed)
SEC_FEATURED = """
  <!-- ===== FEATURED FILM ===== -->
  <section class="dots" id="featured">
    <p class="ptc-eyeb ptc-reveal">Showreel</p>
    <h2 class="ptc-reveal">Our Work, <em>in Motion</em></h2>
    <p class="lead ptc-reveal">A highlight reel of the films, campaigns and brands we have built. Press play.</p>
    <div class="film ptc-reveal">
      <div class="film-frame" data-yt="YJovd_GEqYw" role="button" tabindex="0" aria-label="Play the PTC Creatives showreel">
        <img class="film-thumb" src="https://i.ytimg.com/vi/YJovd_GEqYw/maxresdefault.jpg" alt="" loading="lazy" onerror="this.remove()">
        <span class="film-shade" aria-hidden="true"></span>
        <span class="film-play" aria-hidden="true"></span>
        <div class="film-cap"><span>Showreel</span><b>PTC Creatives Highlights</b></div>
      </div>
    </div>
  </section>
"""
# place it as a mid-page centerpiece, right after the About strip
sect_body = sect_body.replace("  <!-- ===== PROCESS ===== -->",
                              SEC_FEATURED + "\n  <!-- ===== PROCESS ===== -->", 1)

# ---- team section (face->name mapping UNVERIFIED for the 4 camera-named photos; confirm) ----
# face->name mapping VERIFIED: photos are named per person in the project uploads.
# LinkedIn URLs from the old site's team section. Toufiq's link there duplicated
# Tanjir's (copy error on the old site) -> left out until the real one arrives.
TEAM = [
    ("team1", "Mahfuz Bin Monsur", "Managing Partner",            "https://www.linkedin.com/in/mahfuzbinmonsur/"),
    ("team2", "Sabitul Islam", "Account Lead",                    "https://www.linkedin.com/in/k-m-sabitul-islam-767a422a4/"),
    ("team3", "Yousuf Sabid", "Project Coordinator",              "https://www.linkedin.com/in/yusuf-ibne-humayun-a02b5534b/"),
    ("team4", "Tanjir Pallab", "Lead &ndash; Post Production",    "https://www.linkedin.com/in/tanjir-pallab/"),
    ("team5", "Josub Bin Shoayb", "Visualizer",                   "https://www.linkedin.com/in/josub/"),
    ("team6", "Toufiq Yamin", "Assistant Cinematographer",        None),  # EDIT: add his real LinkedIn URL
]
_team_cards = ""
for _img, _name, _role, _li in TEAM:
    _lia = (f'<a class="tm-li" href="{_li}" target="_blank" rel="noopener" '
            f'aria-label="{_name} on LinkedIn">in</a>') if _li else ""
    _team_cards += f"""      <figure class="tm ptc-reveal">
        <div class="tm-ph"><img src="img/team/{_img}.webp" alt="{_name}" loading="lazy"></div>
        <figcaption><b>{_name}</b><span>{_role}</span>{_lia}</figcaption>
      </figure>\n"""
SEC_TEAM = f"""
  <!-- ===== TEAM =====
       EDIT: names/roles under the 4 camera-named photos are a best guess — confirm the mapping. -->
  <section class="dots pg-dusk" id="team">
    <p class="ptc-eyeb ptc-reveal">Our Team</p>
    <h2 class="ptc-reveal">The People Behind<br>the <em>Work</em></h2>
    <div class="tm-grid">
{_team_cards}    </div>
  </section>
"""

SEC_PROCESS = grab("process", r"(<!-- ===== PROCESS ===== -->.*?</section>)")
SEC_PROCESS_RAW = SEC_PROCESS  # pre-palette copy; used to strip it from the homepage
SEC_STATS   = grab("stats",   r"(<!-- ===== STATS =====.*?</section>)")
SEC_CTA     = grab("cta",     r"(<!-- ===== CTA ===== -->.*?</section>)")
SEC_PROCESS = SEC_PROCESS.replace('<section class="dots ptc-process">', '<section class="ptc-process pg-eve">')
SEC_STATS   = SEC_STATS.replace('<section class="alt">', '<section class="pg-night">')
SEC_CTA     = SEC_CTA.replace('<section class="cta dots">', '<section class="cta dots pg-night">')

# ---------- new shared css ----------
EXTRA_CSS = """
/* ===== site chrome ===== */
html{scroll-behavior:smooth;}
body{margin:0;background:#101f1f;}
.ptc-nav{position:fixed;top:0;left:0;right:0;z-index:60;display:flex;align-items:center;justify-content:space-between;padding:0 7vw;height:76px;font-family:'Poppins',sans-serif;transition:background .3s;}
.ptc-nav.solid,.ptc-nav.open{background:rgba(11,22,22,.94);backdrop-filter:blur(8px);}
.ptc-nav .nlogo{display:flex;align-items:center;}
.ptc-nav .nlogo img{width:140px;display:block;}
.ptc-nav ul{display:flex;gap:36px;list-style:none;margin:0;padding:0;align-items:center;}
.ptc-nav ul a{color:#ffffff;font-size:12.5px;font-weight:400;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;transition:color .25s;}
.ptc-nav ul a:hover{color:#179c97;}
.ptc-nav ul a.on{color:#179c97;}
.ptc-nav .ncta{border:1px solid #179c97;padding:10px 20px;}
.nburger{display:none;background:none;border:none;cursor:pointer;padding:8px;}
.nburger span{display:block;width:24px;height:2px;background:#fff;margin:5px 0;}
@media (max-width:900px){
  .ptc-nav ul{display:none;position:fixed;top:76px;left:0;right:0;background:#0b1616;flex-direction:column;align-items:flex-start;padding:28px 7vw 40px;gap:24px;}
  .ptc-nav.open ul{display:flex;}
  .nburger{display:block;}
}
/* ===== inner page band ===== */
#ptc-main .band{padding:190px 7vw 80px;}
#ptc-main .band h1{font-size:50px;font-weight:600;line-height:1.12;color:#ffffff;margin:0 0 18px;}
#ptc-main .band h1 em{font-style:normal;color:#179c97;}
@media (max-width:600px){#ptc-main .band{padding:150px 24px 60px;}#ptc-main .band h1{font-size:34px;}}
/* ===== services page rows ===== */
#ptc-main .srow{display:grid;grid-template-columns:84px 1fr;gap:30px;padding:48px 0;border-bottom:1px solid rgba(255,255,255,.08);}
#ptc-main .srow svg{width:54px;height:54px;stroke:#179c97;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;}
#ptc-main .srow h3{font-size:22px;font-weight:600;color:#ffffff;margin:0 0 10px;}
#ptc-main .srow p{font-weight:300;font-size:15.5px;line-height:1.75;color:rgba(255,255,255,.68);margin:0 0 16px;max-width:640px;}
#ptc-main .srow ul{margin:0;padding:0;list-style:none;columns:2;max-width:560px;}
#ptc-main .srow li{font-weight:300;font-size:14px;color:rgba(255,255,255,.65);padding:4px 0 4px 18px;position:relative;break-inside:avoid;}
#ptc-main .srow li::before{content:'';position:absolute;left:0;top:11px;width:8px;height:2px;background:#e8a317;}
@media (max-width:600px){#ptc-main .srow{grid-template-columns:1fr;gap:14px;}#ptc-main .srow ul{columns:1;}}
/* ===== values cards (about) ===== */
#ptc-main .val-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:56px;}
@media (max-width:900px){#ptc-main .val-grid{grid-template-columns:1fr;}}
/* ===== contact ===== */
#ptc-main .c-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:10px;}
#ptc-main .c-card{background:#15292a;padding:34px 30px;border-top:2px solid rgba(23,156,151,.25);}
#ptc-main .c-card h3{font-size:13px;font-weight:400;letter-spacing:.3em;text-transform:uppercase;color:#179c97;margin:0 0 14px;}
#ptc-main .c-card p,#ptc-main .c-card a{font-weight:300;font-size:16px;line-height:1.7;color:rgba(255,255,255,.85);margin:0;text-decoration:none;}
#ptc-main .c-card a:hover{color:#179c97;}
#ptc-main .ptc-form{margin-top:70px;max-width:680px;}
#ptc-main .ptc-form .frow{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
#ptc-main .ptc-form input,#ptc-main .ptc-form textarea{width:100%;background:#15292a;border:1px solid rgba(255,255,255,.1);color:#fff;font:200 15px 'Poppins',sans-serif;padding:15px 16px;margin-bottom:18px;outline:none;transition:border-color .25s;}
#ptc-main .ptc-form input:focus,#ptc-main .ptc-form textarea:focus{border-color:#179c97;}
#ptc-main .ptc-form textarea{min-height:150px;resize:vertical;}
#ptc-main .ptc-form button{background:none;border:1px solid #179c97;color:#fff;padding:14px 32px;font:400 13px 'Poppins',sans-serif;letter-spacing:.18em;text-transform:uppercase;cursor:pointer;transition:background .3s,color .3s;}
#ptc-main .ptc-form button:hover{background:#179c97;color:#101f1f;}
#ptc-main .fmsg{display:none;margin-top:16px;font-weight:300;font-size:15px;line-height:1.6;}
#ptc-main .fmsg.ok{color:#2fc3bd;}
#ptc-main .fmsg.err{color:#ff8a6a;}
#ptc-main .ptc-form .hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none;}
#ptc-main .ptc-form button[disabled]{opacity:.6;cursor:default;}
@media (max-width:900px){#ptc-main .c-grid{grid-template-columns:1fr;}#ptc-main .ptc-form .frow{grid-template-columns:1fr;}}
/* ===== legal / privacy ===== */
#ptc-main .legal{max-width:760px;}
#ptc-main .legal h3{font-size:20px;font-weight:600;color:#fff;margin:40px 0 12px;}
#ptc-main .legal p{font-weight:300;font-size:16px;line-height:1.85;color:rgba(255,255,255,.78);margin:0 0 14px;}
#ptc-main .legal p em{font-style:normal;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#179c97;}
#ptc-main .legal a{color:#179c97;text-decoration:none;border-bottom:1px solid rgba(23,156,151,.4);}
#ptc-main .legal a:hover{color:#e8a317;border-bottom-color:#e8a317;}
/* ===== footer ===== */
.ptc-footer{background:#0a1414;font-family:'Poppins',sans-serif;padding:76px 7vw 0;}
.ptc-footer .fgrid{display:grid;grid-template-columns:1.2fr .8fr 1fr;gap:50px;}
.ptc-footer .flogo{width:160px;margin-bottom:18px;}
.ptc-footer p,.ptc-footer a,.ptc-footer li{font-weight:300;font-size:14.5px;line-height:1.9;color:rgba(255,255,255,.68);text-decoration:none;}
.ptc-footer a:hover{color:#179c97;}
.ptc-footer h4{font-size:12px;font-weight:400;letter-spacing:.3em;text-transform:uppercase;color:#179c97;margin:0 0 18px;}
.ptc-footer ul{list-style:none;margin:0;padding:0;}
.ptc-footer .fbot{border-top:1px solid rgba(255,255,255,.08);margin-top:56px;padding:24px 0;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:12px;color:rgba(255,255,255,.4);font-weight:300;}
@media (max-width:900px){.ptc-footer .fgrid{grid-template-columns:1fr;gap:36px;}}
/* touch targets: inline links need real height on phones/tablets */
@media (max-width:900px){
  .ptc-footer li a,.ptc-footer p a,.ptc-footer .fbot a{display:inline-block;min-height:40px;line-height:40px;}
  #ptc-main .c-card a{display:inline-block;min-height:44px;line-height:1.5;padding:10px 0;}
  #ptc-main .ix-row{padding-top:30px;padding-bottom:30px;}
  .ptc-nav ul a{display:inline-block;min-height:40px;line-height:40px;}
}
/* ===== client logo marquee ===== */
#ptc-main .mq{position:relative;overflow:hidden;margin-top:48px;}
#ptc-main .mq::before,#ptc-main .mq::after{content:'';position:absolute;top:0;bottom:0;width:120px;z-index:2;pointer-events:none;}
#ptc-main .mq::before{left:0;background:linear-gradient(90deg,#101f1f,transparent);}
#ptc-main .mq::after{right:0;background:linear-gradient(270deg,#101f1f,transparent);}
#ptc-main .mq-track{display:flex;align-items:center;gap:74px;width:max-content;padding-right:74px;animation:mqL 42s linear infinite;}
#ptc-main .mq-track.rev{animation:mqR 50s linear infinite;margin-top:36px;}
#ptc-main .mq:hover .mq-track{animation-play-state:paused;}
@keyframes mqL{to{transform:translateX(-50%)}}
@keyframes mqR{from{transform:translateX(-50%)}to{transform:translateX(0)}}
#ptc-main .mq-track span{font-weight:300;font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.62);white-space:nowrap;transition:color .3s;}
#ptc-main .mq-track span:hover{color:#179c97;}
#ptc-main .mq-track img{height:54px;width:auto;filter:brightness(0) invert(1);opacity:.6;transition:opacity .3s,filter .3s;}
#ptc-main .mq-track img:hover{opacity:1;filter:none;}
@media (prefers-reduced-motion:reduce){#ptc-main .mq-track{animation:none;flex-wrap:wrap;width:auto;}}
/* ===== featured film ===== */
#ptc-main .film{max-width:1000px;margin:56px auto 0;}
#ptc-main .film-frame{position:relative;aspect-ratio:16/9;border-radius:6px;overflow:hidden;cursor:pointer;background:radial-gradient(circle at 50% 42%,#1a3a38,#0c1818);box-shadow:0 30px 70px rgba(0,0,0,.45);outline:none;}
#ptc-main .film-frame::before{content:'';position:absolute;inset:0;background:url(../img/sun.webp) center/320px no-repeat;opacity:.08;}
#ptc-main .film-thumb{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;}
#ptc-main .film-shade{position:absolute;inset:0;z-index:2;background:linear-gradient(to top,rgba(10,20,20,.82),rgba(10,20,20,.1) 55%);}
#ptc-main .film-play{position:absolute;left:50%;top:48%;transform:translate(-50%,-50%);z-index:3;width:84px;height:84px;border-radius:50%;background:rgba(23,156,151,.92);display:flex;align-items:center;justify-content:center;transition:transform .3s,background .3s;box-shadow:0 0 0 0 rgba(23,156,151,.5);animation:filmpulse 2.6s ease-out infinite;}
#ptc-main .film-frame:hover .film-play,#ptc-main .film-frame:focus-visible .film-play{transform:translate(-50%,-50%) scale(1.09);background:#179c97;}
#ptc-main .film-play::before{content:'';border-style:solid;border-width:13px 0 13px 23px;border-color:transparent transparent transparent #fff;margin-left:6px;}
@keyframes filmpulse{0%{box-shadow:0 0 0 0 rgba(23,156,151,.45)}70%{box-shadow:0 0 0 22px rgba(23,156,151,0)}100%{box-shadow:0 0 0 0 rgba(23,156,151,0)}}
#ptc-main .film-cap{position:absolute;left:30px;bottom:26px;z-index:3;}
#ptc-main .film-cap span{display:block;font-size:11.5px;letter-spacing:.24em;text-transform:uppercase;color:#179c97;font-weight:400;margin-bottom:6px;}
#ptc-main .film-cap b{font-size:21px;font-weight:600;color:#fff;}
#ptc-main .film-frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0;z-index:5;}
@media (prefers-reduced-motion:reduce){#ptc-main .film-play{animation:none;}}
@media (max-width:600px){#ptc-main .film-play{width:62px;height:62px;}#ptc-main .film-cap b{font-size:16px;}}
/* ===== team grid ===== */
#ptc-main .tm-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:52px auto 0;max-width:720px;}
#ptc-main .tm{margin:0;background:#15292a;overflow:hidden;border-bottom:2px solid rgba(23,156,151,.25);transition:transform .35s,border-color .35s;}
#ptc-main .tm:hover{transform:translateY(-6px);border-bottom-color:#179c97;}
#ptc-main .tm-ph{position:relative;aspect-ratio:2/3;overflow:hidden;}
#ptc-main .tm-ph img{width:100%;height:100%;object-fit:cover;filter:grayscale(.3) brightness(.95);transition:filter .4s,transform .6s;}
#ptc-main .tm:hover .tm-ph img{filter:none;transform:scale(1.04);}
#ptc-main .tm-ph::after{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(21,41,42,.6),transparent 42%);}
#ptc-main .tm figcaption{position:relative;padding:20px 60px 24px 22px;}
#ptc-main .tm-li{position:absolute;right:16px;top:50%;transform:translateY(-50%);display:flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;border:1px solid rgba(23,156,151,.5);color:#179c97;font-weight:600;font-size:13px;line-height:1;text-decoration:none;transition:background .3s,color .3s,border-color .3s;}
#ptc-main .tm-li:hover{background:#179c97;color:#0a1414;border-color:#179c97;}
#ptc-main .tm figcaption b{display:block;font-size:17px;font-weight:600;color:#fff;}
#ptc-main .tm figcaption span{display:block;margin-top:5px;font-size:12px;font-weight:300;letter-spacing:.14em;text-transform:uppercase;color:#179c97;}
@media (max-width:900px){#ptc-main .tm-grid{grid-template-columns:1fr 1fr;}}
@media (max-width:600px){#ptc-main .tm-grid{grid-template-columns:1fr 1fr;gap:14px;}#ptc-main .tm figcaption{padding:14px 14px 18px;}#ptc-main .tm figcaption b{font-size:14px;}}
/* ===== cross-page transitions (progressive enhancement) ===== */
@view-transition{navigation:auto;}
::view-transition-old(root),::view-transition-new(root){animation-duration:.4s;}
::view-transition-group(ptc-sun){animation-duration:.65s;}
::view-transition-group(ptc-logo){animation-duration:.5s;}
#ptc-hero .ptc-sun{view-transition-name:ptc-sun;}
.ptc-nav .nlogo{view-transition-name:ptc-logo;}
/* sun-lens on inner page bands (morph target) */
#ptc-main .band{position:relative;overflow:hidden;}
.band-sun{position:absolute;right:7vw;top:120px;width:130px;opacity:.95;pointer-events:none;view-transition-name:ptc-sun;animation:sunspin 60s linear infinite;}
@keyframes sunspin{to{transform:rotate(360deg)}}
@media (max-width:700px){.band-sun{width:80px;top:96px;right:24px;opacity:.5;}}
@media (prefers-reduced-motion:reduce){.band-sun{animation:none;}}
/* ===== homepage travelers: hero elements journey down the page ===== */
#trav-fish{position:fixed;bottom:7vh;left:-280px;z-index:3;opacity:0;pointer-events:none;display:flex;gap:26px;align-items:center;will-change:transform;}
#trav-fish img{width:112px;}
#trav-fish img:last-child{width:86px;margin-top:30px;}
@media (max-width:900px){#trav-fish{display:none!important;}}
"""

# ---------- new shared js ----------
EXTRA_JS = """
(function(){
  var nav=document.querySelector('.ptc-nav');
  if(nav){
    var ns=function(){(window.scrollY>40)?nav.classList.add('solid'):nav.classList.remove('solid');};
    window.addEventListener('scroll',ns); ns();
    var bg=nav.querySelector('.nburger');
    if(bg) bg.addEventListener('click',function(){nav.classList.toggle('open');});
    nav.querySelectorAll('ul a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');});});
  }
  var f=document.querySelector('.ptc-form');
  if(f) f.addEventListener('submit',function(e){
    e.preventDefault();
    var msg=f.querySelector('.fmsg'), btn=f.querySelector('button[type=submit]');
    var hp=f.querySelector('[name=_hp]');
    function say(text,kind){ if(!msg) return; msg.textContent=text; msg.className='fmsg '+kind; msg.style.display='block'; }
    if(hp && hp.value){ say('Thanks, your message has been sent.','ok'); f.reset(); return; } /* bot */
    var data={};
    new FormData(f).forEach(function(v,k){ if(k!=='_hp') data[k]=v; });
    var label=btn?btn.textContent:'';
    if(btn){ btn.disabled=true; btn.textContent='Sending...'; }
    say('','');
    fetch(f.getAttribute('action'),{
      method:'POST',
      headers:{'Content-Type':'application/json','Accept':'application/json'},
      body:JSON.stringify(data)
    }).then(function(r){
      if(!r.ok) throw new Error('status '+r.status);
      f.reset();
      say('Thank you. Your message is on its way, we will reply shortly.','ok');
      if(window.ptcTrackLead) window.ptcTrackLead();   /* only on a confirmed send */
    }).catch(function(){
      say('Something went wrong sending that. Please email contact@ptccreatives.com or call +880 1762 206983.','err');
    }).then(function(){
      if(btn){ btn.disabled=false; btn.textContent=label||'Send Message'; }
    });
  });
  var y=document.getElementById('ptc-year'); if(y) y.textContent=new Date().getFullYear();
  /* featured film: click/enter swaps the poster for the YouTube embed */
  document.querySelectorAll('.film-frame').forEach(function(fr){
    function play(){
      var id=fr.getAttribute('data-yt'); if(!id) return;
      fr.innerHTML='<iframe src="https://www.youtube.com/embed/'+id+'?autoplay=1&rel=0" title="PTC Creatives film" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>';
    }
    fr.addEventListener('click',play);
    fr.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();play();}});
  });
})();
/* homepage travelers: the hero's sun and fish journey through the sections */
(function(){
  if(!window.gsap) return;
  var tf=document.getElementById('trav-fish');
  if(!tf) return;
  if(!window.matchMedia('(min-width:901px)').matches) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  var tl=gsap.timeline({scrollTrigger:{trigger:'#services',start:'top 75%',end:'bottom bottom',endTrigger:'#ptc-main',scrub:1.2,invalidateOnRefresh:true}});
  /* fish swim across the bottom, then back the other way */
  tl.to(tf,{opacity:.55,duration:.03},.15)
    .to(tf,{x:function(){return window.innerWidth+340;},duration:.26,ease:'none'},.16)
    .set(tf,{scaleX:-1,y:-50},.46)
    .to(tf,{opacity:.5,duration:.02},.52)
    .to(tf,{x:0,duration:.26,ease:'none'},.53)
    .to(tf,{opacity:0,duration:.05},.82);
})();
"""

# ---------- shared partials ----------
PAGES = {
    "index.html":        ("Home",         "PTC Creatives | Stories Told With Passion", "Creative production house in Dhaka: video production, documentaries, podcasts, design and digital campaigns for businesses worldwide."),
    "about.html":        ("About",        "About | PTC Creatives", "The studio behind the stories: who we are, how we work, and what we believe about content."),
    "services.html":     ("Services",     "Services | PTC Creatives", "Video production, content audit, content strategy, design & printing, social media management and web presence."),
    "case-studies.html": ("Case Studies", "Case Studies | PTC Creatives", "Selected work: documentaries, campaigns, podcasts and corporate films by PTC Creatives."),
    "contact.html":      ("Contact",      "Contact | PTC Creatives", "Schedule a free strategy call with PTC Creatives. No strings attached."),
    "privacy.html":      ("Privacy",      "Privacy Policy | PTC Creatives", "How PTC Creatives handles information collected through ptccreatives.com."),
}
NAV_ITEMS = [("Home","index.html"),("About","about.html"),("Services","services.html"),("Case Studies","case-studies.html")]

SITE = "https://ptccreatives.com"

JSONLD = """<script type="application/ld+json">
{
 "@context":"https://schema.org",
 "@type":"ProfessionalService",
 "name":"PTC Creatives",
 "alternateName":"PTC",
 "slogan":"Inspiring Creative Brilliance",
 "description":"Creative production agency in Dhaka, Bangladesh: video production, documentaries, podcasts, design, events, PR and digital campaigns.",
 "url":"https://ptccreatives.com/",
 "logo":"https://ptccreatives.com/img/favicon.png",
 "image":"https://ptccreatives.com/img/og.jpg",
 "email":"contact@ptccreatives.com",
 "telephone":"+8801762206983",
 "address":{
  "@type":"PostalAddress",
  "streetAddress":"H-1263, Road 10, Avenue 2, Mirpur DOHS",
  "addressLocality":"Dhaka",
  "postalCode":"1216",
  "addressCountry":"BD"
 },
 "areaServed":"Worldwide",
 "sameAs":[
  "https://www.facebook.com/PTCcreatives",
  "https://www.instagram.com/ptccreatives/",
  "https://www.linkedin.com/company/ptc-creatives"
 ]
}
</script>
"""

def head(title, desc, fname="index.html", p=""):
    canon = SITE + "/" + ("" if fname == "index.html" else fname)
    ld = JSONLD if fname == "index.html" else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#101f1f">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:alt" content="PTC Creatives, a Patachitra-inspired illustration of a storyteller filming">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="PTC Creatives">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/img/og.jpg">
{ld}
<link rel="icon" type="image/png" href="{p}img/favicon.png">
<link rel="apple-touch-icon" href="{p}img/apple-touch.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}css/tw.css">
<link rel="stylesheet" href="{p}css/site.css">
</head>
<body>
""" + PRELUDE_HTML

def nav(active, day=False, p=""):
    links = "".join(f'<li><a href="{p}{href}"{" class=\"on\"" if label==active else ""}>{label}</a></li>'
                    for label, href in NAV_ITEMS)
    return f"""<nav class="ptc-nav{' nav-day' if day else ''}">
  <a class="nlogo" href="{p}index.html"><img class="lg-l" src="{p}img/logo.webp" alt="PTC Creatives"><img class="lg-d" src="{p}img/logo_dark.webp" alt="PTC Creatives"></a>
  <ul>{links}<li><a class="ncta" href="{p}contact.html">Contact Us</a></li></ul>
  <button class="nburger" aria-label="Menu"><span></span><span></span><span></span></button>
</nav>
"""

def band_motif(svg):
    return '<span class="band-motif" aria-hidden="true">' + svg.replace('class="dr ', 'class="dr dr-page ') + '</span>'
BM_LOTUS, BM_FISH, BM_FEATHER = band_motif(SVG_LOTUS), band_motif(SVG_FISH), band_motif(SVG_FEATHER)

def footer(p=""):
  return f"""<footer class="ptc-footer">
  <div class="fgrid">
    <div>
      <img class="flogo" src="{p}img/logo.webp" alt="PTC Creatives">
      <p>Inspiring Creative Brilliance for businesses all around the world. A creative production house based in Dhaka, Bangladesh.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <ul>
        <li><a href="{p}index.html">Home</a></li>
        <li><a href="{p}about.html">About</a></li>
        <li><a href="{p}services.html">Services</a></li>
        <li><a href="{p}case-studies.html">Case Studies</a></li>
        <li><a href="{p}contact.html">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul>
        <li>H-1263, Road 10, Avenue 2,<br>Mirpur DOHS, Dhaka-1216, Bangladesh</li>
        <li><a href="tel:+8801762206983">+880 1762 206983</a></li>
        <li><a href="mailto:contact@ptccreatives.com">contact@ptccreatives.com</a></li>
        <li><a href="https://www.facebook.com/PTCcreatives" target="_blank" rel="noopener">Facebook</a> · <a href="https://www.instagram.com/ptccreatives/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.linkedin.com/company/ptc-creatives" target="_blank" rel="noopener">LinkedIn</a></li>
      </ul>
    </div>
  </div>
  <div class="fbot">
    <span>© <span id="ptc-year">2026</span> PTC Creatives. All rights reserved.</span>
    <span><a href="{p}privacy.html">Privacy Policy</a> &nbsp;·&nbsp;
      <button class="ck-reopen" type="button">Cookie settings</button> &nbsp;·&nbsp;
      Inspiring Creative Brilliance</span>
  </div>
</footer>
""" + CONSENT_HTML + f"""
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.4/dist/lenis.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="{p}js/main.js"></script>
</body>
</html>
"""

# ---------- page bodies ----------
# small sun-lens on every inner page band; shares a view-transition-name with the
# hero sun so browsers morph it between pages on navigation
BAND_SUN = '<img class="band-sun" src="img/sun.webp" alt="" aria-hidden="true">'

TRAVELERS = """
  <div id="trav-fish" aria-hidden="true"><img src="img/fish1.webp" alt=""><img src="img/fish2.webp" alt=""></div>
"""
# homepage: About strip + Process move into the unrolling-scroll chapter (About page keeps its own copies)
sect_home = sect_body.replace(SEC_PROCESS_RAW, "")  # "How We Work" lives in the scroll chapter now
sect_home = re.sub(r"\n  <!-- ===== ABOUT STRIP ===== -->.*?</section>\n", "\n", sect_home, flags=re.S)
sect_home = sect_home.replace('<div id="ptc-main">', '<div id="ptc-main">\n' + SEC_PATA, 1)
sect_home = apply_home(sect_home)
BODY_INDEX = hero_body + "\n" + sect_home + TRAVELERS + RAIL + "\n</div>\n"

BODY_ABOUT = f"""<div id="ptc-main">
  <section class="band dots pg-day">
    {BAND_SUN}
    {BM_LOTUS}
    <p class="ptc-eyeb ptc-reveal">About Us</p>
    <h1 class="ptc-reveal">The studio behind<br>the <em>stories</em></h1>
    <p class="lead ptc-reveal">PTC Creatives is a creative production house based in Dhaka: part strategy consultancy, part film crew, part design studio.</p>
  </section>
  <section class="dots pg-amber">
    <h2 class="ptc-reveal">Why we <em>exist</em></h2>
    <p class="lead ptc-reveal">Founded in 2025, PTC Creatives was built on a simple belief: businesses don't have a content problem, they have a story problem. From corporate AV films and national documentaries to podcast branding and full digital campaigns, we help organisations say what they actually mean, and say it beautifully.</p>
    <p class="lead ptc-reveal" style="margin-top:18px;">Our visual language draws on the storytelling traditions of Bengal: the scroll, the frame, the motif, rebuilt for the screens your audience actually watches.</p>
    <div class="val-grid">
      <div class="svc ptc-reveal"><h3>End-to-End, In-House</h3><p>Strategy, script, shoot, edit, design and distribution under one roof. Nothing lost in handovers.</p></div>
      <div class="svc ptc-reveal"><h3>Strategy Before Camera</h3><p>Every frame answers a business question. We verify the concept before full production begins.</p></div>
      <div class="svc ptc-reveal"><h3>Rooted, Not Retro</h3><p>Local storytelling instincts, global production standards. Work that stands out in any feed, anywhere.</p></div>
    </div>
  </section>
  {SEC_TEAM}
  {SEC_STATS}
  {SEC_CTA}
</div>
"""

SVC_ICONS = re.findall(r"(<svg viewBox=\"0 0 48 48\">.*?</svg>)", sect_body, re.S)
# the homepage grid supplies six icons; PR & Activation brings its own (megaphone)
SVC_ICONS.append('<svg viewBox="0 0 48 48"><path d="M8 20v8a3 3 0 003 3h4l12 7V10L15 17h-4a3 3 0 00-3 3z"/>'
                 '<path d="M15 31v8a2 2 0 002 2h3a2 2 0 002-2v-6"/><path d="M34 18c3 3 3 9 0 12"/>'
                 '<path d="M39 13c6 6 6 16 0 22"/></svg>')

SERVICES = [
    ("Video Production",
     "Brand stories that capture your company's voice and engage the audience they're made for, built to generate leads, not just views.",
     ["Corporate AV &amp; company profiles","Documentaries","Podcast production","Music videos","TVC &amp; OVC","Event aftermovies"]),
    ("Event Management",
     "Concept to coverage. We plan, run and capture events end to end, handling the production on the ground and on camera.",
     ["Event concept &amp; planning","On-ground management","Multi-camera coverage","Photo &amp; video wrap-up"]),
    ("Content Strategy",
     "Data-driven content plans that turn posting into a system, built for engagement, visibility and measurable business growth.",
     ["Messaging &amp; positioning","Content pillars &amp; calendar","Platform strategy","KPI framework &amp; reporting"]),
    ("Graphic Design &amp; Printing",
     "Ideas turned into bold visuals that strengthen brand identity and capture attention, on screen and on paper.",
     ["Brand identity","Campaign key visuals","Social media creatives","Print collateral"]),
    ("Social Media Management",
     "Strategic campaigns, tailored content and consistent engagement that grow a presence your audience actually follows.",
     ["Monthly calendars &amp; captions","Community management","Paid campaign management","Monthly reporting"]),
    ("Web Presence",
     "Responsive websites, search optimisation and cohesive digital branding, so everything online points the same direction.",
     ["Websites &amp; landing pages","Search engine optimisation","Digital brand consistency"]),
    ("PR &amp; Activation",
     "Campaigns that move from the screen to the street: press outreach, brand partnerships and live activations that put your story in front of real audiences.",
     ["Press &amp; media outreach","Launch events &amp; activations","Influencer &amp; partnership campaigns","Coverage reporting"]),
]
rows = ""
for i, (name, desc, items) in enumerate(SERVICES):
    lis = "".join(f"<li>{x}</li>" for x in items)
    rows += f"""    <div class="srow ptc-reveal">
      {SVC_ICONS[i]}
      <div><h3>{name}</h3><p>{desc}</p><ul>{lis}</ul></div>
    </div>\n"""

BODY_SERVICES = f"""<div id="ptc-main">
  <section class="band dots pg-day">
    {BAND_SUN}
    {BM_FISH}
    <p class="ptc-eyeb ptc-reveal">Our Services</p>
    <h1 class="ptc-reveal">Everything your story needs,<br>under <em>one roof</em></h1>
    <p class="lead ptc-reveal">Six disciplines, one team, so your brand sounds like itself everywhere it appears.</p>
  </section>
  <section class="dots pg-grad-serv" style="padding-top:40px;">
{rows}  </section>
  {SEC_CTA}
</div>
"""

# ---------- case studies (horizontal) ----------
# Add a dict per project. Everything after "approach" is optional.
CASE_STUDIES = [
  {
    "slug": "future-of-capitalism",
    "title": "Future of Capitalism",
    "client": "IBACC",
    "category": "Event Management",
    "year": "2026",
    "cover": "foc",
    "summary": "A startup competition where every logistic ran through our team, from the stage and set design to execution on the day.",
    "brief_head": "A competition that had to feel national",
    "brief": "IBACC came to us with a startup competition and a room to fill. It needed to look like a national platform from the first photograph, and every part of it had to be handled by one team rather than stitched together from vendors.",
    "approach_head": "One team, from drawing to doors open",
    "approach": "We took the whole production in-house: set and stage design, build, lighting, run of show and live coverage. Our crew was on site through the build and stayed through to the final session, shooting stills and video as it happened.",
    "approach_points": ["Stage &amp; set design","Full build and logistics","Lighting and AV","Run of show","Event photography","Video coverage"],
    "gallery": ["foc","fbc","chronicles"],
    "result_head": "A platform that looked the part",
    "results": [],
    "result_text": "PLACEHOLDER: send turnout, reach, coverage or any numbers you have and they drop in here as headline figures.",
  },
]

CASES = [
    ("foc","Event Management","Future of Capitalism","IBACC",
     "A startup competition where every logistic ran through our team, from the stage and set design to execution on the day."),
    ("chronicles","Documentary","Chronicles of Freedom","The Bangladesh Dialogue",
     "A documentary preserving the history of the July Revolution, carried end to end in-house, from the shoots to the screening."),
    ("fbc","Event Management","Future Bangladesh Challenge","The Bangladesh Dialogue",
     "A national case competition finale built to surface policy from the root level, with the stage set and run by us from planning to the closing minute."),
    ("samuda","Corporate Film","PHC Pile Process Films","Samuda Construction Ltd",
     "Narrated films that turn heavy manufacturing into a clear, confident story for clients and partners."),
    ("onrecord","Podcast","On Record with Saif Rubab","On Record",
     "A long-form interview series produced and branded with us, from studio setup through to post."),
    ("fgcc","Institutional Film","Feni Girls' Cadet College","FGCC",
     "An institutional film capturing the character of one of the country's cadet colleges."),
    ("merch","Design","Brand Merchandising","WeGro, United Securities, Momentum",
     "Identity applied across merchandise, print and collateral: totes, notebooks, profiles and packaging."),
    ("almostfriday","Event Coverage","Almost Friday","Chords",
     "Live music coverage, photography and video, capturing the room as it happened."),
]
# EDIT: add a URL as a 6th item in CASES to make a card clickable.
cards = ""
for _i, _c in enumerate(CASES):
    img, tag, title, client, desc = _c[:5]
    _slug = {c["title"]: c["slug"] for c in CASE_STUDIES}.get(title)
    url = ("work/" + _slug + "/") if _slug else (_c[5] if len(_c) > 5 else None)
    _o = f'<a class="card ptc-reveal" href="{url}">' if url else '<div class="card ptc-reveal">'
    _end = "</a>" if url else "</div>"
    _go = '<span class="card-go">View Case Study &rarr;</span>' if url else ""
    cards += f"""      {_o}
        <div class="card-top"><img src="img/work/{img}.webp" alt="{title}" loading="lazy">
          <span class="tag">{tag}</span><span class="card-n">{_i+1:02d}</span></div>
        <div class="card-body"><h3>{title}</h3><p class="client">{client}</p><p>{desc}</p>{_go}</div>
      {_end}\n"""

BODY_CASES = f"""<div id="ptc-main">
  <section class="band dots pg-day">
    {BAND_SUN}
    {BM_FEATHER}
    <p class="ptc-eyeb ptc-reveal">Case Studies</p>
    <h1 class="ptc-reveal">Stories we've <em>told</em></h1>
    <p class="lead ptc-reveal">A selection of films, campaigns and brands we've helped bring to life.</p>
  </section>
  <section class="dots pg-grad-case" id="work" style="padding-top:30px;">
    <div class="work-grid">
{cards}    </div>
    <p class="note ptc-reveal">Selected work. Send us a note to see the full reel.</p>
  </section>
  {SEC_CTA}
</div>
"""


BODY_PRIVACY = """<div id="ptc-main">
  <section class="band dots pg-day">
    {BAND_SUN}
    {BM_LOTUS}
    <p class="ptc-eyeb ptc-reveal">Legal</p>
    <h1 class="ptc-reveal">Privacy <em>Policy</em></h1>
    <p class="lead ptc-reveal">How we handle information collected through this website.</p>
  </section>
  <section class="dots pg-grad-contact" style="padding-top:30px;">
    <div class="legal">
      <p class="ptc-reveal"><em>Last updated: 16 November 2026</em></p>

      <h3 class="ptc-reveal">Who we are</h3>
      <p class="ptc-reveal">PTC Creatives is a creative production agency based at H-1263, Road 10, Avenue 2,
      Mirpur DOHS, Dhaka-1216, Bangladesh. This policy covers the website at ptccreatives.com. If you have any
      question about it, write to <a href="mailto:contact@ptccreatives.com">contact@ptccreatives.com</a>.</p>

      <h3 class="ptc-reveal">What we collect</h3>
      <p class="ptc-reveal">We collect only what you choose to send us. If you fill in the contact form, we
      receive the name, email address, company name and message you enter. If you email or call us directly,
      we hold whatever you share in that conversation. We do not ask for payment details through this site.</p>

      <h3 class="ptc-reveal">How we use it</h3>
      <p class="ptc-reveal">We use your details only to reply to you and to discuss work you have asked us
      about. We do not sell your information, rent it, or share it with anyone for marketing. We do not add you
      to a mailing list unless you ask us to.</p>

      <h3 class="ptc-reveal">Cookies and advertising</h3>
      <p class="ptc-reveal">We ask before we track you. When you first visit, a banner offers you the choice to
      accept or decline advertising cookies. Nothing is loaded until you accept, and declining does not change
      how the site works. Your choice is stored in your own browser so we do not have to ask again, and you can
      change it at any time through the <button class="ck-reopen" type="button">cookie settings</button> link in
      the footer.</p>
      <p class="ptc-reveal">If you accept, we load the Meta pixel, a small piece of code from Meta (Facebook and
      Instagram). It tells us which pages are visited and lets us show our work to people who have been here
      before, or to audiences that resemble them. It records the pages you view on this site, your IP address and
      general browser information, and sets cookies in your browser. If you decline, none of this loads.</p>
      <p class="ptc-reveal">We do not run any other analytics software on this site.</p>

      <h3 class="ptc-reveal">Third parties</h3>
      <p class="ptc-reveal">The site is hosted on GitHub Pages, which records standard server access logs
      including IP addresses. Typefaces load from Google Fonts. If you press play on the showreel, the video is
      served by YouTube, which may set cookies and record the view under its own policy. If the contact form is
      connected, submissions are delivered through a form-handling service. If you accept advertising cookies,
      Meta Platforms receives the data described above and processes it under its own data policy. Each of these
      providers handles data under its own privacy policy.</p>

      <h3 class="ptc-reveal">How long we keep it</h3>
      <p class="ptc-reveal">We keep enquiry correspondence for as long as it is useful to the working
      relationship, and delete it on request.</p>

      <h3 class="ptc-reveal">Your choices</h3>
      <p class="ptc-reveal">You can ask us what information we hold about you, ask us to correct it, or ask us
      to delete it. Email <a href="mailto:contact@ptccreatives.com">contact@ptccreatives.com</a> and we will
      respond. You can withdraw your consent to advertising cookies whenever you like through the cookie
      settings link in the footer, and you can block cookies in your browser settings, though some embedded
      content may then not work.</p>

      <h3 class="ptc-reveal">Changes</h3>
      <p class="ptc-reveal">If this policy changes, we will update the date at the top of this page.</p>
    </div>
  </section>
</div>
"""

BODY_CONTACT = f"""<div id="ptc-main">
  <section class="band dots pg-day">
    {BAND_SUN}
    {BM_LOTUS}
    <p class="ptc-eyeb ptc-reveal">No Strings Attached</p>
    <h1 class="ptc-reveal">Let's <em>talk</em></h1>
    <p class="lead ptc-reveal">Schedule a free strategy call and tell us what you're trying to say. We'll tell you how we'd say it.</p>
  </section>
  <section class="dots pg-grad-contact" style="padding-top:30px;">
    <div class="c-grid">
      <div class="c-card ptc-reveal"><h3>Call</h3><a href="tel:+8801762206983">+880 1762 206983</a></div>
      <div class="c-card ptc-reveal"><h3>Email</h3><a href="mailto:contact@ptccreatives.com">contact@ptccreatives.com</a></div>
      <div class="c-card ptc-reveal"><h3>Visit</h3><p>H-1263, Road 10, Avenue 2,<br>Mirpur DOHS, Dhaka-1216, Bangladesh</p></div>
    </div>
    <form class="ptc-form ptc-reveal" action="https://submit-form.com/sxPAOlY7L" method="POST">
      <div class="frow">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
      </div>
      <input type="text" name="company" placeholder="Company (optional)">
      <input class="hp" type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <textarea name="message" placeholder="What are you trying to say?" required></textarea>
      <button type="submit">Send Message</button>
      <p class="fmsg"></p>
    </form>
  </section>
</div>
"""

# ---------- write files ----------
css = "/* PTC Creatives — site.css (generated) */\n" + hero_css + "\n" + sect_css + "\n" + EXTRA_CSS + "\n" + PATA_CSS + "\n" + PAGE_CSS + "\n" + HOME_CSS + "\n" + CONSENT_CSS + "\n" + CS_CSS
open(f"{OUT}/css/site.css", "w").write(detok(css).replace("url(img/", "url(../img/"))  # css lives in css/
js = "/* PTC Creatives — main.js (generated) */\n" + hero_js + "\n" + sect_js + "\n" + EXTRA_JS + "\n" + PATA_JS + "\n" + PAGE_JS + "\n" + HOME_JS + "\n" + CONSENT_JS + "\n" + CS_JS
# isolate each module: one uncaught error must never kill the modules after it
# (real module IIFEs open/close at line starts; inner callbacks never do)
_starts = len(re.findall(r"^\(function\(\)\{", js, flags=re.M))
_ends   = len(re.findall(r"^\}\)\(\);", js, flags=re.M))
assert _starts == _ends, f"IIFE mismatch {_starts} vs {_ends}"
js = re.sub(r"^\(function\(\)\{", "(function(){try{", js, flags=re.M)
js = re.sub(r"^\}\)\(\);", "}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();", js, flags=re.M)
open(f"{OUT}/js/main.js", "w").write(js)

bodies = {"index.html": BODY_INDEX, "about.html": BODY_ABOUT, "services.html": BODY_SERVICES,
          "case-studies.html": BODY_CASES, "contact.html": BODY_CONTACT,
          "privacy.html": BODY_PRIVACY.replace("{BAND_SUN}", BAND_SUN).replace("{BM_LOTUS}", BM_LOTUS)}
for fname, (active, title, desc) in PAGES.items():
    html = head(title, desc, fname) + nav(active, day=(fname != "index.html")) + detok(bodies[fname]) + footer()
    open(f"{OUT}/{fname}", "w").write(html)
    print(fname, len(html)//1024, "KB")
# case study pages at /work/<slug>/
CASE_URLS = []
for _ci, _cs in enumerate(CASE_STUDIES):
    _d = f"{OUT}/work/{_cs['slug']}"
    os.makedirs(_d, exist_ok=True)
    _nxt = CASE_STUDIES[(_ci + 1) % len(CASE_STUDIES)] if len(CASE_STUDIES) > 1 else None
    _c = dict(_cs)
    if _nxt: _c["next"] = {"title": _nxt["title"], "href": "../" + _nxt["slug"] + "/"}
    _p = "../../"
    _title = f"{_cs['title']} | PTC Creatives"
    _desc = _cs["summary"][:155]
    _html = (head(_title, _desc, f"work/{_cs['slug']}/", _p)
             + nav("Case Studies", day=True, p=_p)
             + build_case(_c, _p)
             + footer(_p))
    open(f"{_d}/index.html", "w").write(_html)
    CASE_URLS.append(f"work/{_cs['slug']}/")
    print("case:", _cs["slug"])

# ---------- robots.txt + sitemap.xml ----------
import datetime
_today = datetime.date.today().isoformat()
open(f"{OUT}/robots.txt", "w").write(
    "User-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n")
_prio = {"index.html": "1.0", "services.html": "0.9", "case-studies.html": "0.9",
         "about.html": "0.8", "contact.html": "0.8", "privacy.html": "0.3"}
_prio.update({_u: "0.8" for _u in CASE_URLS})
_urls = ""
for _f in list(PAGES) + CASE_URLS:
    _loc = SITE + "/" + ("" if _f == "index.html" else _f)
    _urls += (f"  <url>\n    <loc>{_loc}</loc>\n    <lastmod>{_today}</lastmod>\n"
              f"    <changefreq>monthly</changefreq>\n    <priority>{_prio.get(_f,'0.5')}</priority>\n  </url>\n")
open(f"{OUT}/sitemap.xml", "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + _urls + "</urlset>\n")
print("seo: robots.txt + sitemap.xml (" + str(len(PAGES) + len(CASE_URLS)) + " urls)")
print("css", os.path.getsize(f"{OUT}/css/site.css")//1024, "KB; js", os.path.getsize(f"{OUT}/js/main.js")//1024, "KB")
