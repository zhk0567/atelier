/* /personal — task filters, local "already delivered" state, decade countdown */
(function () {
  "use strict";

  var STORAGE_KEY = "atelier.personal.tasks.v1";

  function readDone() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed.filter(function (id) { return typeof id === "string"; }) : [];
    } catch (err) {
      return [];
    }
  }

  function writeDone(ids) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
    } catch (err) {
      /* private mode / quota — the page still works without persistence */
    }
  }

  function initTasks() {
    var list = document.querySelector("[data-personal-tasks]");
    if (!list) {
      return;
    }
    var tasks = Array.prototype.slice.call(list.querySelectorAll(".personal-task"));
    if (!tasks.length) {
      return;
    }

    var done = readDone();
    var progressNode = document.querySelector("[data-personal-progress]");
    var progressBar = document.querySelector("[data-personal-progressbar]");
    var progressFill = document.querySelector("[data-personal-progress-fill]");
    var emptyNode = document.querySelector("[data-personal-empty]");

    function syncProgress() {
      var checked = tasks.filter(function (task) {
        var input = task.querySelector("[data-task-check]");
        return input && input.checked;
      }).length;
      var total = tasks.length;
      var percent = total ? Math.round((checked / total) * 100) : 0;
      if (progressNode) {
        progressNode.textContent = String(checked);
      }
      if (progressBar) {
        progressBar.setAttribute("aria-valuenow", String(checked));
      }
      if (progressFill) {
        progressFill.style.width = percent + "%";
      }
    }

    tasks.forEach(function (task) {
      var input = task.querySelector("[data-task-check]");
      if (!input) {
        return;
      }
      var id = task.getAttribute("data-task-id") || "";
      if (done.indexOf(id) !== -1) {
        input.checked = true;
        task.classList.add("is-done");
      }
      input.addEventListener("change", function () {
        task.classList.toggle("is-done", input.checked);
        var current = readDone();
        var index = current.indexOf(id);
        if (input.checked && index === -1) {
          current.push(id);
        } else if (!input.checked && index !== -1) {
          current.splice(index, 1);
        }
        writeDone(current);
        syncProgress();
      });
    });

    var filters = document.querySelector("[data-personal-filters]");
    if (filters) {
      filters.hidden = false;
      var buttons = Array.prototype.slice.call(filters.querySelectorAll("[data-filter]"));
      buttons.forEach(function (button) {
        button.addEventListener("click", function () {
          var wanted = button.getAttribute("data-filter") || "all";
          buttons.forEach(function (other) {
            var active = other === button;
            other.classList.toggle("is-active", active);
            other.setAttribute("aria-pressed", active ? "true" : "false");
          });
          var visible = 0;
          tasks.forEach(function (task) {
            var show = wanted === "all" || task.getAttribute("data-category") === wanted;
            task.classList.toggle("is-filtered", !show);
            if (show) {
              visible += 1;
            }
          });
          if (emptyNode) {
            emptyNode.hidden = visible !== 0;
          }
        });
      });
    }

    syncProgress();
  }

  function initCountdown() {
    var root = document.querySelector("[data-personal-countdown]");
    if (!root) {
      return;
    }
    var output = root.querySelector("[data-personal-countdown-days]");
    var deadline = root.getAttribute("data-deadline") || "";
    if (!output || !deadline) {
      return;
    }
    var target = Date.parse(deadline + "T00:00:00+08:00");
    if (Number.isNaN(target)) {
      return;
    }

    function tick() {
      var days = Math.ceil((target - Date.now()) / 86400000);
      if (days <= 0) {
        output.textContent = "到站";
        root.classList.add("is-due");
        return;
      }
      output.textContent = days.toLocaleString("zh-CN");
    }

    tick();
    window.setInterval(tick, 60000);
  }

  function boot() {
    initTasks();
    initCountdown();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
