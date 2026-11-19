(() => {
  const root = document.querySelector("[data-ft-root]");
  if (!root) return;

  const bootEl = document.getElementById("ft-boot");
  let boot;
  try {
    boot = JSON.parse(bootEl ? bootEl.textContent || "{}" : "{}");
  } catch {
    return;
  }

  const drawUrl = boot.draw_url || "/fortune/api/draw";
  const disclaimer = boot.disclaimer || "";

  const tube = document.getElementById("ft-tube");
  const tubeWrap = document.getElementById("ft-tube-wrap");
  const rising = document.getElementById("ft-rising");
  const statusEl = document.getElementById("ft-status");
  const drawBtn = document.getElementById("ft-draw");
  const drawLabel = document.getElementById("ft-draw-label");
  const result = document.getElementById("ft-result");
  const card = document.getElementById("ft-card");
  const levelEl = document.getElementById("ft-level");
  const blurbEl = document.getElementById("ft-blurb");
  const titleEl = document.getElementById("ft-title");
  const verseEl = document.getElementById("ft-verse");
  const keysEl = document.getElementById("ft-keys");
  const dimsEl = document.getElementById("ft-dims");
  const seedEl = document.getElementById("ft-seed");
  const dailyJoyEl = document.getElementById("ft-daily-joy");
  const copyBtn = document.getElementById("ft-copy");
  const favBtn = document.getElementById("ft-fav");
  const hintEl = document.getElementById("ft-hint");
  const themeToggle = document.getElementById("ft-theme-toggle");
  const altar = root.querySelector(".ft-altar");

  const FAV_KEY = "atelier.fortune.favs.v1";
  // 主动求签仪式必须可感知；reduced-motion 只关装饰循环，不把仪式压成瞬间
  const T = { shake: 1200, settle: 350, rise: 900, hold: 450, seal: 1100 };
  const DIM_HUES = new Set(["sky", "rose", "lilac", "amber", "mint"]);

  let busy = false;
  let switching = false;
  let lastDraw = null;
  let drawnOnce = false;

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function setHint(text) {
    if (hintEl) hintEl.textContent = text || "";
  }

  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function syncDrawButton() {
    if (!drawBtn) return;
    drawBtn.disabled = busy || switching;
    if (drawLabel) drawLabel.textContent = drawnOnce ? "再求一支" : "求一支";
  }

  function showTube() {
    if (altar) altar.classList.remove("is-revealed");
    if (tubeWrap) {
      tubeWrap.classList.remove("is-dimmed");
      tubeWrap.hidden = false;
    }
    if (result) {
      result.hidden = true;
      result.classList.remove("is-present", "is-unveiled");
      result.classList.add("is-sealed");
    }
  }

  function escapeHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function scoreDots(score, maxScore) {
    const max = Math.max(1, Number(maxScore) || 5);
    const on = Math.max(0, Math.min(max, Number(score) || 0));
    let html = "";
    for (let i = 1; i <= max; i += 1) {
      html += `<span class="ft-dim__dot${i <= on ? " is-on" : ""}" aria-hidden="true"></span>`;
    }
    return html;
  }

  function renderDimensions(list) {
    if (!dimsEl) return;
    const rows = Array.isArray(list) ? list : [];
    if (!rows.length) {
      dimsEl.innerHTML = "";
      return;
    }
    dimsEl.innerHTML = rows
      .map((dim) => {
        const hue = DIM_HUES.has(dim.hue) ? dim.hue : "sky";
        const score = Math.max(1, Math.min(5, Number(dim.score) || 3));
        const maxScore = Math.max(1, Number(dim.max_score) || 5);
        const label = escapeHtml(dim.label || "");
        const tag = escapeHtml(dim.tag || "");
        const glyph = escapeHtml(dim.glyph || "·");
        const text = escapeHtml(dim.text || "");
        return (
          `<section class="ft-dim ft-dim--${hue}">` +
          `<div class="ft-dim__head">` +
          `<span class="ft-dim__pill"><span class="ft-dim__glyph">${glyph}</span>${label}</span>` +
          (tag ? `<span class="ft-dim__tag">${tag}</span>` : "") +
          `<span class="ft-dim__dots" aria-label="气场 ${score}/${maxScore}">${scoreDots(score, maxScore)}</span>` +
          `</div>` +
          `<span class="ft-dim__bar" style="--ft-score:${score}" aria-hidden="true"><i></i></span>` +
          `<p class="ft-dim__text">${text}</p>` +
          `</section>`
        );
      })
      .join("");
  }

  function renderSealed(payload) {
    const level = payload.level || {};
    const stick = payload.stick || {};
    lastDraw = payload;
    if (levelEl) levelEl.textContent = level.label || "";
    if (blurbEl) blurbEl.textContent = level.blurb || "";
    if (titleEl) titleEl.textContent = stick.title || "";
    if (verseEl) verseEl.textContent = stick.verse || "";
    if (seedEl) seedEl.textContent = payload.seed || "";
    if (dailyJoyEl) dailyJoyEl.textContent = payload.daily_joy ? `今日一喜 · ${payload.daily_joy}` : "";
    if (keysEl) {
      const keys = Array.isArray(payload.keywords) ? payload.keywords : [];
      keysEl.innerHTML = keys.map((k) => `<li>${escapeHtml(k)}</li>`).join("");
    }
    renderDimensions(payload.dimensions);
    if (card) card.dataset.tone = level.tone || "ok";
    if (tubeWrap) {
      tubeWrap.classList.add("is-dimmed");
      tubeWrap.hidden = true;
    }
    if (altar) altar.classList.add("is-revealed");
    if (result) {
      result.hidden = false;
      result.classList.add("is-sealed");
      result.classList.remove("is-unveiled");
      result.classList.remove("is-present");
      void result.offsetWidth;
      // 先只呈现「封」面，启封另走 unveilCard
      result.classList.add("is-present");
    }
  }

  function unveilCard() {
    if (!result) return;
    result.classList.remove("is-sealed");
    result.classList.add("is-unveiled");
  }

  async function fetchDraw() {
    const res = await fetch(drawUrl, {
      headers: { Accept: "application/json" },
      credentials: "same-origin",
    });
    if (!res.ok) throw new Error(`draw_http_${res.status}`);
    const data = await res.json();
    if (!data || data.ok === false) throw new Error(data?.error || "draw_failed");
    return data;
  }

  async function runDraw() {
    if (busy || switching) return;
    busy = true;
    syncDrawButton();
    setHint("");
    showTube();
    setStatus("签筒摇起来了……");

    if (rising) {
      rising.hidden = true;
      rising.classList.remove("is-out");
    }

    if (tube) {
      tube.classList.remove("is-shaking");
      void tube.offsetWidth;
      tube.classList.add("is-shaking");
    }

    let payload = null;
    let fetchError = null;
    const fetchPromise = fetchDraw().catch((err) => {
      fetchError = err;
      return null;
    });

    await wait(T.shake);
    if (tube) tube.classList.remove("is-shaking");
    setStatus("定神片刻……");
    await wait(T.settle);

    payload = await fetchPromise;
    if (!payload) {
      busy = false;
      syncDrawButton();
      setStatus("求签暂时不通，稍后再试。");
      setHint(fetchError ? String(fetchError.message || fetchError) : "");
      return;
    }

    setStatus("一支签升起来了……");
    if (rising) {
      rising.hidden = false;
      rising.classList.remove("is-out");
      void rising.offsetWidth;
      rising.classList.add("is-out");
    }
    await wait(T.rise);
    setStatus("签已出筒……");
    await wait(T.hold);

    renderSealed(payload);
    setStatus("封存片刻，静候启封……");
    await wait(T.seal);
    unveilCard();
    setStatus("签文已启封。开心最重要。");
    // 签面已可读：立刻解锁，启封动效自行播放，不再空锁按钮
    drawnOnce = true;
    busy = false;
    syncDrawButton();
  }

  function favText(payload) {
    const stick = payload.stick || {};
    const level = payload.level || {};
    const dims = Array.isArray(payload.dimensions) ? payload.dimensions : [];
    const dimLines = dims.map((d) => {
      const tag = d.tag ? `（${d.tag}）` : "";
      return `${d.label || "运势"}${tag}：${d.text || ""}`;
    });
    return [
      `【${level.label || "签"}】${stick.title || ""}`,
      stick.verse || "",
      ...dimLines,
      payload.daily_joy ? `今日一喜：${payload.daily_joy}` : "",
      payload.seed || "",
      disclaimer,
    ]
      .filter(Boolean)
      .join("\n");
  }

  async function copyLast() {
    if (!lastDraw) return;
    try {
      await navigator.clipboard.writeText(favText(lastDraw));
      setHint("已复制到剪贴板。");
    } catch {
      setHint("复制失败，请手动选中签文。");
    }
  }

  function loadFavs() {
    try {
      const raw = localStorage.getItem(FAV_KEY);
      const list = raw ? JSON.parse(raw) : [];
      return Array.isArray(list) ? list : [];
    } catch {
      return [];
    }
  }

  function saveFavs(list) {
    localStorage.setItem(FAV_KEY, JSON.stringify(list.slice(0, 20)));
  }

  function favLast() {
    if (!lastDraw) return;
    const stick = lastDraw.stick || {};
    const level = lastDraw.level || {};
    const entry = {
      level: level.label || "",
      title: stick.title || "",
      verse: stick.verse || "",
      at: Date.now(),
    };
    const list = loadFavs().filter((x) => !(x.title === entry.title && x.verse === entry.verse));
    list.unshift(entry);
    saveFavs(list);
    setHint("已收藏到本机（仅此浏览器）。");
  }

  function commitTheme(next) {
    document.documentElement.setAttribute("data-theme", next);
    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  }

  function isNarrowViewport() {
    return window.matchMedia("(max-width: 720px)").matches;
  }

  function prefersReduced() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function switchTheme() {
    if (switching || busy) return;

    const prev = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
    const next = prev === "dark" ? "light" : "dark";

    // Mobile / reduced-motion: avoid SVG clip liquid (full-screen black flash).
    if (
      isNarrowViewport() ||
      prefersReduced() ||
      !window.FortuneLiquid ||
      typeof window.FortuneLiquid.reveal !== "function"
    ) {
      switching = true;
      commitTheme(next);
      switching = false;
      syncDrawButton();
      return;
    }

    switching = true;
    syncDrawButton();
    document.documentElement.classList.add("is-liquidating");

    window.FortuneLiquid.reveal({
      fromBtn: themeToggle,
      toTheme: next,
      duration: 3900,
      prepareLayer(layer) {
        const clone = root.cloneNode(true);
        clone.removeAttribute("id");
        clone.querySelectorAll("[id]").forEach((el) => el.removeAttribute("id"));
        clone.setAttribute("data-theme", next);
        layer.setAttribute("data-theme", next);
        layer.appendChild(clone);
      },
      onCover() {
        commitTheme(next);
      },
      onDone() {
        document.documentElement.classList.remove("is-liquidating");
        switching = false;
        syncDrawButton();
      },
    });
  }

  drawBtn?.addEventListener("click", () => {
    void runDraw();
  });
  copyBtn?.addEventListener("click", () => {
    void copyLast();
  });
  favBtn?.addEventListener("click", favLast);
  themeToggle?.addEventListener("click", switchTheme);

  syncDrawButton();
  setStatus("静心一念，摇一支随缘签。");
})();
