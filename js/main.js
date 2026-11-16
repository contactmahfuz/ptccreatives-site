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

  /* ---- entrance: the scene assembles on load ---- */
  gsap.timeline({defaults:{ease:'power3.out'}})
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
    /* lighter, unpinned parallax on phones */
    choreo(gsap.timeline({scrollTrigger:{trigger:'#ptc-hero',start:'top 85%',end:'bottom top',scrub:1}}),.6);
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
    if(f.getAttribute('action').indexOf('YOUR_FORM_ID')>-1){
      e.preventDefault();
      var m=f.querySelector('.fmsg');
      if(m){m.textContent='The form is not connected yet. Please use the email or phone number above.';m.style.display='block';}
    }
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
    var m=card.querySelector('.card-top .m'); if(m) gsap.set(m,{z:46});
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
var PTC_META_PIXEL_ID = '';

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
    if (yes) yes.addEventListener('click', function(){ set('yes'); el.hidden = true; loadAll(); });
    if (no)  no.addEventListener('click',  function(){ set('no');  el.hidden = true; });
  }
  /* footer "Cookie settings" lets a visitor change their mind */
  document.querySelectorAll('.ck-reopen').forEach(function(b){
    b.addEventListener('click', function(ev){ ev.preventDefault(); if (el) el.hidden = false; });
  });

  /* fire a Lead event when the contact form is submitted, if consent was given */
  var f = document.querySelector('.ptc-form');
  if (f) f.addEventListener('submit', function(){
    if (get() === 'yes' && window.fbq) window.fbq('track', 'Lead');
  });
}catch(_e){if(window.console&&console.warn)console.warn('ptc module error:',_e);}})();
