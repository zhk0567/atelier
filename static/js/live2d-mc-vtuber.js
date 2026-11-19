/**
 * MC_Vtuber — bottom-right Live2D (pixi-live2d-display + Cubism 3).
 */
(function () {
  "use strict";

  var root = document.getElementById("live2d-mc-vtuber");
  if (!root || root.dataset.enabled !== "1") return;

  var modelUrl = root.dataset.modelUrl;
  var DESKTOP = { W: 360, H: 460, anchorX: 0.58, footPad: 6, scale: 0.92 };
  var MOBILE = { W: 140, H: 178, anchorX: 0.56, footPad: 4, scale: 0.9 };
  var stage = DESKTOP;
  var W = stage.W;
  var H = stage.H;

  function fitStage(baseW, baseH, maxW, maxH) {
    var aspect = baseW / baseH;
    var w = Math.min(baseW, maxW);
    var h = Math.round(w / aspect);
    if (h > maxH) {
      h = Math.min(baseH, maxH);
      w = Math.round(h * aspect);
    }
    return { W: Math.max(96, w), H: Math.max(120, h) };
  }

  function readStageSize() {
    var narrow = window.matchMedia("(max-width: 640px)").matches;
    if (narrow) {
      var fitted = fitStage(
        MOBILE.W,
        MOBILE.H,
        Math.floor(window.innerWidth * 0.38),
        Math.floor(window.innerHeight * 0.28),
      );
      return {
        W: fitted.W,
        H: fitted.H,
        anchorX: MOBILE.anchorX,
        footPad: MOBILE.footPad,
        scale: MOBILE.scale,
      };
    }
    var desk = fitStage(
      DESKTOP.W,
      DESKTOP.H,
      Math.min(360, Math.floor(window.innerWidth * 0.42)),
      Math.min(460, Math.floor(window.innerHeight * 0.55)),
    );
    return {
      W: desk.W,
      H: desk.H,
      anchorX: DESKTOP.anchorX,
      footPad: DESKTOP.footPad,
      scale: DESKTOP.scale,
    };
  }

  function applyStageSize() {
    stage = readStageSize();
    W = stage.W;
    H = stage.H;
    // Keep CSS box === PIXI stage so canvas never stretches unevenly.
    root.style.width = W + "px";
    root.style.height = H + "px";
  }

  applyStageSize();
  var BLESSINGS = [
    "愿你今天心情晴朗，万事顺心～",
    "祝你学习进步，答啥都会！",
    "愿你所盼皆所成，所行皆坦途。",
    "今天也要好好照顾自己呀。",
    "好运正在向你跑来，请签收～",
    "愿你眼里有光，心里有暖。",
    "祝你身体健康，笑口常开！",
    "愿烦恼像乌云，太阳一晒就散了。",
    "你在认真生活，生活也会温柔待你。",
    "愿每次努力，都有值得的回报。",
    "祝你周末愉快，睡个好觉！",
    "愿你的代码无 bug，编译一次过～",
    "今天适合喝奶茶，也适合收获小确幸。",
    "愿你被世界温柔以待，也向人间散发善意。",
    "愿考试顺利，发挥超常！",
    "愿你与人相遇皆善意，与事相争皆从容。",
    "愿你在方块世界里，建起属于自己的童话。",
    "愿你平安喜乐，不负韶华。",
    "祝你心想事成，好事连连！",
    "愿温柔与勇气，常伴你左右。",
  ];
  var bubbleEl = null;
  var bubbleTimer = null;
  var RULER_SIZE = 22;
  var TICK_STEP = 20;
  var LABEL_EVERY = 100;

  function randomBlessing() {
    return BLESSINGS[Math.floor(Math.random() * BLESSINGS.length)];
  }

  function ensureBubble() {
    if (bubbleEl) return bubbleEl;
    bubbleEl = document.createElement("div");
    bubbleEl.className = "live2d-mc-vtuber__bubble";
    bubbleEl.setAttribute("role", "status");
    bubbleEl.setAttribute("aria-live", "polite");
    bubbleEl.hidden = true;
    root.appendChild(bubbleEl);
    return bubbleEl;
  }

  function syncHitAndBubble(model) {
    if (!model) return;
    var hit = ensureHitTarget();
    var bounds = null;
    try {
      bounds = model.getBounds(true);
    } catch (e) {
      bounds = null;
    }
    if (!bounds || !isFinite(bounds.width) || bounds.width < 8) {
      return;
    }

    var padX = Math.max(6, W * 0.03);
    var padY = Math.max(8, H * 0.02);
    var left = Math.max(0, bounds.x - padX);
    var top = Math.max(0, bounds.y - padY);
    var right = Math.min(W, bounds.x + bounds.width + padX);
    var bottom = Math.min(H, bounds.y + bounds.height + padY);
    var width = Math.max(36, right - left);
    var height = Math.max(48, bottom - top);

    hit.style.left = (left / W) * 100 + "%";
    hit.style.top = (top / H) * 100 + "%";
    hit.style.width = (width / W) * 100 + "%";
    hit.style.height = (height / H) * 100 + "%";
    hit.style.right = "auto";
    hit.style.bottom = "auto";

    var bubble = ensureBubble();
    var headX = bounds.x + bounds.width * 0.5;
    var headTop = Math.max(0, bounds.y);
    var bubbleMax = Math.min(220, window.innerWidth * 0.64, W * 1.45);
    var bubbleLeft = Math.min(Math.max(headX - bubbleMax * 0.35, -W * 0.55), W * 0.08);
    bubble.style.left = bubbleLeft + "px";
    bubble.style.right = "auto";
    bubble.style.bottom = H - headTop + 10 + "px";
    bubble.style.maxWidth = bubbleMax + "px";
    var tailX = Math.max(14, Math.min(bubbleMax - 24, headX - bubbleLeft - 5));
    bubble.style.setProperty("--bubble-tail-x", tailX + "px");
  }

  function showBlessingDialog() {
    var bubble = ensureBubble();
    if (root._live2dModel) syncHitAndBubble(root._live2dModel);
    bubble.textContent = randomBlessing();
    bubble.hidden = false;
    bubble.classList.add("is-visible");
    clearTimeout(bubbleTimer);
    bubbleTimer = setTimeout(function () {
      bubble.classList.remove("is-visible");
      window.setTimeout(function () {
        if (!bubble.classList.contains("is-visible")) {
          bubble.hidden = true;
        }
      }, 280);
    }, 5000);
  }

  var lastTapAt = 0;

  function onCharacterTap() {
    var now = Date.now();
    if (now - lastTapAt < 350) return;
    lastTapAt = now;
    showBlessingDialog();
  }

  function ensureHitTarget() {
    var hit = root.querySelector(".live2d-mc-vtuber__hit");
    if (hit) return hit;
    hit = document.createElement("button");
    hit.type = "button";
    hit.className = "live2d-mc-vtuber__hit";
    hit.setAttribute("aria-label", "与看板娘互动");
    root.appendChild(hit);
    return hit;
  }

  function bindModelInteraction(model, canvas, app) {
    root._live2dModel = model;

    // Avoid full-canvas hit stealing scroll/clicks; use compact CSS hit button.
    model.interactive = false;
    model.buttonMode = false;
    if (app.renderer.plugins.interaction) {
      app.stage.interactive = false;
      app.stage.hitArea = null;
    }

    var hit = ensureHitTarget();
    hit.addEventListener("click", onCharacterTap);
    hit.addEventListener(
      "touchend",
      function (event) {
        event.preventDefault();
        onCharacterTap();
      },
      { passive: false },
    );
  }

  function isDebugRulers() {
    if (root.dataset.debugRulers === "1") return true;
    if (root.dataset.debugRulers === "0") return false;
    try {
      if (localStorage.getItem("live2d_debug") === "1") return true;
      if (localStorage.getItem("live2d_debug") === "0") return false;
      return new URLSearchParams(window.location.search).has("live2d_debug");
    } catch (e) {
      return false;
    }
  }

  function buildRuler(axis, length) {
    var el = document.createElement("div");
    el.className =
      "live2d-mc-vtuber__ruler live2d-mc-vtuber__ruler--" + axis;
    el.setAttribute("aria-hidden", "true");

    for (var px = 0; px <= length; px += TICK_STEP) {
      var tick = document.createElement("span");
      tick.className = "live2d-mc-vtuber__tick";
      var pct = (px / length) * 100;
      if (axis === "x") {
        tick.style.left = pct + "%";
      } else {
        tick.style.top = pct + "%";
      }
      if (px % LABEL_EVERY === 0) {
        tick.classList.add("live2d-mc-vtuber__tick--label");
        tick.textContent = String(px);
      }
      el.appendChild(tick);
    }
    return el;
  }

  function setupDomDebugChrome() {
    if (!isDebugRulers()) return;

    root.classList.add("is-debug");
    root.setAttribute("data-stage-w", String(W));
    root.setAttribute("data-stage-h", String(H));

    var stageFrame = document.createElement("div");
    stageFrame.className = "live2d-mc-vtuber__stage-frame";
    stageFrame.setAttribute("aria-hidden", "true");

    var stageLabel = document.createElement("div");
    stageLabel.className = "live2d-mc-vtuber__stage-label";
    stageLabel.textContent = "canvas " + W + "×" + H;

    var modelLabel = document.createElement("div");
    modelLabel.className = "live2d-mc-vtuber__model-label";
    modelLabel.id = "live2d-mc-vtuber-model-label";
    modelLabel.textContent = "model bounds —";

    root.appendChild(buildRuler("x", W));
    root.appendChild(buildRuler("y", H));
    root.appendChild(stageFrame);
    root.appendChild(stageLabel);
    root.appendChild(modelLabel);
  }

  function setupPixiDebugOverlay(app, model) {
    var stageGfx = new PIXI.Graphics();
    stageGfx.name = "debug-stage-box";
    var boundsGfx = new PIXI.Graphics();
    boundsGfx.name = "debug-model-bounds";
    var localGfx = new PIXI.Graphics();
    localGfx.name = "debug-model-local";

    app.stage.addChildAt(stageGfx, 0);
    app.stage.addChild(boundsGfx);
    model.addChildAt(localGfx, 0);

    function redraw() {
      stageGfx.clear();
      stageGfx.lineStyle(2, 0xe53935, 1);
      stageGfx.drawRect(0.5, 0.5, W - 1, H - 1);

      boundsGfx.clear();
      localGfx.clear();
      boundsGfx.interactive = false;
      stageGfx.interactive = false;

      if (!model || model.destroyed) return;

      if (typeof model.getBounds === "function") {
        var b = model.getBounds();
        boundsGfx.lineStyle(2, 0x00c853, 0.95);
        boundsGfx.drawRect(b.x, b.y, b.width, b.height);

        var label = document.getElementById("live2d-mc-vtuber-model-label");
        if (label) {
          label.textContent =
            "bounds x:" +
            Math.round(b.x) +
            " y:" +
            Math.round(b.y) +
            " " +
            Math.round(b.width) +
            "×" +
            Math.round(b.height) +
            " | cubism " +
            Math.round(model.width) +
            "×" +
            Math.round(model.height);
        }
      }

      if (typeof model.getLocalBounds === "function") {
        var lb = model.getLocalBounds();
        if (lb.width > 0 && lb.height > 0) {
          localGfx.lineStyle(2, 0x1e88e5, 0.9);
          localGfx.drawRect(lb.x, lb.y, lb.width, lb.height);
        }
      }
    }

    app.ticker.add(redraw);
    redraw();
    return redraw;
  }

  /** 关闭左右手装备贴图（texture_01/02） */
  var HAND_EQUIP_PARAMS = ["kiri_biaoqing2", "kiri_biaoqing3"];

  function hideHandEquipment(model) {
    var core = model.internalModel;
    if (!core || !core.coreModel || !core.coreModel.setParameterValueById) {
      return;
    }
    for (var i = 0; i < HAND_EQUIP_PARAMS.length; i++) {
      core.coreModel.setParameterValueById(HAND_EQUIP_PARAMS[i], 0);
    }
  }

  /** 脚底锚点站在画布内；不再额外 OFFSET，避免人物偏出 hit 区 */
  function layoutModel(model) {
    var mw = model.width > 0 ? model.width : 1000;
    var mh = model.height > 0 ? model.height : 1000;
    var scale = Math.min(W / mw, H / mh) * (stage.scale || 0.92);
    if (!isFinite(scale) || scale <= 0) {
      scale = 0.12;
    }
    model.scale.set(scale);
    model.anchor.set(0.5, 1);
    model.position.set(W * (stage.anchorX || 0.56), H - (stage.footPad || 4));
    syncHitAndBubble(model);
  }

  function boot() {
    var PIXI = window.PIXI;
    var Live2DModel = PIXI && PIXI.live2d && PIXI.live2d.Live2DModel;
    if (!Live2DModel) {
      console.error("[live2d] 缺少运行时，请执行 python scripts\\ensure_live2d_vendor.py");
      return;
    }

    if (typeof Live2DModel.registerTicker === "function") {
      Live2DModel.registerTicker(PIXI.Ticker);
    }

    applyStageSize();
    setupDomDebugChrome();

    var canvas = document.createElement("canvas");
    canvas.className = "live2d-mc-vtuber__canvas";
    var app;
    try {
      app = new PIXI.Application({
        view: canvas,
        width: W,
        height: H,
        backgroundAlpha: 0,
        antialias: true,
        resolution: Math.min(window.devicePixelRatio || 1, 2),
        autoDensity: true,
        autoStart: true,
      });
    } catch (err) {
      console.error("[live2d] PIXI 初始化失败", err);
      return;
    }

    root.appendChild(canvas);
    ensureHitTarget();

    if (isDebugRulers()) {
      app.renderer.backgroundColor = 0x101018;
      app.renderer.backgroundAlpha = 0.06;
    }

    var redrawDebug = null;

    Live2DModel.from(modelUrl, { autoInteract: true })
      .then(function (model) {
        model.autoInteract = false;
        layoutModel(model);
        hideHandEquipment(model);
        if (isDebugRulers()) {
          redrawDebug = setupPixiDebugOverlay(app, model);
        }
        app.stage.addChild(model);
        if (redrawDebug) redrawDebug();

        bindModelInteraction(model, canvas, app);
        root.classList.add("is-ready");
        // Bounds settle after first frames of Live2D update
        window.setTimeout(function () {
          syncHitAndBubble(model);
        }, 120);
        window.setTimeout(function () {
          syncHitAndBubble(model);
        }, 600);

        document.addEventListener("visibilitychange", function () {
          if (!root._live2dApp) return;
          if (document.hidden) app.ticker.stop();
          else app.ticker.start();
        });

        var resizeTimer = 0;
        var onStageChange = function () {
          applyStageSize();
          try {
            app.renderer.resize(W, H);
          } catch (e) {
            /* ignore */
          }
          layoutModel(model);
          if (redrawDebug) redrawDebug();
          syncHitAndBubble(model);
        };
        var onResize = function () {
          window.clearTimeout(resizeTimer);
          resizeTimer = window.setTimeout(onStageChange, 120);
        };
        var mq = window.matchMedia("(max-width: 640px)");
        if (typeof mq.addEventListener === "function") mq.addEventListener("change", onStageChange);
        else if (typeof mq.addListener === "function") mq.addListener(onStageChange);
        window.addEventListener("resize", onResize);

        root._live2dApp = app;
      })
      .catch(function (err) {
        console.error("[live2d] 模型加载失败", err);
        if (canvas.parentNode === root) {
          root.removeChild(canvas);
        }
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
