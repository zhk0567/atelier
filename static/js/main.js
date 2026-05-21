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

    const applyWallpaper = (item) => {
      document.body.classList.add("has-wallpaper");
      if (item.is_video) {
        image.hidden = true;
        video.hidden = false;
        if (video.getAttribute("src") !== item.url) {
          video.setAttribute("src", item.url);
          const play = () => video.play().catch(() => {});
          if (video.readyState >= 2) play();
          else video.addEventListener("loadeddata", play, { once: true });
        } else if (video.paused) {
          video.play().catch(() => {});
        }
      } else {
        video.pause();
        video.hidden = true;
        image.hidden = false;
        image.src = item.url;
      }
    };

    const resolveId = () => {
      let stored = localStorage.getItem(WALLPAPER_STORAGE_KEY);
      if (stored === "random") stored = null;
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

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (reduceMotion.matches) {
      video.pause();
    }

    const syncVideoPlayback = () => {
      if (!video || video.hidden || reduceMotion.matches) return;
      if (document.hidden) {
        video.pause();
      } else if (video.getAttribute("src")) {
        video.play().catch(() => {});
      }
    };
    document.addEventListener("visibilitychange", syncVideoPlayback);
    syncVideoPlayback();

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

  const stored = localStorage.getItem("theme");
  if (stored) {
    html.setAttribute("data-theme", stored);
  } else {
    html.setAttribute("data-theme", "light");
  }

  const syncThemeToggleIcon = () => {
    document.querySelectorAll(".theme-toggle").forEach((btn) => {
      btn.textContent = html.getAttribute("data-theme") === "dark" ? "☀" : "☽";
    });
  };
  syncThemeToggleIcon();

  document.querySelectorAll(".theme-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
      html.setAttribute("data-theme", next);
      localStorage.setItem("theme", next);
      syncThemeToggleIcon();
    });
  });

  const sidebar = document.getElementById("wiki-sidebar");
  const backdrop = document.getElementById("wiki-sidebar-backdrop");
  const toggle = document.querySelector(".wiki-nav-toggle");

  const setSidebarOpen = (open) => {
    document.body.classList.toggle("sidebar-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (backdrop) backdrop.hidden = !open;
  };

  toggle?.addEventListener("click", () => {
    setSidebarOpen(!document.body.classList.contains("sidebar-open"));
  });
  backdrop?.addEventListener("click", () => setSidebarOpen(false));

  const path = window.location.pathname;
  document.querySelectorAll(".wiki-nav a[href]").forEach((link) => {
    const href = link.getAttribute("href");
    if (!href || href.startsWith("http") || href.startsWith("mailto:")) return;
    if (href === path || (href !== "/" && path.startsWith(href))) {
      link.classList.add("is-current");
    }
  });

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
