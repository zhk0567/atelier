(function () {
  "use strict";

  var root = document.querySelector("[data-quiz-root]");
  if (!root) return;

  var form = document.getElementById("nq-form");
  var intro = root.querySelector("[data-nq-intro]");
  var quiz = root.querySelector("[data-nq-quiz]");
  var slides = Array.prototype.slice.call(root.querySelectorAll("[data-nq-slide]"));
  var startButton = root.querySelector("[data-nq-start]");
  var backButton = root.querySelector("[data-nq-back]");
  var nextButton = root.querySelector("[data-nq-next]");
  var submitButton = root.querySelector("[data-nq-submit]");
  var errorBox = root.querySelector("[data-nq-error]");
  var introErrorBox = root.querySelector("[data-nq-intro-error]");
  var countBox = root.querySelector("[data-nq-count]");
  var answeredBox = root.querySelector("[data-nq-answered]");
  var remainingBox = root.querySelector("[data-nq-remaining]");
  var controlHint = root.querySelector("[data-nq-control-hint]");
  var progressBar = root.querySelector("[data-nq-progress-bar]");
  var durationInput = root.querySelector("[data-nq-duration]");
  var nameInput = form ? form.querySelector('input[name="name"]') : null;
  var identifierInput = form ? form.querySelector('input[name="identifier"]') : null;
  var consentInput = form ? form.querySelector('input[name="consent"]') : null;
  var consentCard = root.querySelector("[data-nq-consent-card]");
  var startedAt = 0;
  var current = 0;

  if (!form || !intro || !quiz || !slides.length) return;

  function selectedValue(slide) {
    var checked = slide.querySelector("input[type=radio]:checked");
    return checked ? checked.value : "";
  }

  function setError(message) {
    if (errorBox) errorBox.textContent = message || "";
  }

  function setIntroError(message) {
    if (!introErrorBox) return;
    introErrorBox.textContent = message || "";
    introErrorBox.hidden = !message;
  }

  function firstUnanswered() {
    for (var i = 0; i < slides.length; i += 1) {
      if (!selectedValue(slides[i])) return i;
    }
    return -1;
  }

  function answeredCount() {
    return slides.filter(function (slide) {
      return Boolean(selectedValue(slide));
    }).length;
  }

  function updateProgress() {
    var answered = answeredCount();
    var remaining = Math.max(0, slides.length - answered);
    if (answeredBox) answeredBox.textContent = String(answered);
    if (remainingBox) remainingBox.textContent = String(remaining);
    if (progressBar) {
      progressBar.style.width = (answered / slides.length) * 100 + "%";
    }
    if (consentCard && consentInput) {
      consentCard.classList.toggle("is-checked", consentInput.checked);
    }
  }

  function showSlide(index) {
    current = Math.max(0, Math.min(index, slides.length - 1));
    slides.forEach(function (slide, slideIndex) {
      slide.classList.toggle("is-active", slideIndex === current);
    });
    var slide = slides[current];
    if (countBox) countBox.textContent = String(current + 1);
    if (controlHint) {
      controlHint.textContent = selectedValue(slide) ? "这一题已记录" : "选一个最接近的答案";
    }
    quiz.classList.toggle("is-last", current === slides.length - 1);
    if (backButton) backButton.disabled = current === 0;
    setError("");
    updateProgress();
    var focusTarget = slide.querySelector("input[type=radio]");
    if (focusTarget) focusTarget.focus({ preventScroll: true });
    slide.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  function beginQuiz() {
    if (nameInput && !nameInput.value.trim()) {
      setIntroError("请先填写昵称或代号，再开始答题。");
      nameInput.focus();
      return;
    }
    if (identifierInput && !identifierInput.value.trim()) {
      setIntroError("请填写学号/查询码，用于之后找回自己的记录。");
      identifierInput.focus();
      return;
    }
    if (consentInput && !consentInput.checked) {
      setIntroError("请先阅读并同意《数据收集与隐私保护协议》，再开始答题。");
      consentInput.focus();
      return;
    }
    setIntroError("");
    startedAt = Date.now();
    intro.hidden = true;
    quiz.classList.remove("nq-quiz--waiting");
    var unanswered = firstUnanswered();
    showSlide(unanswered >= 0 ? unanswered : slides.length - 1);
    quiz.scrollIntoView({ block: "start", behavior: "smooth" });
  }

  if (startButton) startButton.addEventListener("click", beginQuiz);
  if (nameInput) {
    nameInput.addEventListener("input", function () {
      setIntroError("");
    });
    nameInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        beginQuiz();
      }
    });
  }
  if (consentInput) {
    consentInput.addEventListener("change", function () {
      setIntroError("");
      if (consentCard) consentCard.classList.toggle("is-checked", consentInput.checked);
    });
  }
  if (identifierInput) {
    identifierInput.addEventListener("input", function () {
      setIntroError("");
    });
  }

  slides.forEach(function (slide, index) {
    slide.querySelectorAll("input[type=radio]").forEach(function (input) {
      input.addEventListener("change", function () {
        setError("");
        if (controlHint) controlHint.textContent = "这一题已记录";
        updateProgress();
        if (index < slides.length - 1) {
          window.setTimeout(function () {
            if (current === index) showSlide(index + 1);
          }, 180);
        }
      });
    });
  });

  updateProgress();

  if (backButton) {
    backButton.addEventListener("click", function () {
      if (current > 0) showSlide(current - 1);
    });
  }

  if (nextButton) {
    nextButton.addEventListener("click", function () {
      if (!selectedValue(slides[current])) {
        setError("先选一个最接近的答案，再继续。");
        return;
      }
      if (current < slides.length - 1) showSlide(current + 1);
    });
  }

  form.addEventListener("submit", function (event) {
    var unanswered = firstUnanswered();
    if (unanswered >= 0) {
      event.preventDefault();
      showSlide(unanswered);
      setError("还有第 " + (unanswered + 1) + " 题没有作答。");
      return;
    }
    if (durationInput) {
      var elapsed = startedAt ? Math.round((Date.now() - startedAt) / 1000) : 0;
      durationInput.value = String(Math.max(0, elapsed));
    }
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "正在计算…";
    }
  });
})();
