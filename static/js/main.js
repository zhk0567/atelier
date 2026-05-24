(function () {
  "use strict";

  const html = document.documentElement;
  const WALLPAPER_STORAGE_KEY = "wallpaper-mode";

  const prefersReducedMotion = () =>
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function initWallpaper() {
    const dataEl = document.getElementById("wiki-wallpapers-data");
    const image = document.getElementById("wiki-wallpaper-image");
    const select = document.getElementById("wallpaper-select");
    if (!dataEl || !image) return;

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
      "wp-0": "chunze-2",
      "wp-1": "chunze-1",
      "wp-2": "chunze-3",
      "wp-3": "chunze-4",
      "wallpaper-01-preview": "chunze-1",
      "wallpaper-02-preview-alt": "chunze-2",
      "wallpaper-03-minecraft": "chunze-3",
      "wallpaper-04-cloud-pixel": "chunze-4",
      "春泽_1_original": "chunze-1",
      "春泽_2_original": "chunze-2",
      "春泽_3_original": "chunze-3",
      "春泽_4_original": "chunze-4",
      "春泽_5_original": "chunze-5",
      "春泽_6_original": "chunze-6",
      "栖野_1_original": "qiye-1",
      "栖野_3_original": "qiye-3",
      "栖野_4_original": "qiye-4",
      "栖野_6_original": "qiye-6",
      "渊光_1_original": "yuanguang-1",
      "渊光_2_original": "yuanguang-2",
      "渊光_3_original": "yuanguang-3",
      "渊光_4_original": "yuanguang-4",
      "渊光_5_original": "yuanguang-5",
      "渊光_6_original": "yuanguang-6",
    };

    const wallpaperUrl = (item) => {
      const raw = item.preview_url || item.url;
      return new URL(raw, window.location.href).href;
    };

    const imageShows = (url) => {
      if (!image.src) return false;
      try {
        return (
          new URL(image.src, window.location.href).pathname ===
          new URL(url, window.location.href).pathname
        );
      } catch {
        return false;
      }
    };

    const onImageOk = () => html.classList.remove("wallpaper-img-failed");
    const onImageFail = () => html.classList.add("wallpaper-img-failed");

    image.addEventListener("load", onImageOk);
    image.addEventListener("error", onImageFail);

    let wallpaperHasShown = false;

    const applyWallpaper = (item) => {
      if (!item || !(item.preview_url || item.url)) return;
      document.body.classList.add("has-wallpaper");
      html.classList.add("wallpaper-enabled");
      const url = wallpaperUrl(item);
      if (imageShows(url)) {
        if (image.complete && image.naturalWidth > 0) onImageOk();
        return;
      }

      const reveal = () => {
        image.classList.remove("is-fading");
        wallpaperHasShown = true;
        if (image.complete && image.naturalWidth > 0) onImageOk();
      };

      const assignSrc = () => {
        image.src = url;
        if (image.complete && image.naturalWidth > 0) {
          reveal();
          return;
        }
        const onReveal = () => {
          image.removeEventListener("load", onReveal);
          image.removeEventListener("error", onReveal);
          reveal();
        };
        image.addEventListener("load", onReveal);
        image.addEventListener("error", onReveal);
      };

      if (prefersReducedMotion() || !wallpaperHasShown) {
        assignSrc();
        return;
      }

      image.classList.add("is-fading");
      const preload = new Image();
      preload.onload = assignSrc;
      preload.onerror = assignSrc;
      preload.src = url;
    };

    const resolveId = () => {
      let stored = localStorage.getItem(WALLPAPER_STORAGE_KEY);
      if (stored === "random" || stored === "none") stored = null;
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

    applyWallpaper(resolveWallpaper());

    if (select) {
      select.value = resolveId();
      select.addEventListener("change", () => {
        const next = select.value;
        localStorage.setItem(WALLPAPER_STORAGE_KEY, next);
        const item = wallpapers.find((w) => w.id === next);
        if (item) applyWallpaper(item);
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
      if (!prefersReducedMotion()) {
        html.classList.add("theme-transitioning");
        window.setTimeout(() => html.classList.remove("theme-transitioning"), 220);
      }
      applyTheme(next);
    });
  });

  function initUiReady() {
    if (prefersReducedMotion()) {
      document.body.classList.add("is-ui-ready");
      return;
    }
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        document.body.classList.add("is-ui-ready");
      });
    });
  }

  function initHeaderScroll() {
    const header = document.querySelector(".wiki-header");
    if (!header) return;
    const onScroll = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  initUiReady();
  initHeaderScroll();

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
    const counterEl = document.getElementById("wiki-lightbox-counter");
    const closeBtn = document.getElementById("wiki-lightbox-close");
    const prevBtn = document.getElementById("wiki-lightbox-prev");
    const nextBtn = document.getElementById("wiki-lightbox-next");
    if (!overlay || !imgEl) return;

    let slides = [];
    let index = 0;
    let touchStartX = 0;
    let touchStartY = 0;
    let touchTracking = false;

    const isOpen = () => overlay.classList.contains("is-open");

    const slideUrl = (thumb) => {
      const raw =
        thumb.getAttribute("data-full-src") ||
        thumb.getAttribute("src") ||
        thumb.currentSrc ||
        thumb.src ||
        "";
      try {
        return new URL(raw, window.location.href).href;
      } catch {
        return raw;
      }
    };

    const buildSlides = (gallery) =>
      Array.from(gallery.querySelectorAll(".wiki-gallery__item img")).map((thumb) => {
        const item = thumb.closest(".wiki-gallery__item");
        return {
          src: slideUrl(thumb),
          alt: thumb.getAttribute("alt") || "",
          meta: item?.dataset.meta || "",
        };
      });

    const updateChrome = () => {
      const multi = slides.length > 1;
      if (prevBtn) prevBtn.hidden = !multi;
      if (nextBtn) nextBtn.hidden = !multi;
      if (counterEl) {
        counterEl.hidden = !multi;
        counterEl.textContent = multi ? `${index + 1} / ${slides.length}` : "";
      }
    };

    const show = (nextIndex) => {
      if (!slides.length) return;
      index = (nextIndex + slides.length) % slides.length;
      const slide = slides[index];
      const nextSrc = slide.src;
      if (imgEl.src !== nextSrc) {
        imgEl.src = nextSrc;
      } else {
        imgEl.removeAttribute("src");
        imgEl.src = nextSrc;
      }
      imgEl.alt = slide.alt;
      if (captionEl) {
        const parts = [slide.alt, slide.meta].filter(Boolean);
        captionEl.textContent = parts.join(" · ");
        captionEl.hidden = !parts.length;
      }
      updateChrome();
    };

    const step = (delta) => {
      if (slides.length < 2) return;
      show(index + delta);
    };

    const openAt = (gallery, startIndex) => {
      slides = buildSlides(gallery);
      if (!slides.length) return;
      overlay.hidden = false;
      overlay.classList.add("is-open");
      show(startIndex);
      document.body.style.overflow = "hidden";
      closeBtn?.focus();
    };

    const close = () => {
      overlay.classList.remove("is-open");
      overlay.hidden = true;
      slides = [];
      index = 0;
      touchTracking = false;
      imgEl.removeAttribute("src");
      if (captionEl) {
        captionEl.textContent = "";
        captionEl.hidden = true;
      }
      if (counterEl) {
        counterEl.textContent = "";
        counterEl.hidden = true;
      }
      if (prevBtn) prevBtn.hidden = true;
      if (nextBtn) nextBtn.hidden = true;
      document.body.style.overflow = "";
    };

    const onSwipeEnd = (dx, dy) => {
      if (!isOpen() || slides.length < 2) return;
      if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy)) return;
      if (dx < 0) step(1);
      else step(-1);
    };

    document.querySelectorAll("[data-gallery]").forEach((gallery) => {
      gallery.querySelectorAll(".wiki-gallery__item img").forEach((thumb, i) => {
        thumb.style.cursor = "pointer";
        thumb.addEventListener("click", (e) => {
          e.preventDefault();
          openAt(gallery, i);
        });
      });
    });

    closeBtn?.addEventListener("click", (e) => {
      e.stopPropagation();
      close();
    });
    prevBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      step(-1);
    });
    nextBtn?.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      step(1);
    });
    imgEl.addEventListener("click", (e) => e.stopPropagation());
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) close();
    });

    overlay.addEventListener(
      "touchstart",
      (e) => {
        if (!isOpen() || slides.length < 2) return;
        if (!e.touches.length) return;
        const t = e.touches[0];
        touchStartX = t.clientX;
        touchStartY = t.clientY;
        touchTracking = true;
      },
      { passive: true }
    );
    overlay.addEventListener(
      "touchmove",
      (e) => {
        if (!touchTracking || !isOpen()) return;
        if (!e.touches.length) return;
        const t = e.touches[0];
        const dx = t.clientX - touchStartX;
        const dy = t.clientY - touchStartY;
        if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 8) {
          e.preventDefault();
        }
      },
      { passive: false }
    );
    overlay.addEventListener(
      "touchend",
      (e) => {
        if (!touchTracking) return;
        touchTracking = false;
        const t = e.changedTouches[0];
        if (!t) return;
        onSwipeEnd(t.clientX - touchStartX, t.clientY - touchStartY);
      },
      { passive: true }
    );
    overlay.addEventListener(
      "touchcancel",
      () => {
        touchTracking = false;
      },
      { passive: true }
    );

    overlay.addEventListener("pointerdown", (e) => {
      if (!isOpen() || slides.length < 2 || e.pointerType === "touch") return;
      if (e.target.closest(".wiki-lightbox__nav, .wiki-lightbox__close")) return;
      touchStartX = e.clientX;
      touchStartY = e.clientY;
      touchTracking = true;
    });
    overlay.addEventListener("pointerup", (e) => {
      if (!touchTracking || e.pointerType === "touch") return;
      touchTracking = false;
      if (e.target.closest(".wiki-lightbox__nav, .wiki-lightbox__close")) return;
      onSwipeEnd(e.clientX - touchStartX, e.clientY - touchStartY);
    });

    document.addEventListener("keydown", (e) => {
      if (!isOpen()) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") {
        e.preventDefault();
        step(-1);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        step(1);
      }
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
