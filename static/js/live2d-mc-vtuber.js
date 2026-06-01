/**
 * MC_Vtuber — bottom-right Live2D (pixi-live2d-display + Cubism 3).
 */
(function () {
  "use strict";

  var root = document.getElementById("live2d-mc-vtuber");
  if (!root || root.dataset.enabled !== "1") return;

  var modelUrl = root.dataset.modelUrl;
  var W = 360;
  var H = 460;
  var OFFSET_X = 75;
  var OFFSET_Y = 100;
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

  function showBlessingDialog() {
    var bubble = ensureBubble();
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

  function bindModelInteraction(model, canvas, app) {
    root._live2dModel = model;

    model.interactive = true;
    model.buttonMode = true;
    model.cursor = "pointer";

    model.on("hit", onCharacterTap);
    model.on("pointertap", onCharacterTap);

    if (app.renderer.plugins.interaction) {
      app.stage.interactive = true;
      app.stage.hitArea = new PIXI.Rectangle(0, 0, W, H);
    }
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

  /** 稳定可见：脚底锚点，略偏右下（配布画布人物不在几何中心） */
  function layoutModel(model) {
    var mw = model.width > 0 ? model.width : 1000;
    var mh = model.height > 0 ? model.height : 1000;
    var scale = Math.min(W / mw, H / mh) * 0.92;
    if (!isFinite(scale) || scale <= 0) {
      scale = 0.12;
    }
    model.scale.set(scale);
    model.anchor.set(0.5, 1);
    model.position.set(W * 0.58 + OFFSET_X, H - 6 + OFFSET_Y);
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

        document.addEventListener("visibilitychange", function () {
          if (!root._live2dApp) return;
          if (document.hidden) app.ticker.stop();
          else app.ticker.start();
        });
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
