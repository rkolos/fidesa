/**
 * Vacancies list filters: direction ∩ location ∩ format (AND).
 * Syncs ?direction=&location=&format=; empty params removed.
 * Progressive enhancement — all cards remain in HTML for SEO/AEO.
 */
(function () {
  var root = document.querySelector("[data-vacancies-filters]");
  if (!root) return;

  var cards = Array.prototype.slice.call(
    document.querySelectorAll("[data-vacancy-card]")
  );
  var countEl = document.querySelector("[data-vacancies-count]");
  var emptyEl = document.querySelector("[data-vacancies-empty]");
  var listEl = document.querySelector("[data-vacancies-list]");
  var panel = document.querySelector("[data-filters-panel]");
  var openBtn = document.querySelector("[data-filters-open]");
  var closeBtn = document.querySelector("[data-filters-close]");
  var applyBtn = document.querySelector("[data-filters-apply]");
  var resetBtns = Array.prototype.slice.call(
    document.querySelectorAll("[data-filters-reset]")
  );

  var fieldNames = ["direction", "location", "format"];
  var appliedFilters = { direction: "", location: "", format: "" };
  var previousOverflow = "";
  var trapHandler = null;

  function selectsFor(name) {
    return Array.prototype.slice.call(
      document.querySelectorAll('select[name="' + name + '"]')
    );
  }

  function allowedValues(name) {
    var els = selectsFor(name);
    if (!els.length) return {};
    var map = { "": true };
    Array.prototype.forEach.call(els[0].options, function (opt) {
      map[opt.value] = true;
    });
    return map;
  }

  function sanitizeFilters(filters) {
    var out = { direction: "", location: "", format: "" };
    fieldNames.forEach(function (name) {
      var value = filters[name] || "";
      out[name] = allowedValues(name)[value] ? value : "";
    });
    return out;
  }

  var isEn =
    (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;

  function pluralCount(n) {
    if (isEn) {
      return n === 1 ? "1 vacancy" : n + " vacancies";
    }
    var mod10 = n % 10;
    var mod100 = n % 100;
    if (mod10 === 1 && mod100 !== 11) return n + " вакансія";
    if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) {
      return n + " вакансії";
    }
    return n + " вакансій";
  }

  function readControls() {
    var out = { direction: "", location: "", format: "" };
    fieldNames.forEach(function (name) {
      var els = selectsFor(name);
      if (els.length) out[name] = els[0].value || "";
    });
    return sanitizeFilters(out);
  }

  function setControls(filters) {
    fieldNames.forEach(function (name) {
      var value = filters[name] || "";
      selectsFor(name).forEach(function (el) {
        el.value = value;
      });
    });
  }

  function readUrl() {
    var params = new URLSearchParams(window.location.search);
    return sanitizeFilters({
      direction: params.get("direction") || "",
      location: params.get("location") || "",
      format: params.get("format") || "",
    });
  }

  function writeUrl(filters) {
    var params = new URLSearchParams();
    if (filters.direction) params.set("direction", filters.direction);
    if (filters.location) params.set("location", filters.location);
    if (filters.format) params.set("format", filters.format);
    var qs = params.toString();
    var next =
      window.location.pathname + (qs ? "?" + qs : "") + window.location.hash;
    var current =
      window.location.pathname + window.location.search + window.location.hash;
    if (next !== current) {
      window.history.replaceState(null, "", next);
    }
  }

  function attrTokens(card, attr) {
    var raw = card.getAttribute(attr) || "";
    return raw.split(/\s+/).filter(Boolean);
  }

  function cardMatches(card, filters) {
    if (filters.direction) {
      var dirs = attrTokens(card, "data-direction");
      if (dirs.indexOf(filters.direction) === -1) return false;
    }
    if (filters.location) {
      var locs = attrTokens(card, "data-location");
      if (locs.indexOf(filters.location) === -1) return false;
    }
    if (filters.format) {
      var formats = attrTokens(card, "data-format");
      if (formats.indexOf(filters.format) === -1) return false;
    }
    return true;
  }

  function apply(filters) {
    filters = sanitizeFilters(filters);
    var visible = 0;
    cards.forEach(function (card) {
      var match = cardMatches(card, filters);
      card.hidden = !match;
      if (match) visible += 1;
    });

    if (countEl) countEl.textContent = pluralCount(visible);

    var empty = visible === 0;
    if (emptyEl) emptyEl.hidden = !empty;
    if (listEl) listEl.hidden = empty;

    writeUrl(filters);
    appliedFilters = {
      direction: filters.direction,
      location: filters.location,
      format: filters.format,
    };
  }

  function syncFromControls() {
    var filters = readControls();
    setControls(filters);
    apply(filters);
  }

  function resetAll() {
    var empty = { direction: "", location: "", format: "" };
    setControls(empty);
    apply(empty);
  }

  function focusableIn(container) {
    return Array.prototype.slice
      .call(
        container.querySelectorAll(
          'a[href], button:not([disabled]), select:not([disabled]), textarea:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )
      )
      .filter(function (el) {
        return !el.hasAttribute("disabled") && el.offsetParent !== null;
      });
  }

  function lockScroll(lock) {
    if (lock) {
      previousOverflow = document.documentElement.style.overflow;
      document.documentElement.style.overflow = "hidden";
      document.body.style.overflow = "hidden";
    } else {
      document.documentElement.style.overflow = previousOverflow || "";
      document.body.style.overflow = "";
    }
  }

  function enableTrap(enable) {
    if (trapHandler) {
      document.removeEventListener("keydown", trapHandler, true);
      trapHandler = null;
    }
    if (!enable || !panel) return;
    trapHandler = function (e) {
      if (e.key !== "Tab" || panel.hidden) return;
      var nodes = focusableIn(panel);
      if (!nodes.length) return;
      var first = nodes[0];
      var last = nodes[nodes.length - 1];
      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      } else if (document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", trapHandler, true);
  }

  function setPanelOpen(open, opts) {
    opts = opts || {};
    if (!panel || !openBtn) return;

    if (!open && !opts.keepDirty) {
      setControls(appliedFilters);
    }

    panel.hidden = !open;
    openBtn.setAttribute("aria-expanded", open ? "true" : "false");
    lockScroll(open);
    enableTrap(open);

    if (open) {
      setControls(appliedFilters);
      var first = panel.querySelector("select, button");
      if (first) first.focus();
    } else {
      openBtn.focus();
    }
  }

  var formEl = document.getElementById("vacancies-filter-form");
  if (formEl) {
    formEl.addEventListener("submit", function (e) {
      e.preventDefault();
      syncFromControls();
    });
  }

  var initial = readUrl();
  setControls(initial);
  apply(initial);

  fieldNames.forEach(function (name) {
    selectsFor(name).forEach(function (el) {
      el.addEventListener("change", function () {
        var value = el.value || "";
        selectsFor(name).forEach(function (peer) {
          peer.value = value;
        });
        // Desktop: apply immediately; mobile panel waits for Apply
        if (!panel || panel.hidden) {
          apply(readControls());
        }
      });
    });
  });

  resetBtns.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      resetAll();
      if (panel && !panel.hidden) setPanelOpen(false, { keepDirty: true });
    });
  });

  if (openBtn && panel) {
    openBtn.addEventListener("click", function () {
      setPanelOpen(true);
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      setPanelOpen(false);
    });
  }

  if (panel) {
    panel.addEventListener("click", function (e) {
      if (e.target === panel) setPanelOpen(false);
    });
  }

  if (applyBtn) {
    applyBtn.addEventListener("click", function () {
      syncFromControls();
      setPanelOpen(false, { keepDirty: true });
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && panel && !panel.hidden) {
      setPanelOpen(false);
    }
  });

  window.addEventListener("popstate", function () {
    var filters = readUrl();
    setControls(filters);
    apply(filters);
  });
})();
