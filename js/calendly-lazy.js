/**
 * Lazy Calendly: inline widget on home #contact + sitewide badge.
 *
 * Mode:
 * - Inline: click [data-calendly-open] → inject widget.js once, mount via
 *   initInlineWidget into [data-calendly-widget]. Desktop (min-width 1024px):
 *   IntersectionObserver (~150px) preloads script when #contact nears viewport;
 *   mobile: click-to-load only. URL: data-calendly-url on [data-calendly-root].
 * - Badge: lazy initBadgeWidget after requestIdleCallback (~2s fallback) or
 *   first scroll/pointerdown — whichever comes first. Shared CSS+JS inject.
 *   On home: hide badge while #sticky-cta is visible or #contact is near
 *   viewport (avoids double CTA with sticky bar).
 * - Header / sticky CTA stay as #contact anchors — they do not load Calendly.
 *
 * Idempotent: script/css tags, inline mount, and badge init run at most once.
 */
(function () {
  var SCRIPT_SRC = "https://assets.calendly.com/assets/external/widget.js";
  var CSS_HREF = "https://assets.calendly.com/assets/external/widget.css";
  var BADGE_URL = "https://calendly.com/vkolos325/cooperation-with-dna325";
  var BADGE_COLOR = "#2E4259";
  var BADGE_TEXT_COLOR = "#ffffff";

  var root = document.querySelector("[data-calendly-root]");
  var openBtn = root ? root.querySelector("[data-calendly-open]") : null;
  var widgetHost = root ? root.querySelector("[data-calendly-widget]") : null;
  var fallback = root ? root.querySelector(".contact-panel__fallback a") : null;
  var contact = document.getElementById("contact") || (root && root.closest("#contact"));

  var scriptState = "idle"; // idle | loading | ready
  var mounted = false;
  var badgeInited = false;
  var loadWaiters = [];

  function calendlyUrl() {
    if (!root) return BADGE_URL;
    return (root.getAttribute("data-calendly-url") || "").trim() || BADGE_URL;
  }

  function isUsableUrl(url) {
    return /^https?:\/\//i.test(url);
  }

  function ensureCss() {
    if (document.querySelector('link[href="' + CSS_HREF + '"]')) return;
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = CSS_HREF;
    document.head.appendChild(link);
  }

  function whenScriptReady(cb) {
    if (scriptState === "ready" && window.Calendly) {
      cb();
      return;
    }
    loadWaiters.push(cb);
    if (scriptState !== "idle") return;
    scriptState = "loading";
    ensureCss();

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
        resize: true,
      });
      widgetHost.setAttribute("aria-busy", "false");

      if (openBtn) {
        openBtn.disabled = true;
        openBtn.setAttribute("aria-expanded", "true");
      }
    });
  }

  function badgeText() {
    var lang = (document.documentElement.lang || "").toLowerCase();
    if (lang.indexOf("uk") === 0 || lang.indexOf("ua") === 0) {
      return "Забронювати дзвінок";
    }
    return "Book a call";
  }

  function setBadgeVisible(visible) {
    var badge = document.querySelector(".calendly-badge-widget");
    if (!badge) return;
    badge.style.display = visible ? "" : "none";
  }

  function shouldHideBadgeNearContact() {
    if (!contact) return false;
    var sticky = document.getElementById("sticky-cta");
    if (sticky && sticky.classList.contains("is-visible") && !sticky.hidden) {
      return true;
    }
    var rect = contact.getBoundingClientRect();
    return rect.top < window.innerHeight * 0.85;
  }

  function updateBadgeVisibility() {
    if (!badgeInited) return;
    setBadgeVisible(!shouldHideBadgeNearContact());
  }

  function initBadge() {
    if (badgeInited) return;
    if (!isUsableUrl(BADGE_URL)) return;

    whenScriptReady(function () {
      if (badgeInited) return;
      if (!window.Calendly || typeof window.Calendly.initBadgeWidget !== "function") {
        return;
      }
      badgeInited = true;
      window.Calendly.initBadgeWidget({
        url: BADGE_URL,
        text: badgeText(),
        color: BADGE_COLOR,
        textColor: BADGE_TEXT_COLOR,
        branding: true,
      });
      updateBadgeVisibility();
    });
  }

  function scheduleBadge() {
    var done = false;
    function trigger() {
      if (done) return;
      done = true;
      window.removeEventListener("scroll", onInteract, true);
      window.removeEventListener("pointerdown", onInteract, true);
      initBadge();
    }
    function onInteract() {
      trigger();
    }

    window.addEventListener("scroll", onInteract, { capture: true, passive: true, once: true });
    window.addEventListener("pointerdown", onInteract, { capture: true, passive: true, once: true });

    if (typeof window.requestIdleCallback === "function") {
      window.requestIdleCallback(trigger, { timeout: 2000 });
    } else {
      setTimeout(trigger, 2000);
    }
  }

  // --- Inline widget (home Contacts only) ---
  if (openBtn) {
    openBtn.addEventListener("click", function (e) {
      e.preventDefault();
      mount();
    });
  }

  var desktopMq = window.matchMedia("(min-width: 1024px)");
  if (root && contact && "IntersectionObserver" in window && desktopMq.matches) {
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

  // --- Sitewide badge ---
  scheduleBadge();

  if (contact) {
    var ticking = false;
    function onScrollHide() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        updateBadgeVisibility();
        ticking = false;
      });
    }
    window.addEventListener("scroll", onScrollHide, { passive: true });
    window.addEventListener("resize", onScrollHide, { passive: true });
  }
})();
