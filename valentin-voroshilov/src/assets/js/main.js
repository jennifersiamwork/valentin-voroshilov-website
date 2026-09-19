(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* -----------------------------------------------------------
     Sticky header scroll state
     ----------------------------------------------------------- */
  var header = document.querySelector("[data-site-header]");
  if (header) {
    var onScroll = function () {
      if (window.scrollY > 40) {
        header.classList.add("is-scrolled");
      } else {
        header.classList.remove("is-scrolled");
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* -----------------------------------------------------------
     Mobile menu
     ----------------------------------------------------------- */
  var menuToggle = document.querySelector("[data-menu-toggle]");
  var mobileMenu = document.querySelector("[data-mobile-menu]");

  function closeMenu() {
    if (!mobileMenu) return;
    mobileMenu.classList.remove("is-open");
    mobileMenu.setAttribute("aria-hidden", "true");
    if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
    if (header) header.classList.remove("is-open");
    document.documentElement.style.overflow = "";
  }

  function openMenu() {
    if (!mobileMenu) return;
    mobileMenu.classList.add("is-open");
    mobileMenu.setAttribute("aria-hidden", "false");
    if (menuToggle) menuToggle.setAttribute("aria-expanded", "true");
    if (header) header.classList.add("is-open");
    document.documentElement.style.overflow = "hidden";
  }

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener("click", function () {
      var isOpen = menuToggle.getAttribute("aria-expanded") === "true";
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    mobileMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
  }

  /* -----------------------------------------------------------
     Smooth in-page scroll with header offset
     ----------------------------------------------------------- */
  document.querySelectorAll('a[href^="#"][data-scroll], a[href^="/#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var hash = link.getAttribute("href").split("#")[1];
      var target = document.getElementById(hash);
      if (!target) return;
      e.preventDefault();
      var offset = (header ? header.offsetHeight : 0) + 12;
      var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top: top, behavior: prefersReducedMotion ? "auto" : "smooth" });
    });
  });

  /* -----------------------------------------------------------
     Reveal on scroll
     ----------------------------------------------------------- */
  var revealTargets = document.querySelectorAll("[data-reveal], [data-reveal-group]");
  if (revealTargets.length) {
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              io.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.15, rootMargin: "0px 0px -60px 0px" }
      );
      revealTargets.forEach(function (el) {
        el.classList.add(el.hasAttribute("data-reveal-group") ? "reveal-group" : "reveal");
        io.observe(el);
      });
    } else {
      revealTargets.forEach(function (el) {
        el.classList.add("is-visible");
      });
    }
  }

  /* -----------------------------------------------------------
     Category filter (gallery + previous work)
     ----------------------------------------------------------- */
  document.querySelectorAll("[data-filter-bar]").forEach(function (bar) {
    var container = bar.parentElement.querySelector("[data-gallery]");
    if (!container) return;
    var items = container.querySelectorAll("[data-category]");

    bar.querySelectorAll("[data-filter]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var filter = btn.getAttribute("data-filter");

        bar.querySelectorAll("[data-filter]").forEach(function (b) {
          b.classList.remove("is-active");
          b.setAttribute("aria-selected", "false");
        });
        btn.classList.add("is-active");
        btn.setAttribute("aria-selected", "true");

        items.forEach(function (item) {
          var match = filter === "all" || item.getAttribute("data-category") === filter;
          if (match) {
            item.removeAttribute("hidden");
          } else {
            item.setAttribute("hidden", "");
          }
        });
      });
    });
  });

  /* -----------------------------------------------------------
     Lightbox
     ----------------------------------------------------------- */
  var lightboxRoot = document.querySelector("[data-lightbox-root]");
  if (lightboxRoot) {
    var lbImage = lightboxRoot.querySelector("[data-lightbox-image]");
    var lbCaption = lightboxRoot.querySelector("[data-lightbox-caption]");
    var lbClose = lightboxRoot.querySelector("[data-lightbox-close]");
    var lbPrev = lightboxRoot.querySelector("[data-lightbox-prev]");
    var lbNext = lightboxRoot.querySelector("[data-lightbox-next]");
    var triggers = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
    var currentIndex = 0;
    var lastFocused = null;

    function getVisibleTriggers() {
      return triggers.filter(function (t) {
        return t.offsetParent !== null;
      });
    }

    function showAt(index) {
      var visible = getVisibleTriggers();
      if (!visible.length) return;
      currentIndex = (index + visible.length) % visible.length;
      var el = visible[currentIndex];
      lbImage.src = el.getAttribute("href");
      lbImage.alt = el.getAttribute("data-caption") || "";
      lbCaption.textContent = el.getAttribute("data-caption") || "";
    }

    function openLightbox(index) {
      lastFocused = document.activeElement;
      showAt(index);
      lightboxRoot.classList.add("is-open");
      lightboxRoot.setAttribute("aria-hidden", "false");
      document.documentElement.style.overflow = "hidden";
      if (lbClose) lbClose.focus();
    }

    function closeLightbox() {
      lightboxRoot.classList.remove("is-open");
      lightboxRoot.setAttribute("aria-hidden", "true");
      document.documentElement.style.overflow = "";
      if (lastFocused) lastFocused.focus();
    }

    triggers.forEach(function (trigger, i) {
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        openLightbox(getVisibleTriggers().indexOf(trigger));
      });
    });

    if (lbClose) lbClose.addEventListener("click", closeLightbox);
    if (lbPrev) lbPrev.addEventListener("click", function () { showAt(currentIndex - 1); });
    if (lbNext) lbNext.addEventListener("click", function () { showAt(currentIndex + 1); });

    lightboxRoot.addEventListener("click", function (e) {
      if (e.target === lightboxRoot) closeLightbox();
    });

    document.addEventListener("keydown", function (e) {
      if (!lightboxRoot.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowLeft") showAt(currentIndex - 1);
      if (e.key === "ArrowRight") showAt(currentIndex + 1);
    });
  }

  /* -----------------------------------------------------------
     Booking form — progressive enhancement for Netlify Forms
     ----------------------------------------------------------- */
  var bookingForm = document.querySelector("[data-booking-form]");
  if (bookingForm) {
    bookingForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var formData = new FormData(bookingForm);
      var body = new URLSearchParams();
      formData.forEach(function (value, key) {
        body.append(key, value);
      });

      fetch(bookingForm.getAttribute("action") || "/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body.toString(),
      })
        .then(function () {
          var success = document.querySelector("[data-form-success]");
          bookingForm.hidden = true;
          if (success) {
            success.hidden = false;
            success.scrollIntoView({ behavior: prefersReducedMotion ? "auto" : "smooth", block: "center" });
          }
        })
        .catch(function () {
          // Fall back to a normal form submission if the request fails
          bookingForm.submit();
        });
    });
  }
})();
