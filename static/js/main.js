(function () {
  "use strict";

  const html = document.documentElement;
  const WALLPAPER_STORAGE_KEY = "wallpaper-mode";

  function initWallpaper() {
    const dataEl = document.getElementById("wiki-wallpapers-data");
    const layer = document.getElementById("wiki-wallpaper");
    const video = document.getElementById("wiki-wallpaper-video");
    const image = document.getElementById("wiki-wallpaper-image");
    const select = document.getElementById("wallpaper-select");
    if (!dataEl || !layer || !video || !image) return;

    let wallpapers;
    try {
      wallpapers = JSON.parse(dataEl.textContent || "[]");
    } catch {
      return;
    }
    if (!wallpapers.length) return;

    const defaultId =
      wallpapers.find((w) => w.default)?.id || wallpapers[0].id;

    const LEGACY_WALLPAPER_IDS = {
      "wp-0": "wallpaper-02-preview-alt",
      "wp-1": "wallpaper-01-preview",
      "wp-2": "wallpaper-03-minecraft",
      "wp-3": "wallpaper-04-cloud-pixel",
    };

    let activeWallpaperId = null;

    const wallpaperUrl = (item) => new URL(item.url, window.location.href).href;

    const videoHasSrc = (url) => {
      const target = new URL(url, window.location.href).pathname;
      if (!video.currentSrc && !video.getAttribute("src")) return false;
      try {
        return new URL(video.currentSrc || video.src, window.location.href).pathname === target;
      } catch {
        return false;
      }
    };

    const playVideo = () => video.play().catch(() => {});

    const setWallpaperVideoActive = (on) => {
      html.classList.toggle("wallpaper-video-active", Boolean(on));
    };

    const markVideoActive = () => setWallpaperVideoActive(true);

    video.addEventListener("playing", markVideoActive);
    video.addEventListener("loadeddata", markVideoActive);
    video.addEventListener("emptied", () => setWallpaperVideoActive(false));
    video.addEventListener("error", () => {
      setWallpaperVideoActive(false);
      html.classList.add("wallpaper-load-failed");
    });
    video.addEventListener("playing", () => html.classList.remove("wallpaper-load-failed"));

    const applyWallpaper = (item, forceReload) => {
      if (!item || !item.url) {
        return;
      }
      document.body.classList.add("has-wallpaper");
      html.classList.add("wallpaper-enabled");
      setWallpaperVideoActive(true);
      const url = wallpaperUrl(item);
      if (item.is_video) {
        image.hidden = true;
        image.removeAttribute("src");
        video.hidden = false;
        const needsLoad =
          forceReload || activeWallpaperId !== item.id || !videoHasSrc(url);
        if (needsLoad) {
          activeWallpaperId = item.id;
          if (forceReload || !videoHasSrc(url)) {
            video.pause();
            video.src = url;
            video.load();
          }
          video.addEventListener("loadeddata", playVideo, { once: true });
          video.addEventListener("canplay", playVideo, { once: true });
          playVideo();
        } else if (video.paused) {
          playVideo();
        } else {
          markVideoActive();
        }
      } else {
        activeWallpaperId = item.id;
        video.pause();
        video.removeAttribute("src");
        video.hidden = true;
        image.hidden = false;
        if (forceReload || image.src !== url) {
          image.src = url;
        }
      }
    };

    const resolveId = () => {
      let stored = localStorage.getItem(WALLPAPER_STORAGE_KEY);
      if (stored === "random") stored = null;
      if (stored === "none") {
        stored = null;
        localStorage.removeItem(WALLPAPER_STORAGE_KEY);
      }
      if (stored && LEGACY_WALLPAPER_IDS[stored]) {
        stored = LEGACY_WALLPAPER_IDS[stored];
        localStorage.setItem(WALLPAPER_STORAGE_KEY, stored);
      }
      if (stored && wallpapers.some((w) => w.id === stored)) {
        return stored;
      }
      return defaultId;
    };

    const resolveWallpaper = () =>
      wallpapers.find((w) => w.id === resolveId()) || wallpapers[0];

    const initial = resolveWallpaper();
    if (video.currentSrc || video.getAttribute("src")) {
      activeWallpaperId = initial.id;
    }
    applyWallpaper(initial);

    const unlockAutoplay = () => {
      if (!document.body.classList.contains("has-wallpaper") || video.hidden) return;
      if (video.paused && (video.src || video.currentSrc)) playVideo();
    };
    document.addEventListener("click", unlockAutoplay, { once: true, capture: true });
    document.addEventListener("keydown", unlockAutoplay, { once: true, capture: true });
    window.addEventListener("load", unlockAutoplay);

    const syncVideoPlayback = () => {
      if (!video || video.hidden) return;
      if (document.hidden) {
        video.pause();
      } else if (video.src) {
        video.play().catch(() => {});
      }
    };
    document.addEventListener("visibilitychange", syncVideoPlayback);
    syncVideoPlayback();

    if (select) {
      const syncSelect = () => {
        select.value = resolveId();
      };
      syncSelect();
      select.addEventListener("change", () => {
        const next = select.value;
        localStorage.setItem(WALLPAPER_STORAGE_KEY, next);
        const item = wallpapers.find((w) => w.id === next);
        if (item) {
          activeWallpaperId = null;
          applyWallpaper(item, true);
          syncSelect();
        }
      });
    }
  }

  initWallpaper();

  function initMpPortal() {
    document.body.classList.add("client-js");

    document.querySelectorAll(".mp-wrapper .collapsible .collapsetoggle").forEach((btn) => {
      const section = btn.closest(".collapsible");
      if (!section) return;
      const expanded = !section.classList.contains("collapsed");
      btn.setAttribute("aria-expanded", expanded ? "true" : "false");
      btn.addEventListener("click", () => {
        const isCollapsed = section.classList.toggle("collapsed");
        btn.setAttribute("aria-expanded", isCollapsed ? "false" : "true");
      });
    });
  }

  initMpPortal();

  function initGuideTocMobile() {
    const details = document.querySelector(".guide-toc-mobile");
    if (!details) return;
    const mq = window.matchMedia("(min-width: 901px)");
    const apply = () => {
      if (mq.matches) {
        details.setAttribute("open", "");
      } else {
        details.removeAttribute("open");
      }
    };
    apply();
    mq.addEventListener("change", apply);
  }

  initGuideTocMobile();

  const syncThemeToggleIcon = () => {
    document.querySelectorAll(".theme-toggle").forEach((btn) => {
      btn.textContent = html.getAttribute("data-theme") === "dark" ? "☀" : "☽";
    });
  };

  const applyTheme = (theme) => {
    html.setAttribute("data-theme", theme);
    document.body.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    syncThemeToggleIcon();
  };

  const stored = localStorage.getItem("theme");
  const initialTheme = stored === "dark" ? "dark" : "light";
  applyTheme(initialTheme);

  document.querySelectorAll(".theme-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
    });
  });

  const sidebar = document.getElementById("wiki-sidebar");
  const backdrop = document.getElementById("wiki-sidebar-backdrop");
  const toggle = document.querySelector(".wiki-nav-toggle");

  let sidebarScrollY = 0;
  const setSidebarOpen = (open) => {
    document.body.classList.toggle("sidebar-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) backdrop.hidden = !open;
    if (open) {
      sidebarScrollY = window.scrollY;
      document.body.style.overflow = "hidden";
      document.body.style.position = "fixed";
      document.body.style.width = "100%";
      document.body.style.top = `-${sidebarScrollY}px`;
    } else {
      document.body.style.overflow = "";
      document.body.style.position = "";
      document.body.style.width = "";
      document.body.style.top = "";
      window.scrollTo(0, sidebarScrollY);
    }
  };

  toggle?.addEventListener("click", () => {
    setSidebarOpen(!document.body.classList.contains("sidebar-open"));
  });
  backdrop?.addEventListener("click", () => setSidebarOpen(false));

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape" || !document.body.classList.contains("sidebar-open")) return;
    const lightbox = document.getElementById("wiki-lightbox");
    if (lightbox && !lightbox.hidden) return;
    setSidebarOpen(false);
  });

  const path = window.location.pathname;
  const navLinks = Array.from(document.querySelectorAll(".wiki-nav a[href]"));
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      const href = link.getAttribute("href");
      if (href && !href.startsWith("http") && !href.startsWith("mailto:")) {
        setSidebarOpen(false);
      }
    });
  });
  let currentNav = null;
  let currentLen = -1;
  navLinks.forEach((link) => {
    if (link.classList.contains("is-current")) return;
    const href = link.getAttribute("href");
    if (!href || href.startsWith("http") || href.startsWith("mailto:")) return;
    const match =
      href === "/"
        ? path === "/"
        : path === href || path.startsWith(href + "/");
    if (match && href.length > currentLen) {
      currentNav = link;
      currentLen = href.length;
    }
  });
  if (currentNav) currentNav.classList.add("is-current");

  function initInpageTocSpy(selector) {
    const links = document.querySelectorAll(selector);
    if (!links.length) return;
    const items = Array.prototype.map.call(links, (a) => {
      const id = a.getAttribute("href").slice(1);
      const el = document.getElementById(id);
      return { link: a, el };
    }).filter((x) => x.el);
    if (!items.length) return;
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const y = window.scrollY + 80;
        let current = items[0];
        for (let i = 0; i < items.length; i++) {
          if (items[i].el.offsetTop <= y) current = items[i];
        }
        items.forEach((x) => x.link.classList.remove("is-active"));
        if (current) current.link.classList.add("is-active");
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  initInpageTocSpy(".wiki-doc-nav--inpage a[href^=\"#\"]");
  initInpageTocSpy(".guide-sticky-toc a[href^=\"#\"]");

  function initGalleryLightbox() {
    const overlay = document.getElementById("wiki-lightbox");
    const imgEl = document.getElementById("wiki-lightbox-img");
    const captionEl = document.getElementById("wiki-lightbox-caption");
    const closeBtn = document.getElementById("wiki-lightbox-close");
    if (!overlay || !imgEl) return;

    const open = (src, alt, meta) => {
      imgEl.src = src;
      imgEl.alt = alt || "";
      if (captionEl) {
        const parts = [alt, meta].filter(Boolean);
        captionEl.textContent = parts.join(" · ");
        captionEl.hidden = !parts.length;
      }
      overlay.hidden = false;
      document.body.style.overflow = "hidden";
      closeBtn?.focus();
    };

    const close = () => {
      overlay.hidden = true;
      imgEl.removeAttribute("src");
      if (captionEl) {
        captionEl.textContent = "";
        captionEl.hidden = true;
      }
      document.body.style.overflow = "";
    };

    document.querySelectorAll("[data-gallery] .wiki-gallery__item img").forEach((thumb) => {
      thumb.addEventListener("click", () => {
        const item = thumb.closest(".wiki-gallery__item");
        const meta = item?.dataset.meta || "";
        open(thumb.src, thumb.alt, meta);
      });
    });

    closeBtn?.addEventListener("click", close);
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) close();
    });
    document.addEventListener("keydown", (e) => {
      if (!overlay.hidden && e.key === "Escape") close();
    });
  }

  initGalleryLightbox();

  function initBrowseTables() {
    document.querySelectorAll("[data-browse-filter]").forEach((input) => {
      const table = input.closest(".mp-section")?.querySelector("table.mp-data-table");
      const countEl = input.closest(".browse-toolbar")?.querySelector("[data-browse-count]");
      if (!table) return;
      const tbody = table.querySelector("tbody");
      if (!tbody) return;
      const rows = Array.from(tbody.querySelectorAll("tr"));

      const applyFilter = () => {
        const q = input.value.trim().toLowerCase();
        let visible = 0;
        rows.forEach((row) => {
          const text = row.textContent.toLowerCase();
          const show = !q || text.includes(q);
          row.hidden = !show;
          if (show) visible += 1;
        });
        if (countEl) countEl.textContent = String(visible);
      };
      input.addEventListener("input", applyFilter);
      applyFilter();
    });

    document.querySelectorAll("table.mp-data-table[data-sortable]").forEach((table) => {
      const thead = table.querySelector("thead");
      const tbody = table.querySelector("tbody");
      if (!thead || !tbody) return;
      thead.querySelectorAll("th").forEach((th, colIdx) => {
        th.style.cursor = "pointer";
        th.setAttribute("title", "点击排序");
        th.addEventListener("click", () => {
          const rows = Array.from(tbody.querySelectorAll("tr"));
          const asc = th.dataset.sortDir !== "asc";
          thead.querySelectorAll("th").forEach((h) => delete h.dataset.sortDir);
          th.dataset.sortDir = asc ? "asc" : "desc";
          rows.sort((a, b) => {
            const ac = (a.children[colIdx]?.textContent || "").trim();
            const bc = (b.children[colIdx]?.textContent || "").trim();
            const cmp = ac.localeCompare(bc, "zh-CN");
            return asc ? cmp : -cmp;
          });
          rows.forEach((r) => tbody.appendChild(r));
        });
      });
    });
  }

  initBrowseTables();

  const searchInput = document.getElementById("wiki-search");
  if (searchInput) {
    const navLinks = Array.from(document.querySelectorAll(".wiki-nav a[data-nav-label]"));
    searchInput.addEventListener("input", () => {
      const q = searchInput.value.trim().toLowerCase();
      navLinks.forEach((link) => {
        const label = (link.dataset.navLabel || link.textContent || "").toLowerCase();
        const match = !q || label.includes(q);
        link.classList.toggle("is-hidden", !match);
        link.closest("li")?.classList.toggle("is-hidden", !match);
      });
    });
  }

  document.querySelectorAll("[data-count]").forEach((el) => {
    const target = parseInt(el.dataset.count, 10);
    if (Number.isNaN(target)) return;
    el.textContent = target;
  });

  const form = document.getElementById("contact-form");
  const toast = document.getElementById("toast");

  const showToast = (msg, type = "success") => {
    if (!toast) return;
    toast.textContent = msg;
    toast.className = "toast show" + (type === "error" ? " error" : "");
    clearTimeout(showToast._t);
    showToast._t = setTimeout(() => {
      toast.className = "toast";
    }, 3000);
  };

  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    const fields = [
      form.querySelector("#name"),
      form.querySelector("#email-input"),
      form.querySelector("#message"),
    ];
    let ok = true;
    fields.forEach((f) => {
      f?.classList.remove("error");
      if (!f?.value.trim()) {
        f?.classList.add("error");
        ok = false;
      }
    });
    const email = form.querySelector("#email-input");
    if (email?.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      email.classList.add("error");
      ok = false;
    }
    if (!ok) {
      showToast("请填写完整并确保邮箱格式正确。", "error");
      return;
    }
    showToast("感谢留言！当前为演示模式，消息未发送至服务器。", "success");
    form.reset();
  });
})();
