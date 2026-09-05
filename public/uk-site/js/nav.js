/**
 * Mobile nav drawer toggle.
 * Without JS: skip-link + CTA remain usable; section nav links also in footer.
 * Labels follow <html lang> (uk | en).
 * Open: focus first link, trap Tab, inert main+footer; Escape / link closes.
 */
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var drawer = document.getElementById("nav-drawer");
  if (!toggle || !drawer) return;

  var isEn = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0;
  var labelOpen = isEn ? "Open menu" : "Відкрити меню";
  var labelClose = isEn ? "Close menu" : "Закрити меню";
  var main = document.querySelector("main");
  var footer = document.querySelector(".site-footer");
  var trapHandler = null;
  var wasOpen = false;

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

  function enableTrap(enable) {
    if (trapHandler) {
      document.removeEventListener("keydown", trapHandler, true);
      trapHandler = null;
    }
    if (!enable) return;
    trapHandler = function (e) {
      if (e.key !== "Tab" || drawer.hidden) return;
      var nodes = focusableIn(drawer);
      if (!nodes.length) return;
      var first = nodes[0];
      var last = nodes[nodes.length - 1];
      if (e.shiftKey) {
        if (document.activeElement === first || !drawer.contains(document.activeElement)) {
          e.preventDefault();
          last.focus();
        }
      } else if (document.activeElement === last || !drawer.contains(document.activeElement)) {
        e.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", trapHandler, true);
  }

  function setBackgroundInert(inert) {
    if (main) main.inert = inert;
    if (footer) footer.inert = inert;
  }

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? labelClose : labelOpen);
    drawer.classList.toggle("is-open", open);
    drawer.hidden = !open;
    setBackgroundInert(open);
    enableTrap(open);

    if (open) {
      var first = drawer.querySelector("a[href]");
      if (first) first.focus();
      wasOpen = true;
    } else if (wasOpen) {
      toggle.focus();
      wasOpen = false;
    }
  }

  setOpen(false);

  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") !== "true";
    setOpen(open);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
    }
  });

  drawer.addEventListener("click", function (e) {
    var link = e.target.closest("a");
    if (link && drawer.contains(link)) setOpen(false);
  });
})();
