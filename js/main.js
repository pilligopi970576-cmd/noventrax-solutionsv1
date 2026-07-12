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

  /* ---------- Firefly network hero visual ---------- */
  (function(){
    var wrap = document.getElementById('fireflyHero');
    var canvas = document.getElementById('fireflyCanvas');
    if(!wrap || !canvas) return;
    var ctx = canvas.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = 0, h = 0, cx = 0, cy = 0, radius = 0;
    var mouse = { x: -9999, y: -9999, active: false };
    var particles = [];
    var COUNT = 9;
    var LINK_DIST = 0.34;   // relative to radius
    var MOUSE_DIST = 0.22;  // relative to radius

    function size(){
      var rect = wrap.getBoundingClientRect();
      w = rect.width; h = rect.height;
      if(w < 10 || h < 10){
        // container not laid out yet (e.g. fonts/CSS still settling) — retry shortly
        setTimeout(size, 120);
        return;
      }
      canvas.width = w * dpr; canvas.height = h * dpr;
      canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cx = w / 2; cy = h / 2;
      radius = Math.min(w, h) * 0.46;
      if(particles.length === 0) makeParticles();
    }

    function makeParticles(){
      particles = [];
      for(var i = 0; i < COUNT; i++){
        var angle = Math.random() * Math.PI * 2;
        var dist = radius * (0.35 + Math.random() * 0.6);
        particles.push({
          x: cx + Math.cos(angle) * dist,
          y: cy + Math.sin(angle) * dist,
          vx: (Math.random() - 0.5) * 0.25,
          vy: (Math.random() - 0.5) * 0.25,
          r: 2 + Math.random() * 1.6
        });
      }
    }

    size();
    window.addEventListener('resize', function(){ size(); });

    wrap.addEventListener('mousemove', function(e){
      var rect = wrap.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
      mouse.active = true;
    });
    wrap.addEventListener('mouseleave', function(){ mouse.active = false; });

    function step(){
      particles.forEach(function(p){
        // gentle drift
        p.x += p.vx; p.y += p.vy;

        // soft circular boundary containment
        var dx = p.x - cx, dy = p.y - cy;
        var d = Math.hypot(dx, dy);
        if(d > radius){
          var nx = dx / d, ny = dy / d;
          p.x = cx + nx * radius; p.y = cy + ny * radius;
          p.vx -= nx * 0.04; p.vy -= ny * 0.04;
        }

        // gentle cursor avoidance
        if(mouse.active){
          var mdx = p.x - mouse.x, mdy = p.y - mouse.y;
          var mdist = Math.hypot(mdx, mdy);
          var threshold = radius * MOUSE_DIST;
          if(mdist < threshold && mdist > 0.01){
            var force = (1 - mdist / threshold) * 0.06;
            p.vx += (mdx / mdist) * force;
            p.vy += (mdy / mdist) * force;
          }
        }

        // gentle drag so it doesn't speed up forever
        p.vx *= 0.985; p.vy *= 0.985;

        // tiny random wander
        p.vx += (Math.random() - 0.5) * 0.006;
        p.vy += (Math.random() - 0.5) * 0.006;
      });
    }

    function draw(){
      ctx.clearRect(0, 0, w, h);

      // faint concentric guide rings
      ctx.strokeStyle = 'rgba(207,208,211,0.10)';
      ctx.lineWidth = 1;
      [0.55, 0.78, 1].forEach(function(f){
        ctx.beginPath();
        ctx.arc(cx, cy, radius * f, 0, Math.PI * 2);
        ctx.stroke();
      });

      // connecting lines between nearby particles
      var linkThreshold = radius * LINK_DIST;
      for(var i = 0; i < particles.length; i++){
        for(var j = i + 1; j < particles.length; j++){
          var a = particles[i], b = particles[j];
          var dist = Math.hypot(a.x - b.x, a.y - b.y);
          if(dist < linkThreshold){
            var alpha = (1 - dist / linkThreshold) * 0.35;
            ctx.strokeStyle = 'rgba(200,68,86,' + alpha.toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }

      // particles themselves, glowing
      particles.forEach(function(p){
        var grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4);
        grad.addColorStop(0, 'rgba(201,68,86,0.9)');
        grad.addColorStop(1, 'rgba(201,68,86,0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = 'rgba(242,240,238,0.9)';
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      });
    }

    if(reducedMotion){
      draw(); // single static frame, no animation loop
    } else {
      (function loop(){
        step();
        draw();
        requestAnimationFrame(loop);
      })();
    }
  })();

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
