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

  /* Carousels */
  document.querySelectorAll("[data-carousel]").forEach(function (wrap) {
    var track = wrap.querySelector(".carousel-track");
    var prev = wrap.querySelector("[data-prev]");
    var next = wrap.querySelector("[data-next]");
    function step() {
      var item = track.firstElementChild;
      return item ? item.getBoundingClientRect().width + 24 : 320;
    }
    if (prev) prev.addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: "smooth" }); });
    if (next) next.addEventListener("click", function () { track.scrollBy({ left: step(), behavior: "smooth" }); });
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
