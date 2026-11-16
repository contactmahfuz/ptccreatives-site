# The Unrolling Scroll chapter + redesign systems (grain, loader, cursor, lenis).
import random
random.seed(7)

def _fireflies(n):
    out = ""
    for _ in range(n):
        out += (f'<span class="ff" style="left:{random.randint(6,92)}%;top:{random.randint(12,78)}%;'
                f'--d:{random.uniform(2.2,4.4):.1f}s;--dl:{random.uniform(0,3.5):.1f}s;"></span>')
    return out

# ---- hand-drawn line motifs that paint themselves in (stroke draw) ----
SVG_LOTUS = """<svg class="dr dr-lotus" viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true">
<path pathLength="1" d="M100 172 C 96 134, 96 112, 100 82"/>
<path pathLength="1" d="M100 82 C 82 62, 80 40, 97 20 C 113 40, 113 63, 100 82"/>
<path pathLength="1" d="M97 84 C 74 74, 60 56, 58 32 C 80 40, 94 60, 100 82"/>
<path pathLength="1" d="M103 84 C 126 74, 140 56, 142 32 C 120 40, 106 60, 100 82"/>
<path pathLength="1" d="M95 86 C 66 86, 44 72, 34 52 C 60 50, 86 66, 98 84"/>
<path pathLength="1" d="M105 86 C 134 86, 156 72, 166 52 C 140 50, 114 66, 102 84"/>
<path pathLength="1" d="M58 152 C 80 142, 120 142, 142 152"/>
<path pathLength="1" d="M46 166 C 76 154, 124 154, 154 166"/>
</svg>"""

SVG_FISH = """<svg class="dr dr-fish" viewBox="0 0 250 120" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true">
<path pathLength="1" d="M28 60 C 66 22, 150 20, 192 56 C 152 94, 68 96, 28 60 C 36 60, 44 60, 50 60"/>
<path pathLength="1" d="M192 56 C 206 44, 216 34, 226 28 C 221 46, 221 68, 226 88 C 215 80, 204 68, 192 58"/>
<circle pathLength="1" cx="62" cy="50" r="5"/>
<path pathLength="1" d="M96 32 C 106 50, 106 70, 96 88"/>
<path pathLength="1" d="M124 28 C 134 50, 134 72, 124 92"/>
<path pathLength="1" d="M152 32 C 160 50, 160 68, 152 86"/>
</svg>"""

SVG_FEATHER = """<svg class="dr dr-feather" viewBox="0 0 160 230" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true">
<path pathLength="1" d="M82 224 C 72 164, 72 100, 80 44"/>
<ellipse pathLength="1" cx="80" cy="42" rx="30" ry="38"/>
<ellipse pathLength="1" cx="80" cy="46" rx="17" ry="22"/>
<circle pathLength="1" cx="80" cy="48" r="7"/>
<path pathLength="1" d="M70 120 C 50 112, 36 98, 30 80"/>
<path pathLength="1" d="M90 120 C 110 112, 124 98, 130 80"/>
<path pathLength="1" d="M72 160 C 56 154, 44 144, 38 130"/>
<path pathLength="1" d="M88 160 C 104 154, 116 144, 122 130"/>
</svg>"""

TICKER = ("FILMS &#183; PODCASTS &#183; CAMPAIGNS &#183; DESIGN &#183; EVENTS &#183; DOCUMENTARIES &#183; " * 4)

SEC_PATA = f"""
  <!-- ===== THE UNROLLING SCROLL (day -> night) ===== -->
  <section id="pata" class="ps" aria-label="Our story">
    <div class="ps-pin">
      <div class="ps-sky" aria-hidden="true">
        <div class="ps-grad"><span></span><span></span><span></span><span></span><span></span></div>
        <img class="ps-sun" src="img/sun.webp" alt="">
        <svg class="ps-moon" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="44" fill="#f4e9d2"/><circle cx="46" cy="48" r="7" fill="#d9cbae"/><circle cx="72" cy="70" r="5" fill="#d9cbae"/><circle cx="62" cy="38" r="4" fill="#d9cbae"/></svg>
      </div>
      <div class="ps-track">

        <article class="ps-panel ps-p1 ps-ink">
          <div class="ps-inner relative">
            <p class="ps-eyeb ptc-reveal">A Story, Unrolled</p>
            <h2 class="kin" data-sp="1">EVERY BRAND</h2>
            <h2 class="kin kin-o" data-sp="1.6">HAS A STORY.</h2>
            <p class="ps-copy" data-sp="0.6">For centuries, Bengal's patuas sang their stories from painted scrolls.<br>We tell yours on screens.</p>
          </div>
          <div class="ps-art pointer-events-none select-none">{SVG_LOTUS}</div>
        </article>

        <article class="ps-panel ps-p2 ps-ink">
          <div class="ps-inner relative">
            <p class="ps-eyeb">01 &#183; Listen</p>
            <h2 class="kin" data-sp="1.5">WE LISTEN</h2>
            <h2 class="kin kin-o kin-s" data-sp="2">KNOW · UNDERSTAND · VERIFY</h2>
            <p class="ps-copy" data-sp="0.6">Your business, your audience, your market,<br>tested before a single frame rolls.</p>
          </div>
          <div class="ps-art pointer-events-none select-none">{SVG_FISH}</div>
        </article>

        <article class="ps-panel ps-p3 ps-cream">
          <div class="ps-inner relative">
            <p class="ps-eyeb">02 &#183; Craft</p>
            <h2 class="kin" data-sp="1.5">WE CREATE</h2>
            <h2 class="kin kin-o kin-s" data-sp="2">FILM · DESIGN · BUILD</h2>
            <p class="ps-copy" data-sp="0.6">Films and podcasts, brands and campaigns,<br>events and websites.<br>The craft happens here.</p>
          </div>
        </article>

        <article class="ps-panel ps-p4 ps-cream">
          {_fireflies(10)}
          <div class="ps-inner relative">
            <p class="ps-eyeb">03 &#183; Grow</p>
            <h2 class="kin" data-sp="1.5">WE GROW</h2>
            <h2 class="kin kin-o kin-s" data-sp="2">MEASURE · REFINE · SCALE</h2>
            <p class="ps-copy" data-sp="0.6">Work that travels and keeps working<br>long after launch day.</p>
          </div>
          <div class="ps-art pointer-events-none select-none">{SVG_FEATHER}</div>
        </article>

        <article class="ps-panel ps-p5 ps-cream">
          {_fireflies(8)}
          <div class="ps-inner ps-center relative mx-auto text-center">
            <p class="ps-eyeb">PTC Creatives</p>
            <h2 class="kin kin-big" data-sp="1.2">INSPIRING<br>CREATIVE<br><span class="kin-o">BRILLIANCE.</span></h2>
            <a class="ptc-btn" data-mag href="contact.html">Start Your Story</a>
          </div>
        </article>

      </div>
      <div class="ps-rail" aria-hidden="true"><div class="ps-tick"><span>{TICKER}</span><span>{TICKER}</span></div></div>
    </div>
  </section>
"""

PRELUDE_HTML = """<div id="ldr" aria-hidden="true"><img src="img/sun.webp" alt=""></div>
<script>(function(){var l=document.getElementById('ldr');var rm=false;
try{rm=!!sessionStorage.getItem('ptcld')}catch(e){}
if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)rm=true;
if(rm&&l&&l.parentNode){l.parentNode.removeChild(l);return}
setTimeout(function(){if(l&&l.parentNode){l.style.transition='opacity .5s';l.style.opacity='0';
setTimeout(function(){l.parentNode&&l.parentNode.removeChild(l)},550)}},2400);})();</script>
<div class="grain" aria-hidden="true"></div>
<div class="vig" aria-hidden="true"></div>
<div id="curd" aria-hidden="true"></div><div id="curr" aria-hidden="true"></div>
"""

LENIS_TAG = '<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.4/dist/lenis.min.js"></script>\n'

PATA_CSS = """
/* ============ film grain (heavy) + vignette ============ */
.grain{position:fixed;inset:-100%;z-index:200;pointer-events:none;opacity:.16;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' values='0.33 0.33 0.33 0 0 0.33 0.33 0.33 0 0 0.33 0.33 0.33 0 0 0 0 0 1 0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:300px 300px;animation:grainShift .8s steps(8) infinite;}
@keyframes grainShift{0%{transform:translate(0,0)}12.5%{transform:translate(-4%,3%)}25%{transform:translate(3%,-5%)}37.5%{transform:translate(-5%,-2%)}50%{transform:translate(5%,4%)}62.5%{transform:translate(-2%,6%)}75%{transform:translate(6%,-3%)}87.5%{transform:translate(-6%,-6%)}100%{transform:translate(0,0)}}
.vig{position:fixed;inset:0;z-index:199;pointer-events:none;background:radial-gradient(ellipse at 50% 46%,transparent 58%,rgba(5,10,10,.42) 100%);}
@media (max-width:900px){.grain{opacity:.11;}}
@media (prefers-reduced-motion:reduce){.grain{animation:none;}}

/* ============ iris preloader ============ */
#ldr{position:fixed;inset:0;z-index:999;background:#0a1414;display:flex;align-items:center;justify-content:center;}
#ldr img{width:150px;height:auto;opacity:.95;}

/* ============ custom cursor ============ */
#curd,#curr{position:fixed;left:0;top:0;z-index:400;pointer-events:none;border-radius:50%;display:none;mix-blend-mode:difference;}
#curd{width:8px;height:8px;background:#f4e9d2;margin:-4px 0 0 -4px;}
#curr{width:34px;height:34px;border:1.5px solid rgba(244,233,210,.65);margin:-17px 0 0 -17px;transition:transform .25s ease,opacity .25s;}
html.ptc-cur, html.ptc-cur *{cursor:none!important;}
html.ptc-cur #curd,html.ptc-cur #curr{display:block;}

/* ============ the unrolling scroll ============ */
.ps{position:relative;}
#ptc-main .ps{padding:0;}
.ps-pin{position:relative;overflow:hidden;}
.ps-track{display:block;}
.ps-panel{position:relative;min-height:92vh;display:flex;align-items:center;overflow:hidden;padding:80px 7vw;}
.ps-inner{position:relative;z-index:3;max-width:1100px;}
.ps-center{text-align:center;margin:0 auto;}
.ps-eyeb{font-size:13px;font-weight:400;letter-spacing:.42em;text-transform:uppercase;color:#179c97;margin:0 0 22px;}
.kin{font-family:'Poppins',sans-serif;font-weight:600;line-height:.95;letter-spacing:-.015em;margin:0 0 10px;font-size:clamp(64px,11vw,176px);white-space:nowrap;}
.kin-o{color:transparent!important;-webkit-text-stroke:1.5px #f4e9d2;}
.ps-ink .kin-o{-webkit-text-stroke-color:#241e16;}
.kin-s{font-size:clamp(26px,3.2vw,52px);letter-spacing:.12em;}
.kin-big{font-size:clamp(56px,9vw,152px);white-space:normal;line-height:1.02;}
.ps-copy{font-weight:300;font-size:clamp(17px,1.5vw,23px);line-height:1.8;margin:28px 0 0;opacity:.92;}
.ps-ink{color:#241e16;}
.ps-ink .ps-eyeb{color:#a8431f;}
.ps-cream{color:#f4e9d2;}
.ps-art{position:absolute;right:8vw;top:50%;transform:translateY(-50%);z-index:2;opacity:.9;}
.dr{width:min(24vw,300px);height:auto;}
.dr path,.dr circle,.dr ellipse{stroke-dasharray:1 1;stroke-dashoffset:1;}
/* day->night: horizontal gradients blend panel to panel on desktop; vertical when stacked */
.ps-p1{background:linear-gradient(180deg,#f4e9d2 70%,#eed8ac 100%);}
.ps-p2{background:linear-gradient(180deg,#eed8ac 0%,#d99a4e 80%,#c0693a 100%);}
.ps-p3{background:linear-gradient(180deg,#c0693a 0%,#7e3528 60%,#38222e 100%);}
.ps-p4{background:linear-gradient(180deg,#38222e 0%,#122028 70%,#0d1a20 100%);}
.ps-p5{background:linear-gradient(180deg,#0d1a20 0%,#0a1414 100%);}
.ps-sky{display:none;}
.ps-rail{display:none;}
/* fireflies */
.ff{position:absolute;width:5px;height:5px;border-radius:50%;background:#e8a317;z-index:2;opacity:0;
  box-shadow:0 0 12px 3px rgba(232,163,23,.75);animation:ffl var(--d,3s) ease-in-out var(--dl,0s) infinite alternate;}
@keyframes ffl{0%{opacity:0;transform:translateY(0)}55%{opacity:.95}100%{opacity:.1;transform:translateY(-28px)}}
@media (prefers-reduced-motion:reduce){.ff{animation:none;opacity:.6;}}
/* desktop horizontal mode (activated by JS via html.js-h) */
@media (min-width:900px){
  html.js-h .ps-pin{height:100vh;}
  html.js-h .ps-track{display:flex;width:500vw;height:100vh;}
  html.js-h .ps-panel{width:100vw;height:100vh;min-height:0;flex:0 0 auto;padding:0 7vw;}
  /* sky holds the gradient strip + sun; the track rides above it so text is never covered */
  html.js-h .ps-panel{background:transparent;}
  html.js-h .ps-track{position:relative;z-index:2;}
  html.js-h .ps-sky{display:block;position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden;}
  html.js-h .ps-grad{position:absolute;top:0;left:0;height:100%;width:500vw;display:flex;z-index:0;will-change:transform;}
  html.js-h .ps-grad span{flex:0 0 100vw;height:100%;}
  html.js-h .ps-grad span:nth-child(1){background:linear-gradient(90deg,#f4e9d2 72%,#eed8ac 100%);}
  html.js-h .ps-grad span:nth-child(2){background:linear-gradient(90deg,#eed8ac 0%,#d99a4e 72%,#c0693a 100%);}
  html.js-h .ps-grad span:nth-child(3){background:linear-gradient(90deg,#c0693a 0%,#7e3528 55%,#38222e 100%);}
  html.js-h .ps-grad span:nth-child(4){background:linear-gradient(90deg,#38222e 0%,#122028 60%,#0d1a20 100%);}
  html.js-h .ps-grad span:nth-child(5){background:linear-gradient(90deg,#0d1a20 0%,#0a1414 100%);}
  html.js-h .ps-sun{position:absolute;left:0;top:0;width:200px;z-index:1;will-change:transform;}
  html.js-h .ps-moon{position:absolute;left:0;top:0;width:110px;z-index:1;transform:translate(70vw,120vh);
    filter:drop-shadow(0 0 26px rgba(244,233,210,.35));will-change:transform;}
  html.js-h .ps-rail{display:block;position:absolute;left:0;right:0;bottom:0;height:58px;z-index:4;
    border-top:1px solid rgba(244,233,210,.25);
    background-image:repeating-linear-gradient(90deg,transparent 0 16px,rgba(244,233,210,.22) 16px 30px);
    background-size:auto 10px;background-repeat:repeat-x;background-position:0 8px;}
  html.js-h .ps-tick{position:absolute;left:0;bottom:12px;display:flex;white-space:nowrap;
    mix-blend-mode:difference;color:#f4e9d2;will-change:transform;}
  html.js-h .ps-tick span{font-weight:300;font-size:15px;letter-spacing:.34em;padding-right:40px;}
}
@media (max-width:900px){
  .ps-art{position:relative;right:auto;top:auto;transform:none;margin-top:36px;}
  .kin{white-space:normal;}
}
"""

PATA_JS = """
/* ===== lenis smooth scrolling ===== */
(function(){
  if(!window.Lenis || !window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var lenis = new Lenis({duration:1.15, smoothWheel:true});
  window.__lenis = lenis;
  lenis.on('scroll', function(){ if(window.ScrollTrigger) ScrollTrigger.update(); });
  gsap.ticker.add(function(t){ lenis.raf(t*1000); });
  gsap.ticker.lagSmoothing(0);
})();
/* ===== iris preloader (enhanced open) ===== */
(function(){
  var l=document.getElementById('ldr');
  if(!l) return;
  if(!window.gsap){ return; } /* inline fallback timer will clear it */
  var img=l.querySelector('img'), o={r:0};
  gsap.timeline()
    .fromTo(img,{scale:.55,rotation:-60,autoAlpha:0},{scale:1,rotation:0,autoAlpha:1,duration:.7,ease:'power3.out'})
    .to(img,{rotation:90,scale:.9,duration:.45,ease:'power2.in'})
    .to(o,{r:160,duration:.9,ease:'power2.inOut',onUpdate:function(){
        var m='radial-gradient(circle '+o.r+'vmax at 50% 50%, transparent '+Math.max(0,o.r-2)+'vmax, #000 '+o.r+'vmax)';
        l.style.webkitMaskImage=m; l.style.maskImage=m;
      }},'-=.05')
    .call(function(){ if(l.parentNode) l.parentNode.removeChild(l);
      try{sessionStorage.setItem('ptcld','1')}catch(e){} });
})();
/* ===== custom cursor + magnetic ===== */
(function(){
  if(!window.gsap) return;
  if(!window.matchMedia('(pointer: fine)').matches) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('ptc-cur');
  var d=document.getElementById('curd'), r=document.getElementById('curr');
  var dx=gsap.quickTo(d,'x',{duration:.12,ease:'power2'}), dy=gsap.quickTo(d,'y',{duration:.12,ease:'power2'});
  var rx=gsap.quickTo(r,'x',{duration:.38,ease:'power2'}), ry=gsap.quickTo(r,'y',{duration:.38,ease:'power2'});
  window.addEventListener('mousemove',function(e){ dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY); });
  document.addEventListener('mouseover',function(e){
    var t=e.target.closest('a,button,[role="button"],input,textarea');
    r.style.transform=t?'scale(1.7)':'scale(1)';
  });
  /* magnetic pull on primary buttons */
  document.querySelectorAll('.ptc-cta,.ncta,.ptc-btn,[data-mag]').forEach(function(el){
    var qx=gsap.quickTo(el,'x',{duration:.3,ease:'power3'}), qy=gsap.quickTo(el,'y',{duration:.3,ease:'power3'});
    el.addEventListener('mousemove',function(e){
      var b=el.getBoundingClientRect();
      qx((e.clientX-(b.left+b.width/2))*.25); qy((e.clientY-(b.top+b.height/2))*.35);
    });
    el.addEventListener('mouseleave',function(){ qx(0); qy(0); });
  });
})();
/* ===== frame-cut flicker on section entry ===== */
(function(){
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  gsap.utils.toArray('#ptc-main > section:not(.ps), .ptc-footer').forEach(function(sec){
    ScrollTrigger.create({trigger:sec,start:'top 82%',once:true,onEnter:function(){
      gsap.fromTo(sec,{opacity:.35},{opacity:1,duration:.32,ease:'steps(4)'});
    }});
  });
})();
/* ===== living hero: velocity sun + cursor-aware motifs ===== */
(function(){
  if(!window.gsap) return;
  if(!window.matchMedia('(pointer: fine)').matches) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var hero=document.getElementById('ptc-hero');
  if(!hero) return;
  var sunW=hero.querySelector('.lyr-sun');
  if(sunW && window.__lenis){
    var rot=0, qr=gsap.quickTo(sunW,'rotation',{duration:.5,ease:'power2'});
    window.__lenis.on('scroll',function(e){ rot+=(e.velocity||0)*.05; rot=Math.max(-70,Math.min(70,rot)); qr(rot); });
    gsap.ticker.add(function(){ rot*= .94; qr(rot); });
  }
  var drift=[['.lyr-fish1',38,22],['.lyr-fish2',26,16],['.lyr-lotus',-16,-10],['.lyr-peacock',-22,-12]];
  var qs=drift.map(function(c){
    var el=hero.querySelector(c[0]); if(!el) return null;
    return {x:gsap.quickTo(el,'x',{duration:.8,ease:'power2'}), y:gsap.quickTo(el,'y',{duration:.8,ease:'power2'}), ax:c[1], ay:c[2]};
  });
  hero.addEventListener('mousemove',function(e){
    var b=hero.getBoundingClientRect();
    var nx=(e.clientX-b.left)/b.width-.5, ny=(e.clientY-b.top)/b.height-.5;
    qs.forEach(function(q){ if(q){ q.x(nx*q.ax); q.y(ny*q.ay); } });
  });
})();
/* ===== the unrolling scroll chapter ===== */
(function(){
  if(!window.gsap) return;
  var ps=document.getElementById('pata');
  if(!ps) return;
  gsap.registerPlugin(ScrollTrigger);
  var mm=gsap.matchMedia();

  mm.add('(min-width:900px) and (prefers-reduced-motion: no-preference)', function(){
    document.documentElement.classList.add('js-h');
    var track=ps.querySelector('.ps-track');
    var dist=function(){ return track.scrollWidth - window.innerWidth; };
    var tl=gsap.timeline({scrollTrigger:{
      trigger:ps, start:'top top', end:function(){ return '+=' + dist(); },
      scrub:1, pin:true, anticipatePin:1, invalidateOnRefresh:true,
      onUpdate:function(self){
        if (self.progress > 0.9 && window.ptcTrackOnce) window.ptcTrackOnce('story','StoryComplete',{},true);
      },
      snap:{snapTo:[0,.25,.5,.75,1], duration:{min:.2,max:.6}, ease:'power1.inOut'}
    }});
    tl.to([track,'.ps-grad'],{x:function(){ return -dist(); }, ease:'none', duration:4},0);
    /* sun sets across the day panels, moon rises over the night ones */
    tl.fromTo('.ps-sun',{x:'12vw',y:'8vh',rotation:0},{x:'58vw',y:'76vh',rotation:160,ease:'none',duration:2.6},0)
      .to('.ps-sun',{autoAlpha:0,duration:.3},2.5)
      .fromTo('.ps-moon',{x:'72vw',y:'120vh'},{x:'74vw',y:'10vh',ease:'power1.out',duration:1.1},2.7);
    /* ticker drifts against the direction of travel */
    tl.fromTo('.ps-tick',{xPercent:0},{xPercent:-50,ease:'none',duration:4},0);
    /* kinetic type: layers slide at their own speeds */
    gsap.utils.toArray(ps.querySelectorAll('[data-sp]')).forEach(function(el){
      var sp=parseFloat(el.getAttribute('data-sp'))||1;
      var panel=el.closest('.ps-panel');
      var i=gsap.utils.toArray(ps.querySelectorAll('.ps-panel')).indexOf(panel);
      var start=Math.max(0,i-1), dur=Math.min(2,4-start);
      var d=90*(sp-1)+40*sp;
      tl.fromTo(el,{x:d},{x:-d,ease:'none',duration:dur},start);
    });
    /* motifs paint themselves in as their panel arrives */
    [['.dr-lotus',.0,.9],['.dr-fish',.7,1.8],['.dr-feather',2.7,3.6]].forEach(function(c){
      var el=ps.querySelector(c[0]); if(!el) return;
      tl.to(el.querySelectorAll('path,circle,ellipse'),
        {strokeDashoffset:0, duration:c[2]-c[1], stagger:.08, ease:'none'}, c[1]);
    });
    return function(){ document.documentElement.classList.remove('js-h'); };
  });

  mm.add('(max-width:899px), (prefers-reduced-motion: reduce)', function(){
    /* stacked fallback: draw + reveal per panel on normal vertical scroll */
    gsap.utils.toArray(ps.querySelectorAll('.dr')).forEach(function(svg){
      gsap.to(svg.querySelectorAll('path,circle,ellipse'),
        {strokeDashoffset:0, duration:1.4, stagger:.1, ease:'power1.inOut',
         scrollTrigger:{trigger:svg, start:'top 85%'}});
    });
    gsap.utils.toArray(ps.querySelectorAll('.ps-inner')).forEach(function(el){
      gsap.from(el,{y:50,autoAlpha:0,duration:.8,ease:'power3.out',
        scrollTrigger:{trigger:el,start:'top 88%'}});
    });
  });
})();
"""

# ===== site-wide day->night theming for inner pages =====
PAGE_CSS = """
/* ===== day->night journey across inner pages ===== */
.pg-day{background:linear-gradient(180deg,#f4e9d2 0%,#eed8ac 100%);}
.pg-amber{background:linear-gradient(180deg,#eed8ac 0%,#d99a4e 82%,#c0693a 100%);}
.pg-dusk{background:linear-gradient(180deg,#c0693a 0%,#7e3528 55%,#38222e 100%);}
.pg-eve{background:linear-gradient(180deg,#38222e 0%,#122028 100%);}
.pg-night{background:linear-gradient(180deg,#122028 0%,#0a1414 100%);}
.pg-grad-serv{background:linear-gradient(180deg,#eed8ac 0%,#b0582f 38%,#2f2030 70%,#122028 100%);}
.pg-grad-case{background:linear-gradient(180deg,#eed8ac 0%,#b0582f 30%,#38222e 65%,#122028 100%);}
.pg-grad-contact{background:linear-gradient(180deg,#eed8ac 0%,#7e3528 34%,#16222a 68%,#0a1414 100%);}
/* ink text on daylight ground */
#ptc-main .pg-day,#ptc-main .pg-amber{color:#241e16;}
#ptc-main .pg-day h1,#ptc-main .pg-day h2,#ptc-main .pg-amber h2{color:#241e16;}
#ptc-main .pg-day .lead,#ptc-main .pg-amber .lead{color:rgba(36,30,22,.78);}
#ptc-main .pg-day .ptc-eyeb,#ptc-main .pg-amber .ptc-eyeb{color:#a8431f;}
#ptc-main .pg-day .ptc-btn,#ptc-main .pg-amber .ptc-btn{color:#241e16;}
#ptc-main .pg-day .ptc-btn:hover,#ptc-main .pg-amber .ptc-btn:hover{color:#f4e9d2;background:#179c97;}
/* services: the first two rows sit in daylight */
#ptc-main .pg-grad-serv .srow:nth-of-type(-n+2) h3{color:#241e16;}
#ptc-main .pg-grad-serv .srow:nth-of-type(-n+2) p{color:rgba(36,30,22,.78);}
#ptc-main .pg-grad-serv .srow:nth-of-type(-n+2) li{color:rgba(36,30,22,.6);}
#ptc-main .pg-grad-serv .srow:nth-of-type(-n+2){border-bottom-color:rgba(36,30,22,.2);}
/* kinetic band titles */
#ptc-main .band h1{font-size:clamp(50px,7.2vw,108px);line-height:1.02;letter-spacing:-.015em;}
#ptc-main .band h1 em{color:transparent;-webkit-text-stroke:1.8px #241e16;}
/* painted band motif */
.band-motif{position:absolute;left:4vw;bottom:-14px;z-index:1;opacity:.45;color:#241e16;pointer-events:none;}
.band-motif .dr{width:min(20vw,220px);height:auto;}
@media (max-width:700px){.band-motif{display:none;}#ptc-main .band h1{font-size:38px;}}
/* nav over daylight bands */
.ptc-nav .nlogo .lg-d{display:none!important;}
.ptc-nav.nav-day:not(.solid):not(.open) .nlogo .lg-l{display:none!important;}
.ptc-nav.nav-day:not(.solid):not(.open) .nlogo .lg-d{display:block!important;}
.ptc-nav.nav-day:not(.solid):not(.open) ul a{color:#241e16;}
.ptc-nav.nav-day:not(.solid):not(.open) ul a.on,.ptc-nav.nav-day:not(.solid):not(.open) ul a:hover{color:#a8431f;}
.ptc-nav.nav-day:not(.solid):not(.open) .nburger span{background:#241e16;}
/* reduced motion: show motifs fully painted */
@media (prefers-reduced-motion:reduce){.dr path,.dr circle,.dr ellipse{stroke-dashoffset:0;}}
"""

PAGE_JS = """
/* band motifs paint themselves in */
(function(){
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  gsap.utils.toArray('.dr-page').forEach(function(svg){
    gsap.to(svg.querySelectorAll('path,circle,ellipse'),{strokeDashoffset:0,duration:1.6,stagger:.09,ease:'power1.inOut',
      scrollTrigger:{trigger:svg,start:'top 92%'}});
  });
})();
"""
