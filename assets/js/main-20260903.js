/*!
 * MUSCLE GYM SHONAN — main.js
 * バニラJSのみ・依存ライブラリなし。役割は3つだけ:
 *   1) スクロール出現アニメーション（IntersectionObserver）
 *   2) モバイル固定CTAバーの表示切り替え
 *   3) CTAクリックのdataLayerイベント送出（GTM/GA4連携用）
 */
(function () {
  "use strict";

  /* ---------- 1) Scroll reveal ---------- */
  var revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && revealEls.length) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    revealEls.forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add("in-view");
    });
  }

  /* ---------- 2) Sticky mobile CTA bar ---------- */
  var stickyCta = document.getElementById("stickyCta");
  var hero = document.querySelector(".hero");
  if (stickyCta && hero) {
    if ("IntersectionObserver" in window) {
      var heroObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            stickyCta.hidden = false;
            if (entry.isIntersecting) {
              stickyCta.classList.remove("is-visible");
            } else {
              stickyCta.classList.add("is-visible");
            }
          });
        },
        { threshold: 0 }
      );
      heroObserver.observe(hero);
    } else {
      stickyCta.hidden = false;
      stickyCta.classList.add("is-visible");
    }
  }

  /* ---------- 3) CTA click tracking (GTM/GA4 ready) ---------- */
  window.dataLayer = window.dataLayer || [];
  document.addEventListener("click", function (e) {
    var target = e.target.closest("[data-cta]");
    if (!target) return;
    window.dataLayer.push({
      event: "cta_click",
      cta_id: target.getAttribute("data-cta"),
      cta_label: (target.textContent || "").trim(),
      cta_href: target.getAttribute("href") || ""
    });
  });

  /* Footer year */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
