/* Liquid theme reveal — adapted from Predict liquid.js for light/dark */
(function (global) {
  function prefersReduced() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function ensureClipSvg() {
    let svg = document.getElementById("liquid-clip-svg");
    if (!svg) {
      svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.id = "liquid-clip-svg";
      svg.setAttribute("aria-hidden", "true");
      svg.innerHTML = `
        <defs>
          <clipPath id="liquid-clip" clipPathUnits="userSpaceOnUse">
            <path id="liquid-path" d=""></path>
          </clipPath>
        </defs>`;
      document.body.appendChild(svg);
    }
    svg.style.cssText = "position:fixed;width:0;height:0;overflow:hidden;pointer-events:none;";
    return svg.querySelector("#liquid-path");
  }

  function buildPath(s, w, h) {
    const { ox, oy, colH, colW, poolH, wave } = s;
    let d = "";

    if (colH > 2) {
      const tip = Math.min(h + 40, oy + colH);
      const bulge = Math.min(18, colH * 0.04);
      d += `M ${ox - colW / 2} ${oy}`;
      for (let i = 0; i <= 18; i++) {
        const p = i / 18;
        const y = oy + (tip - oy) * p;
        const widen = Math.sin(p * Math.PI) * bulge;
        const wob = Math.sin(wave + p * 8) * (6 + colW * 0.14);
        d += ` L ${ox + colW / 2 + widen + wob} ${y}`;
      }
      d += ` Q ${ox} ${tip + 10 + Math.sin(wave) * 4} ${ox - colW / 2 - bulge} ${tip}`;
      for (let i = 18; i >= 0; i--) {
        const p = i / 18;
        const y = oy + (tip - oy) * p;
        const widen = Math.sin(p * Math.PI) * bulge;
        const wob = Math.sin(wave + p * 8 + 1.4) * (6 + colW * 0.14);
        d += ` L ${ox - colW / 2 - widen - wob} ${y}`;
      }
      d += " Z";
    }

    if (poolH > 2) {
      const surface = h - poolH;
      d += ` M -60 ${h + 60} L ${w + 60} ${h + 60} L ${w + 60} ${surface}`;
      for (let i = 36; i >= 0; i--) {
        const x = (w * i) / 36;
        const amp = 8 + Math.min(28, poolH * 0.045);
        const y =
          surface +
          Math.sin(wave * 1.15 + i * 0.42) * amp +
          Math.sin(wave * 0.7 + i * 0.9) * amp * 0.35;
        d += ` L ${x} ${y}`;
      }
      d += " Z";
    }

    (s.drops || []).forEach((dr) => {
      d += ` M ${dr.x - dr.r} ${dr.y} a ${dr.r} ${dr.r} 0 1 0 ${dr.r * 2} 0 a ${dr.r} ${dr.r} 0 1 0 ${-dr.r * 2} 0`;
    });
    (s.splash || []).forEach((sp) => {
      d += ` M ${sp.x - sp.r} ${sp.y} a ${sp.r} ${sp.r} 0 1 0 ${sp.r * 2} 0 a ${sp.r} ${sp.r} 0 1 0 ${-sp.r * 2} 0`;
    });

    return d || "M 0 0 Z";
  }

  function drawRim(ctx, s, w, h, toDark, alpha, pathD) {
    ctx.clearRect(0, 0, w, h);
    const stroke = toDark ? "rgba(210,190,140,0.55)" : "rgba(40,90,70,0.45)";
    const glow = toDark ? "rgba(140,180,230,0.2)" : "rgba(180,90,60,0.16)";
    const fillTint = toDark ? "rgba(20,28,42,0.12)" : "rgba(244,236,220,0.14)";

    const p = new Path2D(pathD);
    ctx.globalAlpha = alpha;
    ctx.fillStyle = fillTint;
    ctx.fill(p);
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.strokeStyle = glow;
    ctx.lineWidth = 8;
    ctx.stroke(p);
    ctx.strokeStyle = stroke;
    ctx.lineWidth = 2;
    ctx.stroke(p);

    if (s.poolH > 30) {
      const surface = h - s.poolH;
      ctx.beginPath();
      for (let i = 0; i <= 24; i++) {
        const x = (w * i) / 24;
        const amp = 7 + Math.min(22, s.poolH * 0.04);
        const y = surface + Math.sin(s.wave * 1.15 + i * 0.42) * amp;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = toDark ? "rgba(230,240,255,0.32)" : "rgba(255,255,255,0.35)";
      ctx.lineWidth = 1.4;
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function reveal(opts) {
    const {
      fromBtn,
      duration = 3900,
      onCover,
      onDone,
      prepareLayer,
      toTheme = "dark",
    } = opts;

    const w = window.innerWidth;
    const h = window.innerHeight;
    const rect = fromBtn.getBoundingClientRect();
    const ox = rect.left + rect.width / 2;
    const oy = Math.min(h - 48, Math.max(8, rect.bottom - 2));
    const totalDur = prefersReduced() ? Math.min(duration, 1200) : duration;
    const toDark = toTheme === "dark";

    const pathEl = ensureClipSvg();

    const layer = document.createElement("div");
    layer.className = "liquid-reveal";
    layer.dataset.theme = toTheme;
    layer.style.clipPath = "url(#liquid-clip)";
    layer.style.webkitClipPath = "url(#liquid-clip)";
    document.body.appendChild(layer);
    if (typeof prepareLayer === "function") prepareLayer(layer);

    const rim = document.createElement("canvas");
    rim.className = "liquid-rim";
    const dpr = Math.min(window.devicePixelRatio || 1, 1.25);
    rim.width = Math.floor(w * dpr);
    rim.height = Math.floor(h * dpr);
    rim.style.width = `${w}px`;
    rim.style.height = `${h}px`;
    document.body.appendChild(rim);
    const rctx = rim.getContext("2d", { alpha: true, desynchronized: true });
    rctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    let rimTick = 0;

    const start = performance.now();
    let raf = 0;
    let covered = false;
    let cancelled = false;
    const state = {
      ox,
      oy,
      colH: 6,
      colW: Math.max(16, rect.width * 0.48),
      poolH: 0,
      wave: 0,
      drops: [],
      splash: [],
    };

    const easeIn = (t) => t * t;
    const easeOut = (t) => 1 - Math.pow(1 - t, 3);

    const frame = (now) => {
      if (cancelled) return;
      const raw = Math.min(1, (now - start) / totalDur);
      state.wave += 0.11;

      if (raw < 0.22) {
        const p = raw / 0.22;
        state.colH = (h - oy) * (0.12 + easeIn(p) * 0.95);
        state.colW = Math.max(16, rect.width * 0.48) * (0.85 + Math.sin(p * Math.PI) * 0.55);
        if (p > 0.4 && state.drops.length < 6 && Math.random() > 0.62) {
          state.drops.push({
            x: ox + (Math.random() - 0.5) * state.colW * 1.1,
            y: oy + state.colH * (0.25 + Math.random() * 0.5),
            r: 3 + Math.random() * 6,
            vy: 1.2 + Math.random() * 2,
          });
        }
      } else if (raw < 0.34) {
        state.colH = h - oy + 40;
        const p = (raw - 0.22) / 0.12;
        state.poolH = 24 + easeOut(p) * 110;
        state.splash = Array.from({ length: 8 }, (_, i) => {
          const ang = (i / 8) * Math.PI - Math.PI / 2;
          const dist = 18 + p * 80;
          return {
            x: ox + Math.cos(ang) * dist * (0.75 + (i % 3) * 0.12),
            y: h - 10 - Math.sin(p * Math.PI) * (26 + (i % 4) * 7),
            r: 4 + (i % 3) * 2.2 * (1 - p * 0.35),
          };
        });
      } else if (raw < 0.86) {
        const p = (raw - 0.34) / 0.52;
        state.colH = Math.max(0, (h - oy) * (1 - easeOut(Math.min(1, p * 1.4))));
        state.colW *= 0.992;
        const rise = easeIn(p) * 0.35 + easeOut(p) * 0.65;
        state.poolH = 130 + rise * (h + 160);
        state.splash = state.splash.map((sp) => ({
          ...sp,
          r: sp.r * 0.985,
          y: sp.y - 0.25,
        }));
      } else {
        state.colH = 0;
        state.poolH = h + 200;
        state.splash = [];
      }

      state.drops = state.drops
        .map((d) => ({ ...d, y: d.y + d.vy, vy: d.vy + 0.14 }))
        .filter((d) => d.y < h + 40);

      const pathD = buildPath(state, w, h);
      pathEl.setAttribute("d", pathD);

      rimTick += 1;
      if (rimTick % 3 === 0) {
        const rimAlpha = raw < 0.9 ? 1 : 1 - (raw - 0.9) / 0.1;
        drawRim(rctx, state, w, h, toDark, Math.max(0, rimAlpha), pathD);
      }

      if (!covered && state.poolH > h * 0.95) {
        covered = true;
        if (onCover) onCover();
      }

      if (raw < 1) {
        raf = requestAnimationFrame(frame);
      } else {
        if (onDone) onDone();
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            if (cancelled) return;
            layer.remove();
            rim.style.transition = "opacity 0.28s ease";
            rim.style.opacity = "0";
            setTimeout(() => {
              rim.remove();
            }, 300);
          });
        });
      }
    };

    pathEl.setAttribute("d", buildPath(state, w, h));
    raf = requestAnimationFrame(frame);

    return {
      cancel() {
        cancelled = true;
        cancelAnimationFrame(raf);
        layer.remove();
        rim.remove();
      },
    };
  }

  global.FortuneLiquid = { reveal };
})(window);
