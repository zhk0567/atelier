(function () {
  var input = document.getElementById("blog-search-input");
  var resultsEl = document.getElementById("blog-search-results");
  if (!input || !resultsEl) return;

  var index = [];
  var ready = fetch("/static/blog/search-index.json", { credentials: "same-origin" })
    .then(function (r) {
      if (!r.ok) throw new Error("index");
      return r.json();
    })
    .then(function (data) {
      index = Array.isArray(data) ? data : [];
    })
    .catch(function () {
      index = [];
    });

  function normalize(s) {
    return (s || "").toLowerCase();
  }

  function score(item, q) {
    var title = normalize(item.title);
    var summary = normalize(item.summary);
    var category = normalize(item.category);
    var slug = normalize(item.slug);
    if (title.indexOf(q) !== -1) return 4;
    if (slug.indexOf(q) !== -1) return 3;
    if (category.indexOf(q) !== -1) return 2;
    if (summary.indexOf(q) !== -1) return 1;
    return 0;
  }

  function render(matches) {
    resultsEl.innerHTML = "";
    if (!matches.length) {
      resultsEl.hidden = true;
      return;
    }
    var ul = document.createElement("ul");
    ul.className = "blog-search-results__list";
    matches.slice(0, 12).forEach(function (item) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = item.url;
      a.textContent = item.title;
      li.appendChild(a);
      if (item.category || item.series) {
        var meta = document.createElement("span");
        meta.className = "blog-search-results__meta";
        meta.textContent = [item.category, item.series].filter(Boolean).join(" · ");
        li.appendChild(meta);
      }
      ul.appendChild(li);
    });
    resultsEl.appendChild(ul);
    resultsEl.hidden = false;
  }

  input.addEventListener("input", function () {
    var q = normalize(input.value.trim());
    if (q.length < 2) {
      resultsEl.hidden = true;
      return;
    }
    ready.then(function () {
      var matches = index
        .map(function (item) {
          return { item: item, s: score(item, q) };
        })
        .filter(function (x) {
          return x.s > 0;
        })
        .sort(function (a, b) {
          return b.s - a.s || a.item.title.localeCompare(b.item.title, "zh");
        })
        .map(function (x) {
          return x.item;
        });
      render(matches);
    });
  });

  document.addEventListener("click", function (e) {
    if (!resultsEl.contains(e.target) && e.target !== input) {
      resultsEl.hidden = true;
    }
  });
})();
