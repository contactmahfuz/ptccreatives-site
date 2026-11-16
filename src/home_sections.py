# Homepage redesign: index list, cinema expand, tilt cards, ghost ribbons,
# odometer stats, dial CTA, filmstrip rail.
import re

IX_ROWS = [
    ("01", "Video Production",  "Films, documentaries, podcasts & music videos, crafted in-house.", "img/sun.webp"),
    ("02", "Event Management and Coverage", "Concept to coverage, on the ground and on camera.",     "img/peacock.webp"),
    ("03", "Content Strategy",  "A roadmap for what to say, where, and how often.",                  "img/fish1.webp"),
    ("04", "Branding, Design &amp; Merchandising", "Identity, collateral and merchandise that carry the brand.", "img/lotus.webp"),
    ("05", "Social Media Management", "Calendars, captions and growth that compounds.",              "img/fish2.webp"),
    ("06", "Web Presence",      "Websites and landing pages built to convert.",                      "img/ribbon.webp"),
    ("07", "PR &amp; Activation", "Press, partnerships and live activations that get you noticed.",    "img/figure.webp"),
]
_rows = "".join(f"""      <a class="ix-row ptc-reveal" href="services.html" data-img="{img}">
        <span class="ix-num">{num}</span>
        <span class="ix-name">{name}</span>
        <span class="ix-desc">{desc}</span>
        <span class="ix-arrow">&rarr;</span>
      </a>\n""" for num, name, desc, img in IX_ROWS)

SEC_INDEX = f"""<section class="dots" id="services">
    <p class="ptc-eyeb ptc-reveal">Our Services</p>
    <h2 class="ptc-reveal">What We <em>Do</em></h2>
    <div class="ix">
{_rows}    </div>
    <div class="ix-float" aria-hidden="true"><img src="img/sun.webp" alt=""></div>
  </section>"""

_FF = "".join(f'<span class="ff" style="left:{l}%;top:{t}%;--d:{d}s;--dl:{dl}s;"></span>'
              for l, t, d, dl in [(8,22,3.1,0.4),(16,64,2.6,1.8),(28,30,3.8,0.9),(44,70,2.9,2.4),
                                  (58,18,3.4,1.1),(72,58,2.7,0.2),(86,32,3.6,2.0),(93,66,3.0,1.4)])

SEC_DIAL = f"""<section class="cta dots" id="start">
    {_FF}
    <p class="ptc-eyeb ptc-reveal">No Strings Attached</p>
    <h2 class="ptc-reveal">Let's create something<br>that <em>matters.</em></h2>
    <p class="lead ptc-reveal" style="margin:0 auto;">Schedule a free strategy call and tell us what you're trying to say.</p>
    <a class="dial ptc-reveal" href="contact.html" aria-label="Start your story, contact us">
      <svg class="dial-ring" viewBox="0 0 200 200" aria-hidden="true">
        <defs><path id="dialpath" d="M100,100 m-80,0 a80,80 0 1,1 160,0 a80,80 0 1,1 -160,0"/></defs>
        <text textLength="500" lengthAdjust="spacingAndGlyphs"><textPath href="#dialpath">START YOUR STORY &#183; START YOUR STORY &#183; START YOUR STORY &#183;</textPath></text>
      </svg>
      <span class="dial-core">&rarr;</span>
    </a>
  </section>"""

def _ghost(text, rev=False):
    t = (text + " &#183; ") * 8
    return f'<div class="ghost{" ghost-r" if rev else ""}" aria-hidden="true"><span>{t}</span></div>\n  '

RAIL = """
  <nav class="rail" aria-label="Page sections">
    <a class="rail-f" href="#ptc-hero" title="Intro"></a>
    <a class="rail-f" href="#pata" title="Our Story"></a>
    <a class="rail-f" href="#services" title="Services"></a>
    <a class="rail-f" href="#featured" title="Showreel"></a>
    <a class="rail-f" href="#work" title="Selected Work"></a>
    <a class="rail-f" href="#stats" title="The Numbers"></a>
    <a class="rail-f" href="#start" title="Start Your Story"></a>
  </nav>
"""

def apply_home(s):
    """Transform the homepage sections copy."""
    s = re.sub(r'<section class="dots" id="services">.*?</section>', SEC_INDEX, s, flags=re.S)
    s = s.replace('<section class="alt">\n    <div class="stat-grid">',
                  '<section class="alt" id="stats">\n    <div class="stat-grid">')
    s = re.sub(r'<section class="cta dots">.*?</section>', SEC_DIAL, s, flags=re.S)
    s = s.replace('<section class="dots" id="services">', _ghost("WHAT WE DO") + '<section class="dots" id="services">')
    s = s.replace('<section class="dots" id="featured">', _ghost("SHOWREEL", True) + '<section class="dots" id="featured">')
    s = s.replace('<section class="alt" id="work">', _ghost("SELECTED WORK") + '<section class="alt" id="work">')
    s = s.replace('<section class="alt" id="stats">', _ghost("THE NUMBERS", True) + '<section class="alt" id="stats">')
    return s

HOME_CSS = """
/* ===== services index list ===== */
#ptc-main .ix{margin-top:46px;border-top:1px solid rgba(255,255,255,.12);}
#ptc-main .ix-row{position:relative;display:grid;grid-template-columns:64px 1fr auto 40px;align-items:center;gap:26px;padding:26px 8px;border-bottom:1px solid rgba(255,255,255,.12);text-decoration:none;transition:padding .35s,background .35s;}
#ptc-main .ix-num{font-weight:300;font-size:13px;letter-spacing:.3em;color:#e8a317;}
#ptc-main .ix-name{font-weight:600;font-size:clamp(30px,4.4vw,64px);line-height:1.02;color:transparent;-webkit-text-stroke:1.2px rgba(255,255,255,.72);transition:color .35s;white-space:nowrap;}
#ptc-main .ix-row:hover .ix-name{color:#fff;-webkit-text-stroke-color:transparent;}
#ptc-main .ix-row:hover{padding-left:22px;background:rgba(23,156,151,.06);}
#ptc-main .ix-desc{font-weight:300;font-size:15px;line-height:1.6;color:rgba(255,255,255,.7);max-width:300px;text-align:right;opacity:0;transform:translateX(16px);transition:opacity .35s,transform .35s;}
#ptc-main .ix-row:hover .ix-desc{opacity:1;transform:none;}
#ptc-main .ix-arrow{color:#179c97;font-size:24px;opacity:.45;transition:transform .3s,opacity .3s;}
#ptc-main .ix-row:hover .ix-arrow{transform:translateX(7px);opacity:1;}
.ix-float{position:fixed;left:0;top:0;z-index:120;width:150px;pointer-events:none;opacity:0;will-change:transform;}
.ix-float img{width:100%;height:auto;display:block;filter:drop-shadow(0 16px 32px rgba(0,0,0,.5));}
@media (max-width:700px){
  #ptc-main .ix-row{grid-template-columns:40px 1fr 26px;gap:14px;}
  #ptc-main .ix-name{white-space:normal;font-size:26px;-webkit-text-stroke-width:1px;}
  #ptc-main .ix-desc{display:none;}
}
/* ===== ghost type ribbons ===== */
.ghost{overflow:hidden;padding:40px 0 6px;}
.ghost span{display:inline-block;white-space:nowrap;font-family:'Poppins',sans-serif;font-weight:600;font-size:clamp(56px,9vw,150px);line-height:1;color:transparent;-webkit-text-stroke:1.5px rgba(244,233,210,.16);will-change:transform;}
/* ===== work cards: lens sweep (tilt is JS) ===== */
#ptc-main .card{position:relative;overflow:hidden;}
#ptc-main .card::after{content:'';position:absolute;inset:0;z-index:4;pointer-events:none;background:linear-gradient(115deg,transparent 30%,rgba(23,156,151,.22) 48%,rgba(244,233,210,.12) 52%,transparent 70%);transform:translateX(-130%);transition:transform .8s ease;}
#ptc-main .card:hover::after{transform:translateX(130%);}
/* ===== odometer stats in sprocket frames ===== */
#ptc-main .stat{position:relative;background:#15292a;padding:40px 30px 34px;border-radius:4px;overflow:hidden;}
#ptc-main .stat::before,#ptc-main .stat::after{content:'';position:absolute;top:8px;bottom:8px;width:10px;border-radius:2px;background:repeating-linear-gradient(180deg,transparent 0 9px,rgba(10,20,20,.95) 9px 17px);}
#ptc-main .stat::before{left:8px;}
#ptc-main .stat::after{right:8px;}
#ptc-main .odo{display:inline-flex!important;overflow:hidden;font-size:inherit!important;letter-spacing:normal!important;text-transform:none!important;margin:0!important;}
#ptc-main .odo .od,#ptc-main .odo .od-s{font-size:inherit!important;letter-spacing:normal!important;text-transform:none!important;margin:0!important;color:inherit!important;}
#ptc-main .od{display:inline-block;height:1em;overflow:hidden;}
#ptc-main .od-s{display:block;will-change:transform;}
#ptc-main .od-s i{display:block;font-style:normal;height:1em;line-height:1;}
/* ===== dial CTA ===== */
#ptc-main .dial{position:relative;display:flex;align-items:center;justify-content:center;width:256px;height:256px;margin:52px auto 0;border-radius:50%;text-decoration:none;}
#ptc-main .dial-ring{position:absolute;inset:0;animation:dialspin 36s linear infinite;}
#ptc-main .dial-ring text{fill:rgba(255,255,255,.8);font-family:'Poppins',sans-serif;font-weight:300;font-size:12px;letter-spacing:.3em;}
#ptc-main .dial::before{content:'';position:absolute;inset:30px;border:1px solid rgba(23,156,151,.4);border-radius:50%;transition:inset .35s,border-color .35s;}
#ptc-main .dial:hover::before{inset:24px;border-color:rgba(23,156,151,.8);}
#ptc-main .dial-core{display:flex;align-items:center;justify-content:center;width:98px;height:98px;border-radius:50%;background:#179c97;color:#0a1414;font-size:32px;transition:transform .35s,background .35s;}
#ptc-main .dial:hover .dial-core{transform:scale(1.14);background:#e8a317;}
@keyframes dialspin{to{transform:rotate(360deg)}}
@media (max-width:700px){#ptc-main .dial{width:200px;height:200px;}#ptc-main .dial-core{width:78px;height:78px;font-size:26px;}}
@media (prefers-reduced-motion:reduce){#ptc-main .dial-ring{animation:none;}}
/* ===== filmstrip progress rail ===== */
.rail{position:fixed;right:16px;top:50%;transform:translateY(-50%);z-index:150;display:flex;flex-direction:column;gap:10px;}
.rail-f{position:relative;display:block;width:21px;height:15px;border:1px solid rgba(244,233,210,.35);border-radius:3px;background:rgba(10,20,20,.45);transition:background .3s,border-color .3s;}
.rail-f::before,.rail-f::after{content:'';position:absolute;top:2px;bottom:2px;width:2px;background:repeating-linear-gradient(180deg,rgba(244,233,210,.4) 0 2px,transparent 2px 4px);}
.rail-f::before{left:2px;}
.rail-f::after{right:2px;}
.rail-f.on{background:#179c97;border-color:#179c97;}
.rail-f:hover{border-color:#e8a317;}
@media (max-width:1100px){.rail{display:none;}}
/* ===== selected work: photo cover cards ===== */
#ptc-main .work-grid{grid-template-columns:1fr 1fr;gap:30px;}
#ptc-main .work-grid .card:nth-child(even){margin-top:70px;}
#ptc-main .card-top{height:auto;aspect-ratio:16/9;padding:0;display:block;background:#0e1c1c;overflow:hidden;}
#ptc-main .card-top img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  transition:transform .7s cubic-bezier(.2,.8,.3,1),filter .5s;filter:saturate(.92) brightness(.9);}
#ptc-main .card:hover .card-top img{transform:scale(1.07);filter:none;}
#ptc-main .card-top::before{content:'';position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(to top,rgba(10,20,20,.85),rgba(10,20,20,.15) 55%,rgba(10,20,20,.45));}
#ptc-main .card-n{position:absolute;right:18px;bottom:8px;z-index:2;font-weight:600;font-size:78px;
  line-height:.8;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.5);}
#ptc-main .card h3{font-size:21px;}
#ptc-main .card-go{display:inline-block;margin-top:16px;font-size:11.5px;font-weight:400;letter-spacing:.24em;text-transform:uppercase;color:#179c97;opacity:0;transform:translateX(-10px);transition:opacity .35s,transform .35s;}
#ptc-main .card:hover .card-go{opacity:1;transform:none;}
@media (max-width:620px){
  /* two cards per row leaves little width: shrink the counter so three digits
     and the sup sit between the sprocket strips instead of running over them */
  #ptc-main .stat{padding:30px 22px 26px;}
  #ptc-main .stat::before{left:6px;}
  #ptc-main .stat::after{right:6px;}
  #ptc-main .stat b{font-size:clamp(30px,11vw,50px);white-space:nowrap;}
  #ptc-main .stat b sup{font-size:.48em;}
  #ptc-main .stat > span{margin-top:10px;font-size:13px;letter-spacing:.12em;}
}
@media (max-width:900px){#ptc-main .work-grid{grid-template-columns:1fr;}#ptc-main .work-grid .card:nth-child(even){margin-top:0;}#ptc-main .card-n{font-size:70px;}}
"""

HOME_JS = """
/* services index list: floating motif preview chases the cursor */
(function(){
  if(!window.gsap) return;
  if(!window.matchMedia('(pointer: fine)').matches) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var fl=document.querySelector('.ix-float');
  var ix=document.querySelector('#services .ix');
  if(!fl||!ix) return;
  var img=fl.querySelector('img');
  var qx=gsap.quickTo(fl,'x',{duration:.45,ease:'power3'}), qy=gsap.quickTo(fl,'y',{duration:.45,ease:'power3'});
  var qr=gsap.quickTo(fl,'rotation',{duration:.6,ease:'power2'});
  var lastX=0;
  ix.addEventListener('mousemove',function(e){
    qx(e.clientX+28); qy(e.clientY-70); qr(gsap.utils.clamp(-14,14,(e.clientX-lastX)*.8)); lastX=e.clientX;
  });
  ix.querySelectorAll('.ix-row').forEach(function(row){
    row.addEventListener('mouseenter',function(){
      var s=row.getAttribute('data-img');
      if(s && img.getAttribute('src')!==s) img.setAttribute('src',s);
      gsap.to(fl,{opacity:1,scale:1,duration:.3,overwrite:'auto'});
    });
  });
  ix.addEventListener('mouseleave',function(){ gsap.to(fl,{opacity:0,scale:.8,duration:.25,overwrite:'auto'}); });
})();
/* featured film: cinema expand on scroll */
(function(){
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var film=document.querySelector('#featured .film');
  var frame=film && film.querySelector('.film-frame');
  if(!film) return;
  gsap.registerPlugin(ScrollTrigger);
  var tl=gsap.timeline({scrollTrigger:{trigger:'#featured',start:'top 70%',end:'bottom 10%',scrub:1,invalidateOnRefresh:true}});
  tl.fromTo(film,{scale:.74},{scale:function(){return Math.min(window.innerWidth/Math.max(film.offsetWidth,1),1.6);},duration:1,ease:'none'})
    .to(film,{scale:.9,duration:.7,ease:'none'},1.7);
  if(frame) tl.fromTo(frame,{borderRadius:10},{borderRadius:0,duration:1,ease:'none'},0).to(frame,{borderRadius:8,duration:.7,ease:'none'},1.7);
})();
/* work cards: 3D tilt with floating motif layer */
(function(){
  if(!window.gsap) return;
  if(!window.matchMedia('(pointer: fine)').matches) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('#ptc-main .card').forEach(function(card){
    gsap.set(card,{transformPerspective:900,transformStyle:'preserve-3d'});
    var rx=gsap.quickTo(card,'rotationX',{duration:.5,ease:'power2'});
    var ry=gsap.quickTo(card,'rotationY',{duration:.5,ease:'power2'});
    card.addEventListener('mousemove',function(e){
      var b=card.getBoundingClientRect();
      ry(((e.clientX-b.left)/b.width-.5)*10);
      rx(-((e.clientY-b.top)/b.height-.5)*10);
    });
    card.addEventListener('mouseleave',function(){ rx(0); ry(0); });
  });
})();
/* ghost ribbons drift against the scroll */
(function(){
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  gsap.utils.toArray('.ghost').forEach(function(g){
    var rev=g.classList.contains('ghost-r'), s=g.querySelector('span');
    gsap.fromTo(s,{x:rev?-420:60},{x:rev?60:-420,ease:'none',
      scrollTrigger:{trigger:g,start:'top bottom',end:'bottom top',scrub:1}});
  });
})();
/* selected work: show a random few of the projects, fresh on every visit.
   Every project stays in the markup; the case studies page shows them all. */
(function(){
  var grid=document.querySelector('.work-grid[data-rotate]');
  if(!grid) return;
  var cards=[].slice.call(grid.children);
  if(cards.length<2) return;
  var wide=parseInt(grid.getAttribute('data-rotate'),10)||6;
  var narrow=parseInt(grid.getAttribute('data-rotate-mobile'),10)||3;
  var mq=window.matchMedia('(max-width:900px)');
  function draw(){
    var n=Math.min(mq.matches?narrow:wide,cards.length);
    var bag=cards.slice();
    for(var i=bag.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=bag[i];bag[i]=bag[j];bag[j]=t;}
    var keep=bag.slice(0,n);
    cards.forEach(function(c){c.style.display='none';});
    var shown=0;
    cards.forEach(function(c){
      if(keep.indexOf(c)<0) return;
      c.style.display='';
      /* the staggered column needs the visible position, not the DOM one */
      c.style.marginTop=(!mq.matches && shown%2===1)?'70px':'0px';
      var num=c.querySelector('.card-n');
      if(num) num.textContent=('0'+(shown+1)).slice(-2);
      shown++;
    });
  }
  draw();
  if(mq.addEventListener) mq.addEventListener('change',draw);
  else if(mq.addListener) mq.addListener(draw);
})();

/* stats: film-counter odometer (IntersectionObserver — no ScrollTrigger dependency) */
(function(){
  var nums=document.querySelectorAll('.ptc-num');
  if(!nums.length) return;
  var col='<i>0</i><i>1</i><i>2</i><i>3</i><i>4</i><i>5</i><i>6</i><i>7</i><i>8</i><i>9</i>';
  var items=[];
  nums.forEach(function(el){
    var digits=String(el.getAttribute('data-count')||el.textContent).replace(/\\D/g,'').split('');
    if(!digits.length) return;
    el.classList.add('odo');
    el.innerHTML=digits.map(function(){return '<span class="od"><span class="od-s">'+col+'</span></span>';}).join('');
    var strips=el.querySelectorAll('.od-s');
    /* resting state = the correct number. One system owns the transform: gsap if present,
       plain CSS otherwise — never both, or the two offsets compose and show wrong digits. */
    strips.forEach(function(st,i){
      var d=(+digits[i])*10;
      if(window.gsap){ gsap.set(st,{yPercent:-d}); }
      else { st.style.transform='translateY(-'+d+'%)'; }
    });
    items.push({el:el,strips:strips,digits:digits});
  });
  if(!('IntersectionObserver' in window)) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting) return;
      io.unobserve(en.target);
      items.forEach(function(it){
        if(it.el!==en.target) return;
        it.strips.forEach(function(st,i){
          var d=(+it.digits[i])*10;
          if(window.gsap){ gsap.fromTo(st,{yPercent:0},{yPercent:-d,duration:1.6+i*.25,ease:'power4.out'}); }
        });
      });
    });
  },{threshold:.4});
  items.forEach(function(it){ io.observe(it.el); });
})();
/* filmstrip progress rail */
(function(){
  var rail=document.querySelector('.rail');
  if(!rail||!window.gsap) return;
  gsap.registerPlugin(ScrollTrigger);
  rail.querySelectorAll('a').forEach(function(a){
    var t=document.querySelector(a.getAttribute('href'));
    if(!t){ a.style.display='none'; return; }
    ScrollTrigger.create({trigger:t,start:'top center',end:'bottom center',
      onToggle:function(self){ a.classList.toggle('on',self.isActive); }});
    a.addEventListener('click',function(e){
      if(window.__lenis){ e.preventDefault(); window.__lenis.scrollTo(t,{offset:-60}); }
    });
  });
})();
"""
