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
      var en = document.documentElement.lang.indexOf("en") === 0;
      menuBtn.setAttribute("aria-label", open ? (en ? "Close menu" : "Fermer le menu") : (en ? "Open menu" : "Ouvrir le menu"));
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

/* Tunnel « Rendez-vous express » : âge → motif → cabinet & type → récapitulatif */
(function () {
  var EN = document.documentElement.lang.indexOf("en") === 0;
  var AGE = EN ? { bebe: "my baby (0 – 2 years)", enfant: "my child (3 – 11 years)", ado: "my teenager (12 – 17 years)", adulte: "myself (adult)", senior: "myself (senior)" }
               : { bebe: "mon bébé (0 – 2 ans)", enfant: "mon enfant (3 – 11 ans)", ado: "mon adolescent·e (12 – 17 ans)", adulte: "moi (adulte)", senior: "moi (senior)" };
  var AGE_SHORT = EN ? { bebe: "Baby", enfant: "Child", ado: "Teenager", adulte: "Adult", senior: "Senior" }
                     : { bebe: "Bébé", enfant: "Enfant", ado: "Adolescent", adulte: "Adulte", senior: "Senior" };
  var CAB = EN ? { pully: "Pully – Lausanne (Place Neuve 1)", fribourg: "Fribourg (Centre ITS, Thursday)", visio: "by video call" }
               : { pully: "Pully – Lausanne (Place Neuve 1)", fribourg: "Fribourg (Centre ITS, jeudi)", visio: "en visio" };
  var CAB_SHORT = EN ? { pully: "Pully", fribourg: "Fribourg", visio: "Video call" } : { pully: "Pully", fribourg: "Fribourg", visio: "Visio" };
  var TYPE = EN ? { premiere: "first consultation", suivi: "follow-up consultation", urgence: "acute care" }
                : { premiere: "première consultation", suivi: "consultation de suivi", urgence: "urgence homéo" };
  var TX = EN ? {
      step: function (n) { return "Step " + n + " of 3"; }, recap: "Summary", your: "Your appointment", who: "For", reason: "Reason",
      place: "Location", type: "Type", fee: "Indicative fee", flat: "flat rate", warn: "In a medical emergency, contact your doctor or call 144.",
      book: "Book online", wa: "WhatsApp", call: "Call", mail: "Email", more: "Learn more about this support", subject: "Appointment request",
      hello: "Hello Ms Orlando, I would like to book an appointment for ", motif: " — reason: ", thanks: ". Thank you!",
      req: "Your request:", visioTip: "In the calendar, choose a video consultation (or call me to arrange it).",
      tipA: "In the calendar below, select the ", tipB: " practice."
    } : {
      step: function (n) { return "Étape " + n + " sur 3"; }, recap: "Récapitulatif", your: "Votre rendez-vous", who: "Pour", reason: "Motif",
      place: "Lieu", type: "Type", fee: "Tarif indicatif", flat: "forfait", warn: "En cas d’urgence médicale, contactez votre médecin ou le 144.",
      book: "Réserver en ligne", wa: "WhatsApp", call: "Appeler", mail: "E-mail", more: "En savoir plus sur cet accompagnement", subject: "Demande de rendez-vous",
      hello: "Bonjour Madame Orlando, je souhaite prendre rendez-vous pour ", motif: " — motif : ", thanks: ". Merci !",
      req: "Votre demande&nbsp;:", visioTip: "Dans le calendrier, choisissez une consultation en visio (ou appelez-moi pour l’organiser).",
      tipA: "Dans le calendrier ci-dessous, sélectionnez le cabinet de ", tipB: "."
    };

  function price(type, age) {
    var minor = age === "bebe" || age === "enfant" || age === "ado";
    if (type === "premiere") return ["CHF 230.–", "75 – 90 min"];
    if (type === "urgence") return ["CHF 150.–", TX.flat];
    return minor ? ["CHF 90.–", "30 min"] : ["CHF 150.–", "45 – 60 min"];
  }

  document.querySelectorAll("[data-funnel]").forEach(function (box) {
    var root = box.getAttribute("data-root") || "";
    var preset = box.getAttribute("data-preset") || "";
    var st = { step: 1, age: null, motif: null, href: "", cab: null, type: null };
    var steps = box.querySelectorAll(".fn-step");
    var prog = box.querySelectorAll(".fn-progress li");
    var back = box.querySelector(".fn-back");
    var count = box.querySelector(".fn-count");

    /* Sur une page service, ses motifs passent en tête et sont signalés */
    if (preset) {
      var grid = box.querySelector(".motifs");
      Array.prototype.slice.call(grid.children).reverse().forEach(function (b) {
        if ((b.getAttribute("data-href") || "").indexOf(preset) === 0) { b.classList.add("featured"); grid.insertBefore(b, grid.firstChild); }
      });
    }

    function show(n) {
      st.step = n;
      steps.forEach(function (s) { s.hidden = +s.getAttribute("data-step") !== n; });
      prog.forEach(function (li, i) { li.classList.toggle("on", i < Math.min(n, 3)); li.classList.toggle("done", i < n - 1); });
      back.hidden = n === 1;
      count.textContent = n <= 3 ? TX.step(n) : TX.recap;
      if (n > 1) {
        var r = box.getBoundingClientRect();
        if (r.top < 80 || r.top > window.innerHeight * 0.5) box.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
    function select(group, btn) {
      box.querySelectorAll(group).forEach(function (b) { b.classList.toggle("sel", b === btn); b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
    }

    box.querySelectorAll("[data-age]").forEach(function (b) {
      b.addEventListener("click", function () {
        st.age = b.getAttribute("data-age");
        select("[data-age]", b);
        box.querySelectorAll(".fn-motif").forEach(function (m) {
          m.hidden = (" " + m.getAttribute("data-ages") + " ").indexOf(" " + st.age + " ") < 0;
        });
        show(2);
      });
    });
    box.querySelectorAll(".fn-motif").forEach(function (b) {
      b.addEventListener("click", function () {
        st.motif = b.textContent.trim(); st.href = b.getAttribute("data-href");
        select(".fn-motif", b);
        if (b.getAttribute("data-href") === "tarifs-remboursements/" || b.getAttribute("data-href").indexOf("fees-and-insurance/") === 0) { st.type = "urgence"; select(".fn-type", box.querySelector('[data-type="urgence"]')); }
        show(3);
      });
    });
    function maybeDone() { if (st.cab && st.type) result(); }
    /* Sur une page cabinet, le lieu est présélectionné */
    var cabPreset = box.getAttribute("data-cab-preset");
    if (cabPreset) {
      var cb = box.querySelector('[data-cab="' + cabPreset + '"]');
      if (cb) { st.cab = cabPreset; cb.classList.add("sel"); cb.setAttribute("aria-pressed", "true"); }
    }
    box.querySelectorAll("[data-cab]").forEach(function (b) {
      b.addEventListener("click", function () { st.cab = b.getAttribute("data-cab"); select("[data-cab]", b); maybeDone(); });
    });
    box.querySelectorAll(".fn-type").forEach(function (b) {
      b.addEventListener("click", function () { st.type = b.getAttribute("data-type"); select(".fn-type", b); maybeDone(); });
    });
    back.addEventListener("click", function () { show(Math.max(1, st.step - 1)); });

    function result() {
      var p = price(st.type, st.age);
      var msg = TX.hello + AGE[st.age] + TX.motif + st.motif + " — " + TYPE[st.type] + ", " + CAB[st.cab] + TX.thanks;
      var q = "?cab=" + st.cab + "&age=" + st.age + "&type=" + st.type + "&motif=" + encodeURIComponent(st.motif);
      box.querySelector(".fn-summary").innerHTML =
        '<p class="fn-q">' + TX.your + "</p>" +
        '<ul class="fn-recap">' +
        "<li><span>" + TX.who + "</span><strong>" + AGE_SHORT[st.age] + "</strong></li>" +
        "<li><span>" + TX.reason + "</span><strong>" + st.motif + "</strong></li>" +
        "<li><span>" + TX.place + "</span><strong>" + CAB_SHORT[st.cab] + "</strong></li>" +
        "<li><span>" + TX.type + "</span><strong>" + TYPE[st.type].charAt(0).toUpperCase() + TYPE[st.type].slice(1) + "</strong></li>" +
        '<li class="fn-price"><span>' + TX.fee + "</span><strong>" + p[0] + " <small>· " + p[1] + "</small></strong></li>" +
        "</ul>" +
        (st.type === "urgence" ? '<p class="small fn-warn">' + TX.warn + "</p>" : "");
      var a = box.querySelector(".fn-actions");
      a.innerHTML =
        '<a class="btn btn-primary" href="' + root + (box.getAttribute("data-rdv") || "prendre-rdv/") + q + '#calendrier">' + TX.book + "</a>" +
        '<a class="btn btn-wa" href="' + box.getAttribute("data-wa") + "?text=" + encodeURIComponent(msg) + '" target="_blank" rel="noopener">' + TX.wa + "</a>" +
        '<a class="btn btn-ghost" href="' + box.getAttribute("data-tel") + '">' + TX.call + "</a>" +
        '<a class="btn btn-ghost" href="mailto:' + box.getAttribute("data-mail") + "?subject=" + encodeURIComponent(TX.subject) + "&body=" + encodeURIComponent(msg) + '">' + TX.mail + "</a>" +
        (st.href ? '<a class="link-arrow fn-more" href="' + root + st.href + '">' + TX.more + "</a>" : "");
      show(4);
    }
  });

  /* Page Prendre RDV : rappel du choix fait dans le tunnel */
  var banner = document.querySelector("[data-rdv-summary]");
  if (banner && window.URLSearchParams) {
    var q = new URLSearchParams(location.search);
    var cab = q.get("cab");
    if (cab && CAB[cab]) {
      var age = AGE_SHORT[q.get("age")] || "", type = TYPE[q.get("type")] || "", motif = q.get("motif") || "";
      var tip = cab === "visio" ? TX.visioTip : TX.tipA + "<strong>" + CAB_SHORT[cab] + "</strong>" + TX.tipB;
      banner.innerHTML = "<strong>" + TX.req + "</strong> " + [age, motif, type, CAB_SHORT[cab]].filter(Boolean).map(function (x) {
        return x.replace(/[<>&]/g, "");
      }).join(" · ") + "<br>" + tip;
      banner.hidden = false;
    }
  }
})();
