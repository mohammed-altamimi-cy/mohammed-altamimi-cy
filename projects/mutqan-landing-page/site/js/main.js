(function () {
  "use strict";

  var LANG_KEY = "mutqan-lang";
  var dict = window.MUTQAN_I18N;

  function getLang() {
    return localStorage.getItem(LANG_KEY) || "en";
  }

  function applyLang(lang) {
    var strings = dict[lang] || dict.en;
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var value = strings[key];
      if (value === undefined) return;
      if (value.indexOf("<") !== -1) {
        el.innerHTML = value;
      } else {
        el.textContent = value;
      }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-placeholder");
      var value = strings[key];
      if (value !== undefined) el.setAttribute("placeholder", value);
    });

    var metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc && strings["meta.desc"]) metaDesc.setAttribute("content", strings["meta.desc"]);

    var yearEl = document.getElementById("year");
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    localStorage.setItem(LANG_KEY, lang);
  }

  function toggleLang() {
    applyLang(getLang() === "en" ? "ar" : "en");
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyLang(getLang());

    var langBtn = document.getElementById("lang-toggle");
    if (langBtn) langBtn.addEventListener("click", toggleLang);

    // Mobile menu
    var menuToggle = document.getElementById("menu-toggle");
    var mainNav = document.getElementById("main-nav");
    if (menuToggle && mainNav) {
      menuToggle.addEventListener("click", function () {
        var isOpen = mainNav.classList.toggle("is-open");
        menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
      mainNav.querySelectorAll("a, button").forEach(function (el) {
        el.addEventListener("click", function () {
          mainNav.classList.remove("is-open");
          menuToggle.setAttribute("aria-expanded", "false");
        });
      });
    }

    // Smooth-scroll every CTA that targets the hero form, then focus the first field
    document.querySelectorAll('.js-scroll-to-form, a[href="#hero-form"]').forEach(function (el) {
      el.addEventListener("click", function (e) {
        var target = document.getElementById("hero-form");
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        var firstField = document.getElementById("f-name");
        if (firstField) window.setTimeout(function () { firstField.focus({ preventScroll: true }); }, 500);
        history.replaceState(null, "", "#hero-form");
      });
    });

    // Product-preview tabs (cosmetic active state)
    var previewTabs = document.querySelectorAll(".preview-tab");
    previewTabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        previewTabs.forEach(function (t) { t.classList.remove("is-active"); });
        tab.classList.add("is-active");
      });
    });

    // Sticky header shadow on scroll
    var header = document.querySelector(".site-header");
    if (header) {
      window.addEventListener("scroll", function () {
        header.classList.toggle("is-scrolled", window.scrollY > 8);
      }, { passive: true });
    }

    // Demo form -> mailto submission
    var form = document.getElementById("demo-form");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var lang = getLang();
        var strings = dict[lang] || dict.en;

        var requiredIds = ["f-name", "f-company", "f-email", "f-phone", "f-facility"];
        var missing = requiredIds.some(function (id) {
          var el = document.getElementById(id);
          return el && !el.value.trim();
        });
        if (missing) {
          form.reportValidity();
          return;
        }

        var name = document.getElementById("f-name").value.trim();
        var company = document.getElementById("f-company").value.trim();
        var email = document.getElementById("f-email").value.trim();
        var phone = document.getElementById("f-phone").value.trim();
        var facilitySelect = document.getElementById("f-facility");
        var facilityLabel = facilitySelect.options[facilitySelect.selectedIndex].text;
        var jobTitle = document.getElementById("f-title").value.trim();
        var locations = document.getElementById("f-locations").value.trim();
        var notes = document.getElementById("f-notes").value.trim();

        var improve = Array.from(document.querySelectorAll('input[name="improve"]:checked'))
          .map(function (cb) { return cb.parentElement.textContent.trim(); })
          .join(", ");

        var subject = (lang === "ar" ? "طلب عرض توضيحي — " : "Demo request — ") + name;

        var lines = [
          strings["form.name"] + " " + name,
          strings["form.company"] + " " + company,
          strings["form.email"] + " " + email,
          strings["form.phone"] + " " + phone,
          strings["form.facilityType"] + " " + facilityLabel
        ];
        if (improve) lines.push(strings["form.improve"] + " " + improve);
        if (jobTitle) lines.push(strings["form.jobTitle"] + " " + jobTitle);
        if (locations) lines.push(strings["form.locations"] + " " + locations);
        if (notes) lines.push(strings["form.notes"] + " " + notes);

        var body = lines.join("\n");
        var mailto = "mailto:info@mutqan-sa.com" +
          "?subject=" + encodeURIComponent(subject) +
          "&body=" + encodeURIComponent(body);

        var status = document.getElementById("form-status");
        if (status) status.textContent = strings["form.statusSuccess"];

        window.location.href = mailto;
      });
    }

    // Reveal-on-scroll for section headings/cards
    var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var revealTargets = document.querySelectorAll(".section, .hero-form-wrap");
    if (prefersReducedMotion) {
      revealTargets.forEach(function (el) { el.classList.add("is-visible"); });
    } else if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.08 });
      revealTargets.forEach(function (el) { io.observe(el); });
    } else {
      revealTargets.forEach(function (el) { el.classList.add("is-visible"); });
    }
  });
})();
