# Horizontally-scrolling case study pages.
# Give build_case() a dict (see CASE_TEMPLATE at the bottom) and it returns the page body.
# Panel count is dynamic: the day->night ramp and the sun/moon arc stretch to fit.

RAMP = ['#f4e9d2', '#eed8ac', '#d99a4e', '#c0693a', '#7e3528', '#38222e', '#122028', '#0a1414']


def _hex(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def _mix(a, b, t):
    ra, rb = _hex(a), _hex(b)
    return '#%02x%02x%02x' % tuple(round(ra[i] + (rb[i] - ra[i]) * t) for i in range(3))


def _sample(pos):
    """pos 0..1 along the day->night ramp."""
    pos = max(0.0, min(1.0, pos))
    seg = pos * (len(RAMP) - 1)
    i = min(int(seg), len(RAMP) - 2)
    return _mix(RAMP[i], RAMP[i + 1], seg - i)


def _is_light(c):
    r, g, b = _hex(c)
    return (0.299 * r + 0.587 * g + 0.114 * b) > 140


def _grad_strip(n):
    """One gradient span per panel, continuous across the whole track."""
    out = ''
    for i in range(n):
        a, b = _sample(i / n), _sample((i + 1) / n)
        out += f'<span style="background:linear-gradient(90deg,{a},{b})"></span>'
    return out


def _fireflies(n, seed=3):
    import random
    rng = random.Random(seed)
    return ''.join(
        f'<span class="ff" style="left:{rng.randint(8,90)}%;top:{rng.randint(14,76)}%;'
        f'--d:{rng.uniform(2.3,4.3):.1f}s;--dl:{rng.uniform(0,3.2):.1f}s;"></span>'
        for _ in range(n))


def build_case(c, prefix='../../'):
    """c: case dict. prefix: path back to site root from this page."""
    p = prefix
    panels = []

    # ---- 1. title ----
    panels.append(f"""
      <article class="cs-panel cs-title">
        <img class="cs-bg" src="{p}img/work/{c['cover']}.webp" alt="" aria-hidden="true">
        <div class="cs-inner">
          <p class="cs-eyeb">{c['category']}{(' &#183; ' + c['year']) if c.get('year') else ''}</p>
          <h1 class="cs-h1" data-sp="1.3">{c['title']}</h1>
          <p class="cs-client">for {c['client']}</p>
          <p class="cs-lead" data-sp="0.6">{c['summary']}</p>
        </div>
      </article>""")

    # ---- 2. brief ----
    panels.append(f"""
      <article class="cs-panel">
        <div class="cs-inner cs-narrow">
          <p class="cs-eyeb">01 &#183; The Brief</p>
          <h2 class="cs-h2" data-sp="1.4">{c.get('brief_head','What they needed')}</h2>
          <p class="cs-body" data-sp="0.6">{c['brief']}</p>
        </div>
      </article>""")

    # ---- 3. approach ----
    pts = ''.join(f'<li>{x}</li>' for x in c.get('approach_points', []))
    panels.append(f"""
      <article class="cs-panel">
        <div class="cs-inner cs-narrow">
          <p class="cs-eyeb">02 &#183; What We Did</p>
          <h2 class="cs-h2" data-sp="1.4">{c.get('approach_head','How we made it')}</h2>
          <p class="cs-body" data-sp="0.6">{c['approach']}</p>
          {f'<ul class="cs-list" data-sp="0.4">{pts}</ul>' if pts else ''}
        </div>
      </article>""")

    # ---- 4. gallery ----
    if c.get('gallery'):
        shots = ''.join(
            f'<figure class="cs-shot"><img src="{p}img/work/{g}.webp" alt="{c["title"]}" loading="lazy"></figure>'
            for g in c['gallery'])
        panels.append(f"""
      <article class="cs-panel cs-gal-panel">
        <div class="cs-inner">
          <p class="cs-eyeb">03 &#183; On the Day</p>
          <div class="cs-gal">{shots}</div>
        </div>
      </article>""")

    # ---- 5. film ----
    if c.get('video'):
        panels.append(f"""
      <article class="cs-panel">
        <div class="cs-inner">
          <p class="cs-eyeb">04 &#183; The Film</p>
          <div class="cs-film">
            <div class="film-frame" data-yt="{c['video']}" role="button" tabindex="0" aria-label="Play the film">
              <img class="film-thumb" src="https://i.ytimg.com/vi/{c['video']}/maxresdefault.jpg" alt="" loading="lazy" onerror="this.remove()">
              <span class="film-shade" aria-hidden="true"></span><span class="film-play" aria-hidden="true"></span>
            </div>
          </div>
        </div>
      </article>""")

    # ---- 6. results ----
    if c.get('results') or c.get('result_text'):
        stats = ''.join(
            f'<div class="cs-stat"><b>{v}</b><span>{k}</span></div>' for v, k in c.get('results', []))
        panels.append(f"""
      <article class="cs-panel">
        {_fireflies(6)}
        <div class="cs-inner cs-narrow">
          <p class="cs-eyeb">05 &#183; The Result</p>
          <h2 class="cs-h2" data-sp="1.4">{c.get('result_head','What came of it')}</h2>
          {f'<div class="cs-stats" data-sp="0.5">{stats}</div>' if stats else ''}
          <p class="cs-body" data-sp="0.6">{c.get('result_text','')}</p>
        </div>
      </article>""")

    # ---- 7. quote ----
    if c.get('quote'):
        q = c['quote']
        panels.append(f"""
      <article class="cs-panel">
        {_fireflies(5, 9)}
        <div class="cs-inner cs-narrow">
          <blockquote class="cs-quote" data-sp="0.8">&ldquo;{q['text']}&rdquo;</blockquote>
          <p class="cs-attr">{q['who']}{(', ' + q['role']) if q.get('role') else ''}</p>
        </div>
      </article>""")

    # ---- 8. close ----
    nxt = c.get('next')
    panels.append(f"""
      <article class="cs-panel cs-end">
        {_fireflies(8, 17)}
        <div class="cs-inner cs-mid">
          <p class="cs-eyeb">PTC Creatives</p>
          <h2 class="cs-h2 cs-big" data-sp="1.1">Let's tell<br>yours <em>next.</em></h2>
          <div class="cs-acts">
            <a class="ptc-btn" data-mag href="{p}contact.html">Start Your Story</a>
            {f'<a class="cs-next" href="{nxt["href"]}">Next: {nxt["title"]} &rarr;</a>' if nxt else ''}
          </div>
        </div>
      </article>""")

    n = len(panels)
    # per-panel text colour, from the midpoint of that panel's slice of the ramp
    tone = ''.join(
        f'#cs .cs-panel:nth-child({i+1}){{--ink:{"#241e16" if _is_light(_sample((i+.5)/n)) else "#ffffff"};'
        f'--dim:{"rgba(36,30,22,.78)" if _is_light(_sample((i+.5)/n)) else "rgba(255,255,255,.8)"};'
        f'--accent:{"#a8431f" if _is_light(_sample((i+.5)/n)) else "#179c97"};}}'
        for i in range(n))

    return f"""<div id="ptc-main">
  <section id="cs" class="cs" aria-label="{c['title']} case study">
    <style>{tone}
      html.js-h #cs .cs-track{{width:{n*100}vw;}}
      #cs .cs-grad{{width:{n*100}vw;}}
      @media (max-width:899px){{ {''.join(f'#cs .cs-panel:nth-child({i+1}){{background:linear-gradient(180deg,{_sample(i/n)},{_sample((i+1)/n)});}}' for i in range(n))} }}
    </style>
    <div class="cs-pin">
      <div class="cs-sky" aria-hidden="true">
        <div class="cs-grad">{_grad_strip(n)}</div>
        <img class="cs-sun" src="{p}img/sun.webp" alt="">
        <svg class="cs-moon" viewBox="0 0 120 120"><circle cx="60" cy="60" r="44" fill="#f4e9d2"/><circle cx="46" cy="48" r="7" fill="#d9cbae"/><circle cx="72" cy="70" r="5" fill="#d9cbae"/><circle cx="62" cy="38" r="4" fill="#d9cbae"/></svg>
      </div>
      <div class="cs-track">{''.join(panels)}
      </div>
      <div class="cs-rail" aria-hidden="true"><div class="cs-prog"></div></div>
      <a class="cs-back" href="{p}case-studies.html">&larr; All work</a>
    </div>
  </section>
</div>
"""


CS_CSS = """
/* ===== case study: horizontal chapter ===== */
#ptc-main .cs{padding:0;position:relative;}
.cs-pin{position:relative;overflow:hidden;}
.cs-track{display:block;}
.cs-panel{position:relative;min-height:100vh;display:flex;align-items:center;overflow:hidden;padding:120px 7vw 90px;color:var(--ink,#fff);}
.cs-inner{position:relative;z-index:3;width:100%;max-width:1180px;}
.cs-narrow{max-width:760px;}
.cs-mid{max-width:820px;margin:0 auto;text-align:center;}
.cs-eyeb{font-size:12.5px;font-weight:400;letter-spacing:.4em;text-transform:uppercase;color:var(--accent,#179c97);margin:0 0 20px;}
.cs-h1{font-weight:600;font-size:clamp(46px,8vw,124px);line-height:1;letter-spacing:-.015em;margin:0 0 14px;color:var(--ink,#fff);}
.cs-h2{font-weight:600;font-size:clamp(30px,4.4vw,66px);line-height:1.08;margin:0 0 22px;color:var(--ink,#fff);}
.cs-h2 em{font-style:normal;color:transparent;-webkit-text-stroke:1.5px currentColor;}
.cs-big{font-size:clamp(38px,6vw,96px);}
.cs-client{font-size:clamp(15px,1.6vw,21px);font-weight:300;letter-spacing:.16em;text-transform:uppercase;color:var(--accent,#179c97);margin:0 0 26px;}
.cs-lead{font-weight:300;font-size:clamp(17px,1.5vw,23px);line-height:1.75;max-width:640px;color:var(--dim,rgba(255,255,255,.8));margin:0;}
.cs-body{font-weight:300;font-size:clamp(16px,1.35vw,20px);line-height:1.85;color:var(--dim,rgba(255,255,255,.8));margin:0 0 18px;}
.cs-list{margin:26px 0 0;padding:0;list-style:none;columns:2;column-gap:40px;max-width:660px;}
.cs-list li{font-weight:300;font-size:15px;line-height:1.6;color:var(--dim,rgba(255,255,255,.8));padding:7px 0 7px 18px;position:relative;break-inside:avoid;}
.cs-list li::before{content:'';position:absolute;left:0;top:15px;width:9px;height:2px;background:var(--accent,#179c97);}
.cs-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.3;z-index:1;}
.cs-title::after{content:'';position:absolute;inset:0;z-index:2;
  background:linear-gradient(90deg,rgba(244,233,210,.92),rgba(244,233,210,.45));}
.cs-gal{display:flex;gap:22px;align-items:center;margin-top:30px;}
.cs-shot{margin:0;flex:1 1 0;border-radius:4px;overflow:hidden;aspect-ratio:4/5;box-shadow:0 20px 50px rgba(0,0,0,.35);}
.cs-shot img{width:100%;height:100%;object-fit:cover;display:block;}
.cs-film{max-width:900px;margin-top:26px;}
.cs-stats{display:flex;gap:46px;flex-wrap:wrap;margin:0 0 30px;}
.cs-stat b{display:block;font-size:clamp(38px,5vw,64px);font-weight:600;line-height:1;color:var(--accent,#179c97);}
.cs-stat span{display:block;margin-top:10px;font-size:13px;font-weight:400;letter-spacing:.2em;text-transform:uppercase;color:var(--dim,rgba(255,255,255,.8));}
.cs-quote{margin:0 0 22px;font-weight:300;font-size:clamp(22px,2.9vw,44px);line-height:1.4;color:var(--ink,#fff);}
.cs-attr{font-size:13px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;color:var(--accent,#179c97);margin:0;}
.cs-acts{display:flex;gap:26px;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:34px;}
.cs-next{font-size:13px;font-weight:400;letter-spacing:.18em;text-transform:uppercase;color:var(--accent,#179c97);text-decoration:none;border-bottom:1px solid transparent;padding:12px 0;}
.cs-next:hover{border-bottom-color:currentColor;}
.cs-back{position:absolute;left:7vw;top:104px;z-index:20;font-size:12.5px;font-weight:400;letter-spacing:.18em;
  text-transform:uppercase;color:#fff;mix-blend-mode:difference;text-decoration:none;padding:10px 0;
  border-bottom:1px solid transparent;}
.cs-back:hover{border-bottom-color:currentColor;}
.cs-sky{display:none;}
.cs-rail{display:none;}
.cs-sun,.cs-moon{display:none;}
@media (min-width:900px){
  html.js-h #cs .cs-pin{height:100vh;}
  html.js-h #cs .cs-track{display:flex;height:100vh;}
  html.js-h #cs .cs-panel{width:100vw;height:100vh;min-height:0;flex:0 0 auto;padding:0 7vw;background:transparent;}
  html.js-h #cs .cs-sky{display:block;position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden;}
  html.js-h #cs .cs-grad{position:absolute;top:0;left:0;height:100%;display:flex;z-index:0;will-change:transform;}
  html.js-h #cs .cs-grad span{flex:0 0 100vw;height:100%;}
  html.js-h #cs .cs-track{position:relative;z-index:2;}
  html.js-h #cs .cs-sun{display:block;position:absolute;left:0;top:0;width:190px;z-index:1;will-change:transform;}
  html.js-h #cs .cs-moon{display:block;position:absolute;left:0;top:0;width:104px;z-index:1;
    transform:translate(70vw,120vh);filter:drop-shadow(0 0 24px rgba(244,233,210,.35));will-change:transform;}
  html.js-h #cs .cs-rail{display:block;position:absolute;left:0;right:0;bottom:0;height:3px;z-index:6;background:rgba(0,0,0,.18);}
  html.js-h #cs .cs-prog{height:100%;width:100%;background:#179c97;transform:scaleX(0);transform-origin:left center;}
}
@media (max-width:899px){
  .cs-gal{flex-direction:column;}
  .cs-shot{width:100%;aspect-ratio:16/10;}
  .cs-list{columns:1;}
  .cs-panel{min-height:auto;padding:110px 24px 80px;}
  .cs-back{top:92px;left:24px;}
}
"""

CS_JS = """
/* ===== case study chapter ===== */
(function(){
  var cs = document.getElementById('cs');
  if (!cs || !window.gsap) return;
  gsap.registerPlugin(ScrollTrigger);
  var mm = gsap.matchMedia();

  mm.add('(min-width:900px) and (prefers-reduced-motion: no-preference)', function(){
    document.documentElement.classList.add('js-h');
    var track = cs.querySelector('.cs-track');
    var dist = function(){ return track.scrollWidth - window.innerWidth; };
    var tl = gsap.timeline({scrollTrigger:{
      trigger: cs, start:'top top', end:function(){ return '+=' + dist(); },
      scrub:1, pin:true, anticipatePin:1, invalidateOnRefresh:true,
      onUpdate:function(self){ gsap.set('#cs .cs-prog',{scaleX:self.progress}); }
    }});
    tl.to([track,'#cs .cs-grad'],{x:function(){ return -dist(); }, ease:'none', duration:4},0)
      .fromTo('#cs .cs-sun',{x:'14vw',y:'10vh',rotation:0},{x:'60vw',y:'74vh',rotation:150,ease:'none',duration:2.7},0)
      .to('#cs .cs-sun',{autoAlpha:0,duration:.3},2.6)
      .fromTo('#cs .cs-moon',{x:'72vw',y:'120vh'},{x:'74vw',y:'12vh',ease:'power1.out',duration:1.1},2.8);
    gsap.utils.toArray(cs.querySelectorAll('[data-sp]')).forEach(function(el){
      var sp = parseFloat(el.getAttribute('data-sp')) || 1;
      var panel = el.closest('.cs-panel');
      var i = gsap.utils.toArray(cs.querySelectorAll('.cs-panel')).indexOf(panel);
      var n = cs.querySelectorAll('.cs-panel').length;
      var start = Math.max(0, (i - 1) * (4 / n)), dur = Math.min(4 - start, 2 * (4 / n) + .6);
      var d = 70 * (sp - 1) + 34 * sp;
      tl.fromTo(el, {x:d}, {x:-d, ease:'none', duration:dur}, start);
    });
    return function(){ document.documentElement.classList.remove('js-h'); };
  });

  mm.add('(max-width:899px), (prefers-reduced-motion: reduce)', function(){
    gsap.utils.toArray(cs.querySelectorAll('.cs-inner')).forEach(function(el){
      gsap.from(el, {y:46, autoAlpha:0, duration:.8, ease:'power3.out',
        scrollTrigger:{trigger:el, start:'top 88%'}});
    });
  });
})();
"""

# ---------------------------------------------------------------------------
# Send data in this shape and it drops straight in. Everything except
# slug/title/client/category/cover/summary/brief/approach is optional.
CASE_TEMPLATE = {
    "slug": "project-slug",
    "title": "Project Name",
    "client": "Client Name",
    "category": "Event Management",
    "year": "2026",
    "cover": "foc",                      # a file in img/work/ (no extension)
    "summary": "One or two sentences for the opening panel.",
    "brief_head": "What they needed",
    "brief": "A paragraph on the problem the client brought to you.",
    "approach_head": "How we made it",
    "approach": "A paragraph on scope, crew, timeline, anything notable.",
    "approach_points": ["Deliverable one", "Deliverable two"],
    "gallery": [],                        # ["img1","img2","img3"] from img/work/
    "video": "",                          # YouTube id
    "result_head": "What came of it",
    "results": [("450", "Attendees"), ("12", "Films delivered")],
    "result_text": "A paragraph on the outcome.",
    "quote": {"text": "Client quote.", "who": "Name", "role": "Title, Company"},
    "next": {"title": "Next Project", "href": "../other-slug/"},
}
