/* PTC Creatives — main.js (generated) */

(function(){try{
  var hero=document.getElementById('ptc-hero');
  if(!hero) return;
  var stage=hero.querySelector('.ptc-stage');
  var wrap=hero.querySelector('.ptc-stage-wrap');

  function fit(){
    var w=hero.clientWidth,s,tx;
    if(w<900){ s=w/950; tx=-430*s; }      /* mobile: zoom into the artwork cluster */
    else     { s=w/1376; tx=0; }          /* desktop: full 16:9 canvas */
    stage.style.transform='translateX('+tx+'px) scale('+s+')';
    wrap.style.height=(768*s)+'px';
  }
  window.addEventListener('resize',fit); fit();

  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);

  /* ---- entrance: the scene assembles on load (after the iris preloader opens, on a first visit) ---- */
  gsap.timeline({delay:document.getElementById('ldr')?1.1:0,defaults:{ease:'power3.out'}})
    .from('#ptc-hero .ptc-arch',{y:140,autoAlpha:0,duration:.9,stagger:.14})
    .from('#ptc-hero .ptc-sun',{scale:.5,rotation:-45,autoAlpha:0,duration:1.1,ease:'back.out(1.4)'},'-=.55')
    .from('#ptc-hero .ptc-figure',{y:60,autoAlpha:0,duration:.9},'-=.65')
    .fromTo('#ptc-hero .ptc-ribbon',
      {clipPath:'inset(-5% 0% -5% 100%)'},
      {clipPath:'inset(-5% 0% -5% 0%)',duration:1.3,ease:'power2.inOut'},'-=.45')
    .from('#ptc-hero .ptc-motif',{scale:0,autoAlpha:0,duration:.55,ease:'back.out(2.2)',stagger:.13},'-=.5')
    .from('#ptc-hero .ptc-head-desktop > *, #ptc-hero .ptc-head-mobile > *',
      {y:28,autoAlpha:0,duration:.7,stagger:.09},'-=1.1');

  /* ---- scroll choreography ---- */
  function choreo(st,k){
    st.to('#ptc-hero .ptc-arch-teal',{y:-70*k},0)
      .to('#ptc-hero .ptc-arch-char',{y:-115*k},0)
      .to('#ptc-hero .ptc-arch-verm',{y:-45*k},0)
      .to('#ptc-hero .ptc-sun',{rotation:75,scale:1.07},0)
      .to('#ptc-hero .ptc-ribbon',{x:-55*k},0)
      .to('#ptc-hero .ptc-figure',{y:-30*k},0)
      .to('#ptc-hero .ptc-lotus',{y:-45*k,rotation:-6},0)
      .to('#ptc-hero .ptc-fish1',{x:-75*k},0)
      .to('#ptc-hero .ptc-fish2',{x:-50*k},0)
      .to('#ptc-hero .ptc-peacock',{y:-28*k},0)
      .to('#ptc-hero .ptc-border',{backgroundPositionX:'-=280px'},0)
      .to('#ptc-hero .ptc-cue',{autoAlpha:0,duration:.1},0);
  }
  var mm=gsap.matchMedia();
  mm.add('(min-width:700px)',function(){
    /* hero pins in place while the scene plays, then releases */
    choreo(gsap.timeline({scrollTrigger:{trigger:'#ptc-hero',start:'top top',end:'+=120%',scrub:1,pin:true,anticipatePin:1}}),1);
  });
  mm.add('(max-width:699px)',function(){
    /* lighter, unpinned parallax on phones: starts at 0% on load, plays as the hero scrolls away */
    choreo(gsap.timeline({scrollTrigger:{trigger:'#ptc-hero',start:'top top',end:'bottom top',scrub:1}}),.6);
  });
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();


(function(){try{
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  /* section reveals */
  gsap.utils.toArray('.ptc-reveal').forEach(function(el){
    gsap.from(el,{y:44,autoAlpha:0,duration:.85,ease:'power3.out',
      scrollTrigger:{trigger:el,start:'top 88%'}});
  });
  /* process rail fills as you scroll through the strip */
  if(document.querySelector('.ptc-proc-bar')) gsap.fromTo('.ptc-proc-bar',{scaleX:0},{scaleX:1,ease:'none',
    scrollTrigger:{trigger:'.ptc-process',start:'top 65%',end:'bottom 60%',scrub:1}});
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();


(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* homepage travelers: the hero's sun and fish journey through the sections */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();


/* ===== film grain: animated noise that lives on the backgrounds, under all content ===== */
(function(){
  var root = document.querySelector('.grain');
  if(!root) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var N = 256, cv = document.createElement('canvas'); cv.width = cv.height = N;
  var cx = cv.getContext('2d'); if(!cx) return;
  var im = cx.createImageData(N, N), d = im.data;
  for(var i=0; i<d.length; i+=4){ var v = (Math.random() + Math.random()) * 127.5; d[i] = d[i+1] = d[i+2] = v; d[i+3] = 255; }
  cx.putImageData(im, 0, 0);
  var url = 'url(' + cv.toDataURL('image/png') + ')';
  var layers = [], T = 0;
  function add(g, on){
    var inner = document.createElement('div'); inner.className = 'gr-i'; inner.style.backgroundImage = url;
    g.appendChild(inner); var L = {g:g, i:inner, on:on}; g.__gr = L; layers.push(L);
  }
  add(root, true);   // page base: shows wherever a section has no background of its own
  var HOSTS = '#ptc-main .alt,#ptc-main .pg-day,#ptc-main .pg-amber,#ptc-main .pg-dusk,#ptc-main .pg-eve,#ptc-main .pg-night,'
            + '#ptc-main [class*="pg-grad"],.ps-panel,.ps-sky,#cs .cs-panel,#cs .cs-sky,.ptc-footer';
  [].forEach.call(document.querySelectorAll(HOSTS), function(h){
    var g = document.createElement('div'); g.className = 'gr'; g.setAttribute('aria-hidden', 'true');
    h.classList.add('gr-host');
    if(getComputedStyle(h).position === 'static') h.classList.add('gr-pos');
    var grad = h.querySelector(':scope > .ps-grad, :scope > .cs-grad');   // skies: grain sits on the gradient, under the sun/moon
    if(grad) h.insertBefore(g, grad.nextSibling); else h.appendChild(g);
    add(g, false);
  });
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ e.target.__gr.on = e.isIntersecting; }); });
    layers.forEach(function(L){ if(L.g !== root) io.observe(L.g); });
  } else layers.forEach(function(L){ L.on = true; });
  function frame(all){
    for(var k=0; k<layers.length; k++){ var L = layers[k];
      if(all || L.on) L.i.style.transform = 'translate3d(' + ((Math.random() * T) | 0) + 'px,' + ((Math.random() * T) | 0) + 'px,0)'; }
  }
  function size(){
    T = Math.round(N * (window.innerWidth < 900 ? 1.15 : 1.2));   // grain size in CSS px
    layers.forEach(function(L){ var s = L.i.style; s.backgroundSize = T + 'px ' + T + 'px'; s.top = s.left = -T + 'px'; });
    frame(true);
  }
  var rz; window.addEventListener('resize', function(){ clearTimeout(rz); rz = setTimeout(size, 150); });
  size();
  if(reduce) return;
  var last = 0, step = 1000 / 24;
  (function tick(now){ if(now - last >= step){ last = now; frame(false); } requestAnimationFrame(tick); })(0);
})();

/* ===== lenis smooth scrolling ===== */
(function(){try{
  if(!window.Lenis || !window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var lenis = new Lenis({duration:1.15, smoothWheel:true});
  window.__lenis = lenis;
  lenis.on('scroll', function(){ if(window.ScrollTrigger) ScrollTrigger.update(); });
  gsap.ticker.add(function(t){ lenis.raf(t*1000); });
  gsap.ticker.lagSmoothing(0);
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* ===== iris preloader (enhanced open) ===== */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* ===== custom cursor + magnetic ===== */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* ===== frame-cut flicker on section entry ===== */
(function(){try{
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  gsap.utils.toArray('#ptc-main > section:not(.ps), .ptc-footer').forEach(function(sec){
    ScrollTrigger.create({trigger:sec,start:'top 82%',once:true,onEnter:function(){
      gsap.fromTo(sec,{opacity:.35},{opacity:1,duration:.32,ease:'steps(4)'});
    }});
  });
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* ===== living hero: velocity sun + cursor-aware motifs ===== */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* ===== the unrolling scroll chapter ===== */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();


/* band motifs paint themselves in */
(function(){try{
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  gsap.utils.toArray('.dr-page').forEach(function(svg){
    gsap.to(svg.querySelectorAll('path,circle,ellipse'),{strokeDashoffset:0,duration:1.6,stagger:.09,ease:'power1.inOut',
      scrollTrigger:{trigger:svg,start:'top 92%'}});
  });
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();


/* services index list: floating motif preview chases the cursor */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* featured film: cinema expand on scroll */
(function(){try{
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var film=document.querySelector('#featured .film');
  var frame=film && film.querySelector('.film-frame');
  if(!film) return;
  gsap.registerPlugin(ScrollTrigger);
  var tl=gsap.timeline({scrollTrigger:{trigger:'#featured',start:'top 70%',end:'bottom 10%',scrub:1,invalidateOnRefresh:true}});
  tl.fromTo(film,{scale:.74},{scale:function(){return Math.min(window.innerWidth/Math.max(film.offsetWidth,1),1.6);},duration:1,ease:'none'})
    .to(film,{scale:.9,duration:.7,ease:'none'},1.7);
  if(frame) tl.fromTo(frame,{borderRadius:10},{borderRadius:0,duration:1,ease:'none'},0).to(frame,{borderRadius:8,duration:.7,ease:'none'},1.7);
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* work cards: 3D tilt with floating motif layer */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* ghost ribbons drift against the scroll */
(function(){try{
  if(!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  gsap.registerPlugin(ScrollTrigger);
  gsap.utils.toArray('.ghost').forEach(function(g){
    var rev=g.classList.contains('ghost-r'), s=g.querySelector('span');
    gsap.fromTo(s,{x:rev?-420:60},{x:rev?60:-420,ease:'none',
      scrollTrigger:{trigger:g,start:'top bottom',end:'bottom top',scrub:1}});
  });
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* selected work: show a random few of the projects, fresh on every visit.
   Every project stays in the markup; the case studies page shows them all. */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();

/* stats: film-counter odometer (IntersectionObserver — no ScrollTrigger dependency) */
(function(){try{
  var nums=document.querySelectorAll('.ptc-num');
  if(!nums.length) return;
  var col='<i>0</i><i>1</i><i>2</i><i>3</i><i>4</i><i>5</i><i>6</i><i>7</i><i>8</i><i>9</i>';
  var items=[];
  nums.forEach(function(el){
    var digits=String(el.getAttribute('data-count')||el.textContent).replace(/\D/g,'').split('');
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
/* filmstrip progress rail */
(function(){try{
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();


/* ===== consent-gated marketing tags =====
   EDIT: paste your Meta Pixel ID between the quotes to switch tracking on.
   Find it at facebook.com/events_manager -> Data Sources -> your pixel (a ~15-digit number).
   Leave it empty and nothing loads and no banner is shown. */
var PTC_META_PIXEL_ID = '1589986489809939';

(function(){try{
  var KEY = 'ptc-consent';
  var el = document.getElementById('ck');
  function get(){ try { return localStorage.getItem(KEY); } catch(e){ return null; } }
  function set(v){ try { localStorage.setItem(KEY, v); } catch(e){} }

  /* --- Meta Pixel, only ever called after consent --- */
  function loadMeta(){
    if (!PTC_META_PIXEL_ID || window.fbq) return;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
      n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
      (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', PTC_META_PIXEL_ID);
    window.fbq('track', 'PageView');
  }
  /* add other platforms here (TikTok, LinkedIn, Google Ads) so they stay consent-gated too */
  function loadAll(){ loadMeta(); }

  var choice = get();
  if (choice === 'yes') { loadAll(); }
  else if (!choice && el && PTC_META_PIXEL_ID) { el.hidden = false; }

  if (el) {
    var yes = el.querySelector('.ck-yes'), no = el.querySelector('.ck-no');
    if (yes) yes.addEventListener('click', function(){
      set('yes'); el.hidden = true; loadAll();
      if (window.__ptcFirePageEvents) window.__ptcFirePageEvents();
    });
    if (no)  no.addEventListener('click',  function(){ set('no');  el.hidden = true; });
  }
  /* footer "Cookie settings" lets a visitor change their mind */
  document.querySelectorAll('.ck-reopen').forEach(function(b){
    b.addEventListener('click', function(ev){ ev.preventDefault(); if (el) el.hidden = false; });
  });

  /* ===== event layer =====
     Every call is consent-gated. Tiers, most valuable first:
       1 Lead     - contact form sent            (optimise campaigns on this)
       1 Contact  - phone or email clicked       (an enquiry that skips the form)
       2 ViewContent - services / case studies   (commercial intent -> best retargeting pool)
       2 ShowreelPlay - pressed play             (custom; engaged with the work)
       3 StoryComplete / DeepScroll              (custom; read properly, weak but useful)
       4 PageView - every page                   (baseline audience) */
  function track(name, params, custom){
    if (get() !== 'yes' || !window.fbq) return;
    window.fbq(custom ? 'trackCustom' : 'track', name, params || {});
  }
  var fired = {};
  function trackOnce(key, name, params, custom){
    if (fired[key]) return;
    fired[key] = true;
    track(name, params, custom);
  }
  window.ptcTrack = track;
  window.ptcTrackOnce = trackOnce;
  window.ptcTrackLead = function(){ track('Lead', {content_name:'Contact form'}); };

  var file = (location.pathname.split('/').pop() || 'index.html');
  var page = file.replace(/\.html$/,'') || 'home';
  /* substring match, so clean URLs (/services) keep working too */
  var INTENT = [
    ['case-studies', 'Case Studies', 'Work'],
    ['services',     'Services',     'Services']
  ];
  function firePageEvents(){
    for (var i = 0; i < INTENT.length; i++) {
      if (file.indexOf(INTENT[i][0]) > -1) {
        trackOnce('view', 'ViewContent', {content_name:INTENT[i][1], content_category:INTENT[i][2]});
        return;
      }
    }
  }

  /* tier 1: a tap on the phone number or email is a real enquiry */
  document.addEventListener('click', function(e){
    var a = e.target && e.target.closest && e.target.closest('a[href^="tel:"],a[href^="mailto:"]');
    if (!a) return;
    track('Contact', {content_name: a.getAttribute('href').indexOf('tel:') === 0 ? 'Phone' : 'Email'});
  });

  /* tier 2: pressed play on the showreel */
  var film = document.querySelector('.film-frame');
  if (film) film.addEventListener('click', function(){
    track('ShowreelPlay', {content_name:'PTC Creatives Showreel'}, true);
  }, {once:true});

  /* tier 3: reached the end of the scroll story */
  var story = document.getElementById('pata');
  if (story && window.IntersectionObserver) {
    var last = story.querySelector('.ps-p5');
    if (last) {
      var sio = new IntersectionObserver(function(en){
        en.forEach(function(x){ if (x.isIntersecting) { sio.disconnect(); trackOnce('story','StoryComplete',{},true); } });
      }, {threshold:.25});
      sio.observe(last);
    }
  }

  /* tier 3: read three quarters of the page, once */
  var deep = false;
  window.addEventListener('scroll', function(){
    if (deep) return;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (h > 400 && (window.scrollY / h) >= 0.75) { deep = true; trackOnce('deep','DeepScroll',{content_name:page},true); }
  }, {passive:true});

  if (get() === 'yes') firePageEvents();
  window.__ptcFirePageEvents = firePageEvents;
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();


/* ===== case study chapter ===== */
(function(){try{
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
      /* the moon sinks away, then the sun climbs: night into day */
      .fromTo('#cs .cs-moon',{x:'16vw',y:'13vh',autoAlpha:1},{x:'44vw',y:'86vh',ease:'power1.in',duration:1.8},0)
      .to('#cs .cs-moon',{autoAlpha:0,duration:.35},1.5)
      .fromTo('#cs .cs-sun',{x:'52vw',y:'116vh',rotation:-140,autoAlpha:0},
                            {x:'58vw',y:'72vh',rotation:-60,autoAlpha:1,ease:'none',duration:.6},1.5)
      .to('#cs .cs-sun',{x:'74vw',y:'11vh',rotation:60,ease:'power2.out',duration:1.9},2.1);
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
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
