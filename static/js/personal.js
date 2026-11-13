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

  function initWish() {
    var modal = document.querySelector("[data-wish-modal]");
    var opener = document.querySelector("[data-wish-open]");
    if (!modal || !opener) {
      return;
    }
    var panel = modal.querySelector(".personal-wish-modal__panel");
    var form = modal.querySelector("[data-wish-form]");
    var status = modal.querySelector("[data-wish-status]");
    var submit = modal.querySelector("[data-wish-submit]");
    var closeButtons = Array.prototype.slice.call(modal.querySelectorAll("[data-wish-close]"));
    var lastFocus = null;
    var sending = false;

    function setStatus(message, isError) {
      if (!status) {
        return;
      }
      status.hidden = !message;
      status.textContent = message || "";
      status.classList.toggle("is-error", Boolean(isError));
    }

    function focusables() {
      return Array.prototype.slice
        .call(
          panel.querySelectorAll(
            "a[href], button:not([disabled]), input:not([tabindex='-1']), textarea, select"
          )
        )
        .filter(function (node) {
          return node.offsetParent !== null;
        });
    }

    function open() {
      if (!modal.hidden) {
        return;
      }
      lastFocus = document.activeElement;
      modal.hidden = false;
      document.body.classList.add("personal-wish-open");
      var first = modal.querySelector("#wish-modal-name") || modal.querySelector("textarea");
      if (first) {
        window.setTimeout(function () {
          first.focus();
        }, 30);
      }
    }

    function close() {
      if (modal.hidden) {
        return;
      }
      modal.hidden = true;
      document.body.classList.remove("personal-wish-open");
      if (lastFocus && typeof lastFocus.focus === "function") {
        lastFocus.focus();
      }
      window.setTimeout(function () {
        if (form && form.classList.contains("is-sent")) {
          form.reset();
          form.classList.remove("is-sent");
          if (submit) {
            submit.hidden = false;
            submit.disabled = false;
          }
          var closeLabel = modal.querySelector(".personal-wish-form__back");
          if (closeLabel) {
            closeLabel.textContent = "先不写";
          }
          setStatus("", false);
        }
      }, 180);
    }

    opener.addEventListener("click", function (event) {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }
      event.preventDefault();
      open();
    });

    closeButtons.forEach(function (button) {
      button.addEventListener("click", close);
    });

    // The fixed backdrop is clipped by the article's backdrop-filter containing
    // block, so also treat clicks anywhere outside the panel as "close".
    document.addEventListener("click", function (event) {
      if (
        modal.hidden ||
        !panel ||
        panel.contains(event.target) ||
        (opener && opener.contains(event.target))
      ) {
        return;
      }
      close();
    });

    modal.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        event.preventDefault();
        close();
        return;
      }
      if (event.key !== "Tab" || !panel) {
        return;
      }
      var nodes = focusables();
      if (!nodes.length) {
        return;
      }
      var first = nodes[0];
      var last = nodes[nodes.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    if (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        if (sending) {
          return;
        }
        var text = form.querySelector("textarea[name='wish']");
        var value = text ? text.value.trim() : "";
        if (value.length < 2) {
          setStatus("至少写 2 个字吧。", true);
          if (text) {
            text.focus();
          }
          return;
        }
        sending = true;
        if (submit) {
          submit.disabled = true;
        }
        setStatus("正在提交…", false);

        window
          .fetch(form.getAttribute("action") || "/personal/wish", {
            method: "POST",
            body: new FormData(form),
            headers: { Accept: "application/json" },
            credentials: "same-origin",
          })
          .then(function (response) {
            return response
              .json()
              .catch(function () {
                return { ok: false, error: "服务器返回了看不懂的东西，稍后再试。" };
              })
              .then(function (payload) {
                return { ok: response.ok, payload: payload };
              });
          })
          .then(function (result) {
            var payload = result.payload || {};
            if (result.ok && payload.ok) {
              form.classList.add("is-sent");
              if (submit) {
                submit.hidden = true;
              }
              var closeLabel = modal.querySelector(".personal-wish-form__back");
              if (closeLabel) {
                closeLabel.textContent = "关闭";
              }
              setStatus(payload.message || "收到了。审核通过后，它会出现在页面最下面。", false);
              var toast = document.getElementById("toast");
              if (toast) {
                toast.textContent = "愿望已提交，等待审核。";
                toast.className = "toast show";
                window.setTimeout(function () {
                  toast.className = "toast";
                }, 2600);
              }
              return;
            }
            setStatus(payload.error || "没提交成功，稍后再试一次。", true);
          })
          .catch(function () {
            setStatus("网络好像断了，稍后再试一次。", true);
          })
          .finally(function () {
            sending = false;
            if (submit && !form.classList.contains("is-sent")) {
              submit.disabled = false;
            }
          });
      });
    }
  }

  function boot() {
    initTasks();
    initCountdown();
    initWish();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
