/* Noventrax Solutions — shared interactions (vanilla JS, no dependencies) */
(function(){
  "use strict";
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Loader ---------- */
  window.addEventListener('load', function(){
    var loader = document.getElementById('loader');
    if(!loader) return;
    setTimeout(function(){ loader.classList.add('hide'); }, reducedMotion ? 0 : 480);
  });

  /* ---------- Mobile nav ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('nav.primary');
  if(toggle && nav){
    toggle.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ nav.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); });
    });
  }

  /* ---------- Active nav link ---------- */
  var here = (location.pathname.split('/').pop() || 'index.html');
  document.querySelectorAll('nav.primary a').forEach(function(a){
    var href = a.getAttribute('href');
    if(href === here || (here === '' && href === 'index.html')) a.classList.add('active');
  });

  /* ---------- Scroll reveal ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window && !reducedMotion){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: .12, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(function(el){ io.observe(el); });
  } else {
    revealEls.forEach(function(el){ el.classList.add('in'); });
  }

  /* ---------- Card tilt ---------- */
  if(!reducedMotion && matchMedia('(hover:hover)').matches){
    document.querySelectorAll('.tilt').forEach(function(card){
      card.addEventListener('mousemove', function(e){
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - .5;
        var y = (e.clientY - r.top) / r.height - .5;
        card.style.transform = 'perspective(800px) rotateX(' + (y * -6) + 'deg) rotateY(' + (x * 8) + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', function(){ card.style.transform = ''; });
    });
  }

  /* ---------- Cursor glow ---------- */
  if(!reducedMotion && matchMedia('(hover:hover)').matches){
    var glow = document.createElement('div');
    glow.style.cssText = 'position:fixed;width:420px;height:420px;border-radius:50%;pointer-events:none;z-index:1;background:radial-gradient(circle,rgba(122,31,43,.10),transparent 70%);transform:translate(-50%,-50%);transition:opacity .3s;opacity:0;';
    document.body.appendChild(glow);
    window.addEventListener('mousemove', function(e){
      glow.style.left = e.clientX + 'px'; glow.style.top = e.clientY + 'px'; glow.style.opacity = '1';
    });
    window.addEventListener('mouseleave', function(){ glow.style.opacity = '0'; });
  }

  /* ---------- Marquee auto-duplicate ---------- */
  document.querySelectorAll('.marquee-track').forEach(function(track){
    if(track.dataset.dup) return;
    track.innerHTML += track.innerHTML;
    track.dataset.dup = '1';
  });

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll('.faq-item').forEach(function(item){
    var q = item.querySelector('.faq-q');
    var a = item.querySelector('.faq-a');
    if(!q || !a) return;
    q.addEventListener('click', function(){
      var isOpen = item.classList.contains('open');
      item.closest('.faq-list').querySelectorAll('.faq-item.open').forEach(function(other){
        if(other !== item){ other.classList.remove('open'); other.querySelector('.faq-a').style.maxHeight = 0; }
      });
      item.classList.toggle('open', !isOpen);
      a.style.maxHeight = !isOpen ? (a.scrollHeight + 'px') : 0;
    });
  });

  /* ---------- Form validation (placeholder — no backend) ---------- */
  document.querySelectorAll('form[data-validate]').forEach(function(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var valid = true;
      form.querySelectorAll('[required]').forEach(function(field){
        var wrap = field.closest('.form-field');
        var ok = field.type === 'email'
          ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)
          : field.value.trim().length > 0;
        if(wrap) wrap.classList.toggle('error', !ok);
        if(!ok) valid = false;
      });
      if(valid){
        var success = form.querySelector('.form-success') || form.parentElement.querySelector('.form-success');
        form.reset();
        form.querySelectorAll('.form-field.error').forEach(function(w){ w.classList.remove('error'); });
        if(success) success.classList.add('show');
        form.setAttribute('data-submitted', 'true');
      }
    });
  });

  /* ---------- Live chat widget (placeholder) ---------- */
  var launcher = document.querySelector('.chat-launcher');
  var panel = document.querySelector('.chat-panel');
  if(launcher && panel){
    launcher.addEventListener('click', function(){
      var open = panel.classList.toggle('open');
      launcher.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    var closeBtn = panel.querySelector('.chat-close');
    if(closeBtn) closeBtn.addEventListener('click', function(){ panel.classList.remove('open'); });
    var chatForm = panel.querySelector('form');
    if(chatForm){
      chatForm.addEventListener('submit', function(e){
        e.preventDefault();
        var input = chatForm.querySelector('input');
        var body = panel.querySelector('.chat-body');
        if(!input.value.trim()) return;
        var mine = document.createElement('div');
        mine.className = 'chat-bubble';
        mine.style.marginLeft = 'auto';
        mine.style.background = '#3a1218';
        mine.textContent = input.value;
        body.appendChild(mine);
        input.value = '';
        body.scrollTop = body.scrollHeight;
        setTimeout(function(){
          var reply = document.createElement('div');
          reply.className = 'chat-bubble';
          reply.textContent = "Thanks for reaching out — this is a demo chat interface. A Noventrax solutions engineer will follow up by email shortly.";
          body.appendChild(reply);
          body.scrollTop = body.scrollHeight;
        }, 700);
      });
    }
  }

  /* ---------- Header background lattice generator ---------- */
  var latticeSVG = document.querySelector('.lattice-bg svg');
  if(latticeSVG){
    var w = 1600, h = 1000, pts = [], count = 26;
    for(var i=0;i<count;i++){
      pts.push({x: Math.random()*w, y: Math.random()*h});
    }
    var ns = 'http://www.w3.org/2000/svg';
    pts.forEach(function(p, idx){
      pts.forEach(function(p2, idx2){
        if(idx2 <= idx) return;
        var d = Math.hypot(p.x-p2.x, p.y-p2.y);
        if(d < 260){
          var line = document.createElementNS(ns, 'line');
          line.setAttribute('x1', p.x); line.setAttribute('y1', p.y);
          line.setAttribute('x2', p2.x); line.setAttribute('y2', p2.y);
          line.setAttribute('stroke', 'rgba(122,31,43,0.18)');
          line.setAttribute('stroke-width', '1');
          latticeSVG.appendChild(line);
        }
      });
    });
    pts.forEach(function(p){
      var c = document.createElementNS(ns, 'circle');
      c.setAttribute('cx', p.x); c.setAttribute('cy', p.y); c.setAttribute('r', 1.6);
      c.setAttribute('fill', 'rgba(200,68,86,0.35)');
      latticeSVG.appendChild(c);
    });
    latticeSVG.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    latticeSVG.setAttribute('preserveAspectRatio', 'xMidYMid slice');
  }
})();
