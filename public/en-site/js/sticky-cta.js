/**
 * Sticky mobile CTA after ~40% hero scroll; hide near #contact / footer.
 * Always attach listeners so resize desktop→mobile still works.
 * Toggles body.sticky-cta-active as :has() fallback for older WebKit.
 */
(function () {
  var bar = document.getElementById("sticky-cta");
  var hero = document.querySelector(".hero");
  var contact = document.getElementById("contact");
  if (!bar || !hero || !contact) return;

  var mq = window.matchMedia("(min-width: 1024px)");

  function update() {
    if (mq.matches) {
      bar.classList.remove("is-visible");
      bar.hidden = true;
      document.body.classList.remove("sticky-cta-active");
      return;
    }

    var heroRect = hero.getBoundingClientRect();
    var heroH = hero.offsetHeight || 1;
    var scrolledPast = -heroRect.top / heroH >= 0.4;

    var contactRect = contact.getBoundingClientRect();
    var nearContact = contactRect.top < window.innerHeight * 0.85;

    var show = scrolledPast && !nearContact;
    bar.classList.toggle("is-visible", show);
    bar.hidden = !show;
    document.body.classList.toggle("sticky-cta-active", show);
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      update();
      ticking = false;
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  if (typeof mq.addEventListener === "function") {
    mq.addEventListener("change", update);
  } else if (typeof mq.addListener === "function") {
    mq.addListener(update);
  }
  update();
})();
