# Consent-gated marketing tags (Meta Pixel + room for others).
# The pixel only loads after the visitor accepts, and the choice is remembered.

CONSENT_HTML = """
  <div id="ck" class="ck" role="dialog" aria-label="Cookie choices" hidden>
    <div class="ck-in">
      <p class="ck-txt">We use cookies to see what brings people here and to show our work to the right
      audiences on platforms like Facebook and Instagram. Decline and the site works exactly the same.</p>
      <div class="ck-act">
        <a class="ck-more" href="privacy.html">Privacy Policy</a>
        <button class="ck-btn ck-no" type="button">Decline</button>
        <button class="ck-btn ck-yes" type="button">Accept</button>
      </div>
    </div>
  </div>
"""

CONSENT_CSS = """
/* ===== cookie consent ===== */
.ck{position:fixed;left:16px;right:16px;bottom:16px;z-index:300;background:rgba(10,20,20,.97);
  border:1px solid rgba(23,156,151,.4);border-radius:6px;backdrop-filter:blur(8px);
  box-shadow:0 20px 50px rgba(0,0,0,.5);font-family:'Poppins',sans-serif;
  animation:ckUp .45s cubic-bezier(.2,.8,.3,1) both;}
.ck[hidden]{display:none;}
@keyframes ckUp{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
.ck-in{display:flex;align-items:center;gap:26px;flex-wrap:wrap;max-width:1180px;margin:0 auto;padding:18px 22px;}
.ck-txt{flex:1 1 380px;margin:0;font-weight:300;font-size:14px;line-height:1.65;color:rgba(255,255,255,.82);}
.ck-act{display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
.ck-btn{font-family:'Poppins',sans-serif;font-size:12px;font-weight:400;letter-spacing:.16em;
  text-transform:uppercase;padding:12px 24px;min-height:42px;border-radius:3px;cursor:pointer;
  transition:background .25s,color .25s,border-color .25s;}
.ck-no{background:none;border:1px solid rgba(255,255,255,.3);color:rgba(255,255,255,.8);}
.ck-no:hover{border-color:#fff;color:#fff;}
.ck-yes{background:#179c97;border:1px solid #179c97;color:#0a1414;}
.ck-yes:hover{background:#e8a317;border-color:#e8a317;}
.ck-more{font-size:12px;font-weight:300;color:#179c97;text-decoration:none;min-height:42px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent;}
.ck-more:hover{border-bottom-color:#179c97;}
@media (max-width:700px){
  .ck{left:10px;right:10px;bottom:10px;}
  .ck-in{padding:16px;gap:14px;}
  .ck-txt{font-size:13.5px;}
  .ck-act{width:100%;}
  .ck-btn{flex:1;text-align:center;justify-content:center;}
}
.ck-reopen{background:none;border:none;padding:0;font:inherit;color:inherit;cursor:pointer;
  text-decoration:none;border-bottom:1px solid transparent;}
.ck-reopen:hover{color:#179c97;}
"""

CONSENT_JS = """
/* ===== consent-gated marketing tags =====
   EDIT: paste your Meta Pixel ID between the quotes to switch tracking on.
   Find it at facebook.com/events_manager -> Data Sources -> your pixel (a ~15-digit number).
   Leave it empty and nothing loads and no banner is shown. */
var PTC_META_PIXEL_ID = '';

(function(){
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
})();
"""
