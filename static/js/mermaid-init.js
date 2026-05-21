(function () {
  "use strict";

  function themeName() {
    return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "default";
  }

  function runMermaid() {
    if (typeof mermaid === "undefined") return;
    var nodes = document.querySelectorAll(".wiki-md pre.mermaid, .blog-md pre.mermaid");
    if (!nodes.length) return;

    mermaid.initialize({
      startOnLoad: false,
      theme: themeName(),
      securityLevel: "loose",
      flowchart: { useMaxWidth: true, htmlLabels: true },
    });

    nodes.forEach(function (node) {
      node.removeAttribute("data-processed");
    });
    mermaid.run({ nodes: nodes }).catch(function () {});
  }

  function schedule() {
    if (typeof mermaid === "undefined") return;
    requestAnimationFrame(runMermaid);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", schedule);
  } else {
    schedule();
  }

  document.querySelectorAll(".theme-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      setTimeout(schedule, 120);
    });
  });
})();
