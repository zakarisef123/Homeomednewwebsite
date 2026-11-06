/* HOMEOMED — interactions légères, sans dépendance */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  /* Header shadow on scroll */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Mobile menu */
  var menuBtn = document.querySelector(".menu-btn");
  if (menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("menu-open")) {
        document.body.classList.remove("menu-open");
        menuBtn.setAttribute("aria-expanded", "false");
        menuBtn.focus();
      }
    });
  }

  /* Submenus (click / keyboard) */
  document.querySelectorAll(".nav-toggle-sub").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.closest(".has-sub");
      var open = !li.classList.contains("open");
      document.querySelectorAll(".has-sub.open").forEach(function (o) {
        if (o !== li) { o.classList.remove("open"); o.querySelector(".nav-toggle-sub").setAttribute("aria-expanded", "false"); }
      });
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-sub")) {
      document.querySelectorAll(".has-sub.open").forEach(function (o) {
        o.classList.remove("open");
        o.querySelector(".nav-toggle-sub").setAttribute("aria-expanded", "false");
      });
    }
  });

  /* Reveal on scroll */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* Carrousels : défilement page par page (3 avis par 3 sur ordinateur, 1 par 1 sur mobile) */
  document.querySelectorAll("[data-carousel]").forEach(function (wrap) {
    var track = wrap.querySelector(".carousel-track");
    var prev = wrap.querySelector("[data-prev]");
    var next = wrap.querySelector("[data-next]");
    var dots = wrap.querySelector(".carousel-dots");
    if (!track) return;
    function visible() { return Array.prototype.filter.call(track.children, function (c) { return !c.hidden; }); }
    function perPage() {
      var items = visible();
      if (!items.length) return 1;
      var w = items[0].getBoundingClientRect().width + 24;
      return Math.max(1, Math.round((track.clientWidth + 24) / w));
    }
    function step() {
      var items = visible();
      return items.length ? items[0].getBoundingClientRect().width + 24 : 1;
    }
    function pages() { return Math.max(1, Math.ceil(visible().length / perPage())); }
    function current() {
      var n = pages();
      if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 4) return n - 1;
      return Math.min(n - 1, Math.floor(Math.round(track.scrollLeft / step()) / perPage()));
    }
    function go(i) {
      var n = pages();
      i = (i + n) % n;
      var target = visible()[i * perPage()];
      if (!target) return;
      page = i;
      var left = target.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft - 4;
      track.scrollTo({ left: Math.max(0, left), behavior: "smooth" });
    }
    function renderDots() {
      if (!dots) return;
      var n = pages(), c = Math.min(page, n - 1);
      dots.innerHTML = "";
      for (var i = 0; i < n; i++) {
        var d = document.createElement("span");
        if (i === c) d.className = "on";
        dots.appendChild(d);
      }
      var hide = n < 2;
      if (prev) prev.disabled = hide;
      if (next) next.disabled = hide;
    }
    var page = 0;
    if (prev) prev.addEventListener("click", function () { go(page - 1); });
    if (next) next.addEventListener("click", function () { go(page + 1); });
    var t;
    track.addEventListener("scroll", function () {
      clearTimeout(t);
      t = setTimeout(function () { page = current(); renderDots(); }, 150);
    }, { passive: true });
    window.addEventListener("resize", renderDots);
    renderDots();

    /* Filtres par thème */
    wrap.querySelectorAll("[data-rev-filter]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = btn.getAttribute("data-rev-filter");
        wrap.querySelectorAll("[data-rev-filter]").forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
        Array.prototype.forEach.call(track.children, function (c) {
          c.hidden = f !== "all" && c.getAttribute("data-cat") !== f;
        });
        track.scrollTo({ left: 0 });
        page = 0;
        renderDots();
      });
    });
  });

  /* Click-to-load embeds (cartes Google, agenda OneDoc) — respect de la vie privée */
  function loadEmbed(box) {
    if (box.classList.contains("loaded")) return;
    var f = document.createElement("iframe");
    f.src = box.getAttribute("data-src");
    f.title = box.getAttribute("data-title") || "Contenu intégré";
    f.loading = "lazy";
    f.setAttribute("allowfullscreen", "");
    f.setAttribute("referrerpolicy", "no-referrer-when-downgrade");
    box.appendChild(f);
    box.classList.add("loaded");
  }
  document.querySelectorAll("[data-embed]").forEach(function (box) {
    var btn = box.querySelector("button");
    if (btn) btn.addEventListener("click", function () { loadEmbed(box); });
    if (box.hasAttribute("data-autoload")) loadEmbed(box);
  });

  /* Année courante */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();

/* Onglets de l'explorateur de services (accessible clavier) */
(function () {
  document.querySelectorAll("[data-tabs]").forEach(function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll('[role="tab"]'));
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, n = null;
        if (k === "ArrowDown" || k === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (k === "ArrowUp" || k === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (k === "Home") n = tabs[0];
        if (k === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  });
})();

/* Sélecteur « Pour qui consultez-vous ? » (met en avant les services concernés) */
(function () {
  var bar = document.querySelector("[data-filter-bar]");
  var grid = document.querySelector(".svc-tiles");
  if (!bar || !grid) return;
  var tiles = Array.prototype.slice.call(grid.querySelectorAll(".svc-tile"));
  var btns = Array.prototype.slice.call(bar.querySelectorAll("[data-filter]"));
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.getAttribute("data-filter");
      var active = f !== "all" && b.getAttribute("aria-pressed") !== "true";
      btns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      (active ? b : bar.querySelector('[data-filter="all"]')).setAttribute("aria-pressed", "true");
      grid.classList.toggle("filtering", active);
      tiles.forEach(function (t) {
        var on = active && (" " + t.getAttribute("data-profiles") + " ").indexOf(" " + f + " ") > -1;
        t.classList.toggle("match", on);
        t.classList.add("in");
      });
    });
  });
})();
