/**
 * Hero mark: living fog-of-war (desktop ≥1024px).
 * Kill-switch: ?heroMark=off (persisted in localStorage).
 */
(function () {
  var SLOT = document.querySelector("[data-hero-mark]");
  if (!SLOT) return;

  var MQ = window.matchMedia("(min-width: 1024px)");
  var REDUCE = window.matchMedia("(prefers-reduced-motion: reduce)");
  var STORAGE_KEY = "heroMark";
  var SVG_URL = "/assets/brand/logo-hero-mark.svg";
  var loading = false;
  var io = null;

  function resolveVariant() {
    var params = new URLSearchParams(window.location.search);
    var fromQuery = (params.get("heroMark") || "").toLowerCase();
    if (fromQuery === "off") {
      try {
        window.localStorage.setItem(STORAGE_KEY, "off");
      } catch (e) {
        /* ignore */
      }
      return "off";
    }
    if (fromQuery === "on" || fromQuery === "a") {
      try {
        window.localStorage.setItem(STORAGE_KEY, "on");
      } catch (e2) {
        /* ignore */
      }
      return "on";
    }
    try {
      var stored = (window.localStorage.getItem(STORAGE_KEY) || "").toLowerCase();
      if (stored === "off") return "off";
    } catch (e3) {
      /* ignore */
    }
    return "on";
  }

  function clearSlot(forceOff) {
    SLOT.replaceChildren();
    if (forceOff) {
      SLOT.classList.add("is-off");
    } else {
      SLOT.classList.remove("is-off");
    }
  }

  function placeOnBackdrop() {
    var hero = document.querySelector(".hero");
    if (!hero || SLOT.classList.contains("is-off") || !MQ.matches) return;

    SLOT.style.left = "50%";
    SLOT.style.right = "auto";
    SLOT.style.top = "50%";
    SLOT.style.transform = "translate(-50%, -50%)";

    var heroRect = hero.getBoundingClientRect();
    SLOT.style.setProperty("--hero-mark-dx", Math.round(heroRect.width / 2) + "px");
    SLOT.style.setProperty("--hero-mark-dy", Math.round(heroRect.height / 2) + "px");
  }

  function watchVisibility(svg) {
    if (io) {
      io.disconnect();
      io = null;
    }
    if (!("IntersectionObserver" in window)) return;
    io = new IntersectionObserver(
      function (entries) {
        var visible = entries[0] && entries[0].isIntersecting;
        svg.classList.toggle("is-paused", !visible);
      },
      { threshold: 0.12 }
    );
    io.observe(SLOT);
  }

  function markReady(svg, animate) {
    svg.classList.add("hero-mark");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    if (animate) {
      svg.classList.add("is-live");
    } else {
      svg.classList.add("is-static");
    }
    SLOT.classList.remove("is-off");
    SLOT.replaceChildren(svg);
    placeOnBackdrop();
    if (animate) watchVisibility(svg);
  }

  function mount() {
    var variant = resolveVariant();

    if (variant === "off") {
      clearSlot(true);
      return;
    }

    if (!MQ.matches) {
      clearSlot(false);
      return;
    }

    if (loading) return;
    loading = true;

    var animate = !REDUCE.matches;

    fetch(SVG_URL, { credentials: "same-origin" })
      .then(function (res) {
        if (!res.ok) throw new Error("hero-mark svg " + res.status);
        return res.text();
      })
      .then(function (text) {
        loading = false;
        if (resolveVariant() === "off" || !MQ.matches) {
          clearSlot(resolveVariant() === "off");
          return;
        }
        var doc = new DOMParser().parseFromString(text, "image/svg+xml");
        var svg = doc.documentElement;
        if (!svg || svg.nodeName.toLowerCase() !== "svg") {
          throw new Error("hero-mark parse failed");
        }
        markReady(document.importNode(svg, true), animate);
      })
      .catch(function (err) {
        loading = false;
        if (typeof console !== "undefined" && console.warn) {
          console.warn("[hero-mark]", err);
        }
        clearSlot(true);
      });
  }

  mount();

  var placeTick = false;
  function onResize() {
    if (placeTick) return;
    placeTick = true;
    requestAnimationFrame(function () {
      placeTick = false;
      placeOnBackdrop();
    });
  }
  window.addEventListener("resize", onResize);

  if (typeof MQ.addEventListener === "function") {
    MQ.addEventListener("change", mount);
  } else if (typeof MQ.addListener === "function") {
    MQ.addListener(mount);
  }

  if (typeof REDUCE.addEventListener === "function") {
    REDUCE.addEventListener("change", mount);
  } else if (typeof REDUCE.addListener === "function") {
    REDUCE.addListener(mount);
  }
})();
