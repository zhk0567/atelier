/**
 * Lazy-load pyecharts HTML into same-origin iframes on blog post pages.
 * Limits concurrent active charts and unloads off-screen / hidden tabs.
 */
(function () {
  "use strict";

  var MAX_ACTIVE = 2;
  var ROOT_MARGIN = "100px 0px";
  var UNLOAD_DELAY_MS = 600;

  var embeds = Array.prototype.slice.call(
    document.querySelectorAll(".pyecharts-embed[data-src]")
  );
  if (!embeds.length) return;

  var active = new Set();

  function heightPx(el) {
    var h = el.getAttribute("data-height") || "340";
    return /^\d+$/.test(h) ? h + "px" : h;
  }

  function unloadEmbed(el) {
    var iframe = el.querySelector("iframe.pyecharts-embed__frame");
    if (iframe) {
      iframe.src = "about:blank";
      iframe.remove();
    }
    el.classList.remove("is-active", "is-loaded");
    active.delete(el);
    var ph = el.querySelector(".pyecharts-embed__placeholder");
    if (ph) ph.hidden = false;
  }

  function releaseSlot() {
    if (active.size < MAX_ACTIVE) return;
    var oldest = active.values().next().value;
    if (oldest) unloadEmbed(oldest);
  }

  function loadEmbed(el) {
    if (el.classList.contains("is-active")) return;
    releaseSlot();

    var src = el.getAttribute("data-src");
    if (!src) return;

    var h = heightPx(el);
    el.style.minHeight = h;

    var iframe = document.createElement("iframe");
    iframe.className = "pyecharts-embed__frame";
    iframe.title = el.getAttribute("aria-label") || "交互图表";
    iframe.loading = "lazy";
    iframe.setAttribute("importance", "low");
    /* Same-origin chart pages; no sandbox — avoids CSP/sandbox quirks with ECharts. */
    iframe.style.height = h;
    iframe.src = src;

    var ph = el.querySelector(".pyecharts-embed__placeholder");
    if (ph) ph.hidden = true;

    el.appendChild(iframe);
    el.classList.add("is-active", "is-loaded");
    active.add(el);
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        var el = entry.target;
        if (entry.isIntersecting && entry.intersectionRatio > 0.08) {
          if (el._unloadTimer) {
            clearTimeout(el._unloadTimer);
            el._unloadTimer = null;
          }
          loadEmbed(el);
        } else if (!entry.isIntersecting) {
          el._unloadTimer = setTimeout(function () {
            unloadEmbed(el);
            el._unloadTimer = null;
          }, UNLOAD_DELAY_MS);
        }
      });
    },
    { rootMargin: ROOT_MARGIN, threshold: [0, 0.08, 0.25] }
  );

  embeds.forEach(function (el) {
    el.style.minHeight = heightPx(el);
    observer.observe(el);
  });

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
      active.forEach(function (el) {
        unloadEmbed(el);
      });
    }
  });
})();
