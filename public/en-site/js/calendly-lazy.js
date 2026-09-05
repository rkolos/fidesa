/**
 * Lazy Calendly for #contact on home pages.
 *
 * Mode (Task 6):
 * - Click on [data-calendly-open]: inject Calendly widget.js once and mount
 *   an inline widget into [data-calendly-widget] via initInlineWidget only
 *   (empty parentElement — no nested .calendly-inline-widget auto-init).
 * - IntersectionObserver (rootMargin ~150px): on desktop (min-width 1024px)
 *   only, preload widget.js when #contact approaches the viewport IF URL is a
 *   real http(s) link; does NOT mount until click. Mobile: click-to-load only.
 *   Placeholder [CALENDLY_URL] skips preload/mount so the fallback <a> stays
 *   usable until Task 8.
 * - prefers-reduced-motion: same load behaviour; no appearance animation.
 * - Header / sticky CTA stay as #contact anchors — they do not load Calendly.
 *
 * Idempotent: script tag and widget mount run at most once per page.
 * URL source of truth for JS: data-calendly-url on [data-calendly-root].
 */
(function () {
  var SCRIPT_SRC = "https://assets.calendly.com/assets/external/widget.js";
  var root = document.querySelector("[data-calendly-root]");
  if (!root) return;

  var openBtn = root.querySelector("[data-calendly-open]");
  var widgetHost = root.querySelector("[data-calendly-widget]");
  var fallback = root.querySelector(".contact-panel__fallback a");
  var contact = document.getElementById("contact") || root.closest("#contact");

  var scriptState = "idle"; // idle | loading | ready
  var mounted = false;
  var loadWaiters = [];

  function calendlyUrl() {
    return (root.getAttribute("data-calendly-url") || "").trim();
  }

  function isUsableUrl(url) {
    return /^https?:\/\//i.test(url);
  }

  function whenScriptReady(cb) {
    if (scriptState === "ready" && window.Calendly) {
      cb();
      return;
    }
    loadWaiters.push(cb);
    if (scriptState !== "idle") return;
    scriptState = "loading";

    var existing = document.querySelector('script[src="' + SCRIPT_SRC + '"]');
    if (existing) {
      if (window.Calendly) {
        onScriptLoad();
        return;
      }
      existing.addEventListener("load", onScriptLoad);
      existing.addEventListener("error", onScriptError);
      return;
    }

    var s = document.createElement("script");
    s.src = SCRIPT_SRC;
    s.async = true;
    s.addEventListener("load", onScriptLoad);
    s.addEventListener("error", onScriptError);
    document.body.appendChild(s);
  }

  function onScriptLoad() {
    scriptState = "ready";
    var queue = loadWaiters.slice();
    loadWaiters = [];
    for (var i = 0; i < queue.length; i++) queue[i]();
  }

  function onScriptError() {
    scriptState = "idle";
    loadWaiters = [];
    if (widgetHost) {
      widgetHost.removeAttribute("aria-busy");
    }
    if (openBtn) {
      openBtn.disabled = false;
      openBtn.setAttribute("aria-expanded", "false");
    }
  }

  function preload() {
    var url = calendlyUrl();
    if (!isUsableUrl(url)) return;
    whenScriptReady(function () {});
  }

  function focusFallback() {
    if (fallback && typeof fallback.focus === "function") {
      try {
        fallback.focus();
      } catch (e) {
        /* ignore */
      }
    }
  }

  function mount() {
    if (mounted || !widgetHost) return;
    var url = calendlyUrl();

    if (!isUsableUrl(url)) {
      focusFallback();
      return;
    }

    if (openBtn) {
      openBtn.setAttribute("aria-expanded", "true");
    }
    widgetHost.setAttribute("aria-busy", "true");

    whenScriptReady(function () {
      if (mounted) return;
      if (!window.Calendly || typeof window.Calendly.initInlineWidget !== "function") {
        widgetHost.removeAttribute("aria-busy");
        if (openBtn) {
          openBtn.setAttribute("aria-expanded", "false");
        }
        focusFallback();
        return;
      }

      mounted = true;
      widgetHost.hidden = false;
      widgetHost.innerHTML = "";
      window.Calendly.initInlineWidget({
        url: url,
        parentElement: widgetHost,
      });
      widgetHost.setAttribute("aria-busy", "false");

      if (openBtn) {
        openBtn.disabled = true;
        openBtn.setAttribute("aria-expanded", "true");
      }
    });
  }

  if (openBtn) {
    openBtn.addEventListener("click", function (e) {
      e.preventDefault();
      mount();
    });
  }

  // Desktop: preload when #contact nears viewport. Mobile: click-to-load only
  // (Task 7 §2.4 — zero Calendly network until interaction on narrow screens).
  var desktopMq = window.matchMedia("(min-width: 1024px)");
  if (contact && "IntersectionObserver" in window && desktopMq.matches) {
    var io = new IntersectionObserver(
      function (entries) {
        for (var i = 0; i < entries.length; i++) {
          if (entries[i].isIntersecting) {
            preload();
            io.disconnect();
            break;
          }
        }
      },
      { root: null, rootMargin: "150px 0px", threshold: 0 }
    );
    io.observe(contact);
  }
})();
