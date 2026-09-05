/**
 * Domain / language helpers: path-aware UA↔EN links, geo banner on agency.
 * Progressive enhancement only — language of content is determined by URL.
 *
 * Path smoke cases (prod host):
 *   /en/ + #process → https://fidesa.com.ua/#process
 *   /en/vacancies/foo/ → https://fidesa.com.ua/vacancies/foo/
 *   /vacancies/foo/ → https://fidesa.agency/en/vacancies/foo/
 *   /en/blog/foo/ → https://fidesa.com.ua/blog/foo/
 *   /blog/tag/security/ → https://fidesa.agency/en/blog/tag/security/
 * Localhost: enhanceDomainLinks skipped (static hrefs kept).
 */
(function () {
  var UK_ORIGIN = "https://fidesa.com.ua";
  var EN_ORIGIN = "https://fidesa.agency";
  var LANG_CHOICE_KEY = "fidesa.langChoice";
  var LANG_BANNER_KEY = "fidesa.langBanner";
  var SESSION_DISMISS_KEY = "fidesa.langBannerSession";

  var LANG_PREFIX_RE = /^\/(en|de|pl)(?=\/|$)/i;

  function ensureTrailingSlash(path) {
    if (!path || path === "/") return "/";
    return path.endsWith("/") ? path : path + "/";
  }

  function isProductionHost(hostname) {
    var host = (hostname || "").toLowerCase();
    if (!host || host === "localhost" || host === "127.0.0.1") return false;
    if (/^\d{1,3}(\.\d{1,3}){3}$/.test(host)) return false;
    if (host === "fidesa.agency" || host.endsWith(".fidesa.agency")) return true;
    if (host === "fidesa.com.ua" || host.endsWith(".fidesa.com.ua")) return true;
    return false;
  }

  /**
   * Logical path without language prefix (agency /en|/de|/pl stripped).
   * Strips trailing /index.html.
   */
  function getLogicalPath(pathname) {
    var path = pathname || "/";
    path = path.replace(/\/index\.html$/i, "/");
    if (path === "/index.html" || path === "") path = "/";
    var stripped = path.replace(LANG_PREFIX_RE, "");
    if (!stripped || stripped === "/") return "/";
    return stripped.charAt(0) === "/" ? stripped : "/" + stripped;
  }

  /**
   * Vacancies + blog: slug parity UK↔EN — mirror full path.
   * Home and /privacy/ stay 1:1.
   */
  function toMirrorPath(logicalPath) {
    var path = ensureTrailingSlash(logicalPath || "/");
    if (path === "/") return "/";
    if (path === "/privacy/") return "/privacy/";
    if (path.indexOf("/vacancies/") === 0) return path;
    if (path.indexOf("/blog/") === 0) return path;
    return path;
  }

  function buildUkUrl(logicalPath, search, hash) {
    var path = ensureTrailingSlash(toMirrorPath(logicalPath || "/"));
    return UK_ORIGIN + (path === "/" ? "/" : path) + (search || "") + (hash || "");
  }

  function buildEnUrl(logicalPath, search, hash) {
    var logical = toMirrorPath(logicalPath || "/");
    var path =
      logical === "/" ? "/en/" : "/en" + ensureTrailingSlash(logical);
    return EN_ORIGIN + path + (search || "") + (hash || "");
  }

  function mirrorUrl(targetLang, loc) {
    loc = loc || window.location;
    var logical = getLogicalPath(loc.pathname);
    var search = loc.search || "";
    var hash = loc.hash || "";
    if (targetLang === "uk") return buildUkUrl(logical, search, hash);
    return buildEnUrl(logical, search, hash);
  }

  function isAgencySite() {
    var root = document.documentElement;
    if (root.getAttribute("data-site") === "agency") return true;
    if (root.getAttribute("data-site") === "uk") return false;
    var host = (window.location.hostname || "").toLowerCase();
    if (host === "fidesa.agency" || host.endsWith(".fidesa.agency")) return true;
    if (host === "fidesa.com.ua" || host.endsWith(".fidesa.com.ua")) return false;
    return LANG_PREFIX_RE.test(window.location.pathname || "");
  }

  function prefersUkrainian() {
    var list = [];
    if (navigator.languages && navigator.languages.length) {
      for (var i = 0; i < navigator.languages.length; i++) {
        list.push(navigator.languages[i]);
      }
    } else if (navigator.language) {
      list.push(navigator.language);
    }
    for (var j = 0; j < list.length; j++) {
      var code = (list[j] || "").toLowerCase();
      if (code === "uk" || code.indexOf("uk-") === 0) return true;
    }
    return false;
  }

  function readStorage(storage, key) {
    try {
      return storage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  function writeStorage(storage, key, value) {
    try {
      storage.setItem(key, value);
    } catch (e) {
      /* ignore quota / private mode */
    }
  }

  function bannerSuppressed() {
    if (readStorage(localStorage, LANG_BANNER_KEY) === "hidden") return true;
    var choice = readStorage(localStorage, LANG_CHOICE_KEY);
    if (choice === "en" || choice === "uk" || choice === "dismiss") return true;
    if (readStorage(sessionStorage, SESSION_DISMISS_KEY) === "1") return true;
    return false;
  }

  function enhanceDomainLinks() {
    if (!isProductionHost(window.location.hostname)) return;

    var links = document.querySelectorAll("[data-domain-switch]");
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var target = link.getAttribute("data-domain-switch");
      if (target !== "uk" && target !== "en") continue;
      link.setAttribute("href", mirrorUrl(target));
    }
  }

  function initBanner() {
    var banner = document.getElementById("lang-banner");
    if (!banner || !isAgencySite()) return;
    if (bannerSuppressed() || !prefersUkrainian()) return;

    var goUk = banner.querySelector("[data-banner-go-uk]");
    var stayEn = banner.querySelector("[data-banner-stay-en]");
    var dismiss = banner.querySelector("[data-banner-dismiss]");
    var persist = banner.querySelector("[data-banner-persist]");

    if (goUk && isProductionHost(window.location.hostname)) {
      goUk.setAttribute("href", mirrorUrl("uk"));
    }

    banner.hidden = false;
    banner.classList.add("is-visible");

    function hideBanner() {
      banner.hidden = true;
      banner.classList.remove("is-visible");
    }

    function persistHide() {
      writeStorage(localStorage, LANG_BANNER_KEY, "hidden");
    }

    function commitDontShowAgain() {
      writeStorage(localStorage, LANG_CHOICE_KEY, "dismiss");
      persistHide();
      hideBanner();
    }

    if (goUk) {
      goUk.addEventListener("click", function () {
        writeStorage(localStorage, LANG_CHOICE_KEY, "uk");
        /* navigation follows href (path-aware on prod) */
      });
    }

    if (stayEn) {
      stayEn.addEventListener("click", function () {
        writeStorage(localStorage, LANG_CHOICE_KEY, "en");
        persistHide();
        hideBanner();
      });
    }

    if (dismiss) {
      dismiss.addEventListener("click", function () {
        if (persist && persist.checked) {
          commitDontShowAgain();
        } else {
          writeStorage(sessionStorage, SESSION_DISMISS_KEY, "1");
          hideBanner();
        }
      });
    }

    if (persist) {
      persist.addEventListener("change", function () {
        if (persist.checked) {
          commitDontShowAgain();
        }
        /* unchecking does not clear already-written hidden */
      });
    }
  }

  /* Public helpers for Tasks 4–5 */
  window.FidesaDomainLang = {
    getLogicalPath: getLogicalPath,
    toMirrorPath: toMirrorPath,
    mirrorUrl: mirrorUrl,
    buildUkUrl: buildUkUrl,
    buildEnUrl: buildEnUrl,
    isAgencySite: isAgencySite,
    isProductionHost: isProductionHost,
  };

  enhanceDomainLinks();
  initBanner();
})();
