/* =========================================================================
   ASHA SWEET CENTER — SHARED FRONT-END BEHAVIOUR
   Vanilla JS, no build step. Works across all page templates.
   NOTE: Cart/wishlist state here is a lightweight in-memory demo for the
   prototype. On Shopify, wire these hooks to Ajax Cart API / theme sections.
   ========================================================================= */
(function () {
  "use strict";

  var state = {
    cartCount: 2,
    cartItems: [
      { name: "Luxurious Mysore Pak", variant: "Premium Tin Box · 500g", price: 490, qty: 1, img: "assets/images/placeholders/product-mysore-pak.svg" },
      { name: "Kaju Badam Mix Sweets", variant: "500g · ASC 102", price: 800, qty: 1, img: "assets/images/placeholders/product-kaju-badam-mix.svg" }
    ],
    wishlist: {}
  };

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    initMegaMenuTouch();
    initSearchToggle();
    initCartDrawer();
    initWishlist();
    initQuickAdd();
    initAccordions();
    initTabs();
    initFilterDrawer();
    initPincodeChecker();
    initPredictiveSearch();
    initQtyStepper();
    initStickyAddBar();
    initBackToTop();
    initNewsletterForms();
    initVariantChips();
    initGallerySwap();
    initTocScrollSpy();
    initSeoSchema();
    renderCartCount();
  });

  /* ---------------- Mobile nav ---------------- */
  function initMobileNav() {
    var btn = document.querySelector(".hamburger");
    var drawer = document.querySelector("#mobileNavDrawer");
    var overlay = document.querySelector("#mobileNavOverlay");
    if (!btn || !drawer) return;
    function open() { drawer.classList.add("open"); overlay && overlay.classList.add("open"); document.body.style.overflow = "hidden"; }
    function close() { drawer.classList.remove("open"); overlay && overlay.classList.remove("open"); document.body.style.overflow = ""; }
    btn.addEventListener("click", open);
    drawer.querySelectorAll("[data-close-drawer]").forEach(function (el) { el.addEventListener("click", close); });
    overlay && overlay.addEventListener("click", close);
  }

  /* ---------------- Search icon → overlay toggle ---------------- */
  function initSearchToggle() {
    var overlay = document.querySelector("#searchOverlay");
    var toggles = document.querySelectorAll("[data-search-toggle]");
    if (!overlay || !toggles.length) return;
    function open() {
      overlay.classList.add("open");
      toggles.forEach(function (t) { t.setAttribute("aria-expanded", "true"); });
      var input = overlay.querySelector("input[data-search-input]");
      input && setTimeout(function () { input.focus(); }, 50);
    }
    function close() {
      overlay.classList.remove("open");
      toggles.forEach(function (t) { t.setAttribute("aria-expanded", "false"); });
    }
    toggles.forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        overlay.classList.contains("open") ? close() : open();
      });
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    document.addEventListener("click", function (e) {
      if (overlay.classList.contains("open") && !overlay.contains(e.target) && ![].some.call(toggles, function (t) { return t.contains(e.target); })) close();
    });
  }

  /* ---------------- Mega menu on touch devices ---------------- */
  function initMegaMenuTouch() {
    document.querySelectorAll(".header-nav > li").forEach(function (li) {
      var menu = li.querySelector(".mega-menu");
      if (!menu) return;
      var link = li.querySelector(":scope > a, :scope > button.nav-toggle");
      if (!link) return;
      link.addEventListener("click", function (e) {
        if (window.matchMedia("(hover: none)").matches) {
          e.preventDefault();
          li.classList.toggle("touch-open");
          menu.style.opacity = li.classList.contains("touch-open") ? 1 : "";
          menu.style.visibility = li.classList.contains("touch-open") ? "visible" : "";
        }
      });
    });
  }

  /* ---------------- Cart drawer ---------------- */
  function initCartDrawer() {
    var drawer = document.querySelector("#cartDrawer");
    var overlay = document.querySelector("#cartOverlay");
    var openBtns = document.querySelectorAll("[data-open-cart]");
    var closeBtns = drawer ? drawer.querySelectorAll("[data-close-drawer]") : [];
    if (!drawer) return;

    function render() {
      var body = drawer.querySelector(".cart-items-list");
      var subtotalEl = drawer.querySelector(".cart-subtotal-value");
      if (!body) return;
      if (state.cartItems.length === 0) {
        body.innerHTML = '<div class="empty-state"><p>Your cart is empty.</p><a href="collection-detail.html" class="btn btn-primary">Shop Sweets</a></div>';
        if (subtotalEl) subtotalEl.textContent = "₹0";
        return;
      }
      var html = "";
      var subtotal = 0;
      state.cartItems.forEach(function (item, i) {
        subtotal += item.price * item.qty;
        html += '<div class="cart-item" data-index="' + i + '">' +
          '<img src="' + item.img + '" alt="' + item.name + '">' +
          '<div class="info"><span class="name">' + item.name + '</span>' +
          '<div class="variant">' + item.variant + '</div>' +
          '<div class="qty-stepper" data-cart-qty><button type="button" data-step="-1" aria-label="Decrease quantity">−</button><span class="qty-val">' + item.qty + '</span><button type="button" data-step="1" aria-label="Increase quantity">+</button></div>' +
          '</div><div><strong>₹' + (item.price * item.qty) + '</strong><br><button class="btn-link" data-remove style="font-size:12px;margin-top:6px;">Remove</button></div></div>';
      });
      body.innerHTML = html;
      if (subtotalEl) subtotalEl.textContent = "₹" + subtotal.toLocaleString("en-IN");

      body.querySelectorAll(".cart-item").forEach(function (row) {
        var idx = +row.dataset.index;
        row.querySelectorAll("[data-step]").forEach(function (b) {
          b.addEventListener("click", function () {
            state.cartItems[idx].qty = Math.max(1, state.cartItems[idx].qty + (+b.dataset.step));
            recalcCartCount(); render(); renderCartCount();
          });
        });
        var rm = row.querySelector("[data-remove]");
        rm && rm.addEventListener("click", function () {
          state.cartItems.splice(idx, 1); recalcCartCount(); render(); renderCartCount();
        });
      });
    }

    function recalcCartCount() {
      state.cartCount = state.cartItems.reduce(function (a, i) { return a + i.qty; }, 0);
    }

    function open() { render(); drawer.classList.add("open"); overlay && overlay.classList.add("open"); document.body.style.overflow = "hidden"; }
    function close() { drawer.classList.remove("open"); overlay && overlay.classList.remove("open"); document.body.style.overflow = ""; }

    openBtns.forEach(function (b) { b.addEventListener("click", function(e){ e.preventDefault(); open(); }); });
    closeBtns.forEach(function (b) { b.addEventListener("click", close); });
    overlay && overlay.addEventListener("click", close);

    window._openCartDrawer = open;
    window._addToCart = function (product) {
      var existing = state.cartItems.find(function (i) { return i.name === product.name && i.variant === product.variant; });
      if (existing) existing.qty += 1; else state.cartItems.push(Object.assign({ qty: 1 }, product));
      recalcCartCount(); renderCartCount(); showToast(product.name + " added to cart");
      open();
    };
  }

  function renderCartCount() {
    document.querySelectorAll(".cart-count").forEach(function (el) { el.textContent = state.cartCount; });
  }

  /* ---------------- Quick add / Add to cart buttons ---------------- */
  function initQuickAdd() {
    document.querySelectorAll("[data-add-to-cart]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var card = btn.closest("[data-product]");
        var product = {
          name: (card && card.dataset.name) || btn.dataset.name || "Product",
          variant: (card && card.dataset.variant) || btn.dataset.variant || "Default",
          price: +((card && card.dataset.price) || btn.dataset.price || 0),
          img: (card && card.dataset.img) || btn.dataset.img || "assets/images/placeholders/product-mysore-pak.svg"
        };
        window._addToCart(product);
      });
    });
  }

  /* ---------------- Wishlist ---------------- */
  function initWishlist() {
    document.querySelectorAll(".wishlist-btn").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        btn.classList.toggle("active");
        showToast(btn.classList.contains("active") ? "Added to wishlist" : "Removed from wishlist");
      });
    });
  }

  /* ---------------- Accordions ---------------- */
  function initAccordions() {
    document.querySelectorAll(".accordion-trigger").forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        var item = trigger.closest(".accordion-item");
        var group = item.parentElement;
        var singleOpen = group.dataset.singleOpen === "true";
        if (singleOpen) {
          group.querySelectorAll(".accordion-item.open").forEach(function (el) { if (el !== item) el.classList.remove("open"); });
        }
        item.classList.toggle("open");
      });
    });
  }

  /* ---------------- Tabs ---------------- */
  function initTabs() {
    document.querySelectorAll(".tabs-nav").forEach(function (nav) {
      var panelsWrap = document.querySelector(nav.dataset.tabsFor);
      if (!panelsWrap) return;
      nav.querySelectorAll("button").forEach(function (btn) {
        btn.addEventListener("click", function () {
          nav.querySelectorAll("button").forEach(function (b) { b.classList.remove("active"); });
          btn.classList.add("active");
          panelsWrap.querySelectorAll(".tab-panel").forEach(function (p) { p.classList.remove("active"); });
          var panel = panelsWrap.querySelector('[data-tab-panel="' + btn.dataset.tab + '"]');
          panel && panel.classList.add("active");
        });
      });
    });
  }

  /* ---------------- Filter drawer (mobile) ---------------- */
  function initFilterDrawer() {
    var drawer = document.querySelector("#filterDrawer");
    var overlay = document.querySelector("#filterOverlay");
    var openBtns = document.querySelectorAll("[data-open-filters]");
    if (!drawer) return;
    function open() { drawer.classList.add("open"); overlay && overlay.classList.add("open"); document.body.style.overflow = "hidden"; }
    function close() { drawer.classList.remove("open"); overlay && overlay.classList.remove("open"); document.body.style.overflow = ""; }
    openBtns.forEach(function (b) { b.addEventListener("click", open); });
    drawer.querySelectorAll("[data-close-drawer]").forEach(function (b) { b.addEventListener("click", close); });
    overlay && overlay.addEventListener("click", close);

    document.querySelectorAll(".filter-group h4[data-collapsible]").forEach(function (h) {
      h.addEventListener("click", function () {
        var body = h.nextElementSibling;
        if (body) body.style.display = body.style.display === "none" ? "" : "none";
      });
    });
  }

  /* ---------------- PIN code delivery checker ---------------- */
  function initPincodeChecker() {
    document.querySelectorAll("[data-pincode-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var input = form.querySelector("input");
        var resultEl = form.parentElement.querySelector(".delivery-info");
        var val = (input.value || "").trim();
        if (!/^\d{6}$/.test(val)) {
          if (resultEl) resultEl.textContent = "Please enter a valid 6-digit PIN code.";
          return;
        }
        var bengaluru = val.charAt(0) === "5" && val.charAt(1) === "6";
        if (resultEl) {
          resultEl.innerHTML = bengaluru
            ? "✓ Hyperlocal delivery available in approx. <strong>45 minutes</strong> for Bengaluru PIN " + val + ". Standard delivery: 3 days."
            : "✓ Delivery available to PIN " + val + " in approx. <strong>6–7 days</strong>.";
        }
      });
    });
  }

  /* ---------------- Predictive search (mock dataset) ---------------- */
  var SEARCH_INDEX = [
    { name: "Luxurious Mysore Pak", price: 490, img: "assets/images/placeholders/product-mysore-pak.svg" },
    { name: "Kaju Burfi 250g", price: 360, img: "assets/images/placeholders/product-kaju-burfi.svg" },
    { name: "Motichur Laddu 200g", price: 215, img: "assets/images/placeholders/product-motichur-laddu.svg" },
    { name: "Soan Papdi 250g", price: 215, img: "assets/images/placeholders/product-soan-papdi.svg" },
    { name: "Premium Baklava 250g", price: 480, img: "assets/images/placeholders/product-baklava.svg" },
    { name: "Navarathan Mixture", price: 65, img: "assets/images/placeholders/product-navarathan-mixture.svg" },
    { name: "Chow Chow", price: 128, img: "assets/images/placeholders/product-chow-chow.svg" },
    { name: "Cashew Burfi", price: 360, img: "assets/images/placeholders/product-cashew-burfi.svg" },
    { name: "Roasted Almonds", price: 340, img: "assets/images/placeholders/product-roasted-almonds.svg" },
    { name: "Dry Fruit Gift Box", price: 950, img: "assets/images/placeholders/product-dryfruit-giftbox.svg" },
    { name: "Kaju Badam Mix Sweets 500g", price: 800, img: "assets/images/placeholders/product-kaju-badam-mix.svg" }
  ];
  function initPredictiveSearch() {
    document.querySelectorAll("[data-search-input]").forEach(function (input) {
      var scope = input.closest(".search-overlay-inner, .search-hero") || input.closest(".header-search");
      var resultsBox = (scope && scope.querySelector(".search-results")) ||
        (scope && scope.parentElement && scope.parentElement.querySelector(".search-results")) ||
        (input.dataset.resultsTarget ? document.querySelector(input.dataset.resultsTarget) : null);
      if (!resultsBox) return;
      input.addEventListener("input", function () {
        var q = input.value.trim().toLowerCase();
        if (!q) { resultsBox.classList.remove("open"); resultsBox.innerHTML = ""; return; }
        var matches = SEARCH_INDEX.filter(function (p) { return p.name.toLowerCase().indexOf(q) !== -1; }).slice(0, 5);
        if (matches.length === 0) {
          resultsBox.innerHTML = '<div class="search-result-row"><div class="name">No products found for "' + escapeHtml(input.value) + '"</div></div>';
        } else {
          resultsBox.innerHTML = matches.map(function (p) {
            return '<div class="search-result-row"><img src="' + p.img + '" alt=""><div><span class="name">' + p.name + '</span><br><span class="price">₹' + p.price + '</span></div></div>';
          }).join("");
        }
        resultsBox.classList.add("open");
      });
      document.addEventListener("click", function (e) {
        if (!input.contains(e.target) && !resultsBox.contains(e.target)) resultsBox.classList.remove("open");
      });
    });
  }

  /* ---------------- Quantity stepper (PDP) ---------------- */
  function initQtyStepper() {
    document.querySelectorAll("[data-qty-stepper]").forEach(function (stepper) {
      var valEl = stepper.querySelector(".qty-val");
      stepper.querySelectorAll("button").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var val = parseInt(valEl.textContent, 10) || 1;
          val = Math.max(1, val + (+btn.dataset.step));
          valEl.textContent = val;
        });
      });
    });
  }

  /* ---------------- Sticky add-to-cart bar (PDP, mobile) ---------------- */
  function initStickyAddBar() {
    var bar = document.querySelector("#stickyAddBar");
    var trigger = document.querySelector("#pdpBuyBox");
    if (!bar || !trigger) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (window.innerWidth > 600) { bar.style.display = "none"; return; }
        bar.style.display = entry.isIntersecting ? "none" : "flex";
      });
    }, { threshold: 0 });
    io.observe(trigger);
    bar.querySelectorAll("[data-add-to-cart]").forEach(function () {}); // reuse initQuickAdd binding already attached globally
  }

  /* ---------------- Back to top ---------------- */
  function initBackToTop() {
    var btn = document.querySelector(".back-to-top");
    if (!btn) return;
    window.addEventListener("scroll", function () {
      btn.classList.toggle("show", window.scrollY > 700);
    });
    btn.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  /* ---------------- Newsletter / enquiry forms (demo submit) ---------------- */
  function initNewsletterForms() {
    document.querySelectorAll("[data-demo-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var msg = form.dataset.successMessage || "Thank you! We'll be in touch shortly.";
        showToast(msg);
        form.reset();
      });
    });
  }

  /* ---------------- Variant chips (PDP) ---------------- */
  function initVariantChips() {
    document.querySelectorAll(".variant-options").forEach(function (group) {
      group.querySelectorAll(".variant-chip:not(.unavailable)").forEach(function (chip) {
        chip.addEventListener("click", function () {
          group.querySelectorAll(".variant-chip").forEach(function (c) { c.classList.remove("selected"); });
          chip.classList.add("selected");
        });
      });
    });
  }

  /* ---------------- Gallery thumb swap (PDP) ---------------- */
  function initGallerySwap() {
    var main = document.querySelector(".pdp-gallery-main img");
    if (!main) return;
    document.querySelectorAll(".pdp-thumbs img").forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        document.querySelectorAll(".pdp-thumbs img").forEach(function (t) { t.classList.remove("active"); });
        thumb.classList.add("active");
        main.src = thumb.src;
      });
    });
  }

  /* ---------------- TOC scroll-spy (blog detail) ---------------- */
  function initTocScrollSpy() {
    var tocLinks = document.querySelectorAll(".toc a");
    if (!tocLinks.length) return;
    var sections = Array.prototype.map.call(tocLinks, function (l) { return document.querySelector(l.getAttribute("href")); }).filter(Boolean);
    window.addEventListener("scroll", function () {
      var y = window.scrollY + 140;
      var activeIdx = 0;
      sections.forEach(function (s, i) { if (s.offsetTop <= y) activeIdx = i; });
      tocLinks.forEach(function (l, i) { l.classList.toggle("active", i === activeIdx); });
    });
  }

  /* ---------------- SEO/GEO: auto-generated structured data ----------------
     Reads the page's own rendered breadcrumbs and FAQ accordions and emits
     BreadcrumbList / FAQPage JSON-LD, so every template gets correct schema
     without hand-maintaining it per page. ---------------------------------- */
  function initSeoSchema() {
    var BASE_URL = "https://www.ashasweetcenter.com/";

    var crumbNav = document.querySelector(".breadcrumbs");
    if (crumbNav) {
      var items = [];
      crumbNav.querySelectorAll("a").forEach(function (a, i) {
        items.push({ "@type": "ListItem", "position": i + 1, "name": a.textContent.trim(), "item": a.href });
      });
      var current = crumbNav.querySelector(".current");
      if (current) items.push({ "@type": "ListItem", "position": items.length + 1, "name": current.textContent.trim() });
      if (items.length) {
        appendSchema({ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items });
      }
    }

    document.querySelectorAll(".faq-list").forEach(function (list) {
      var qas = [];
      list.querySelectorAll(".accordion-item").forEach(function (item) {
        var qEl = item.querySelector(".accordion-trigger");
        var aEl = item.querySelector(".accordion-panel-inner");
        if (!qEl || !aEl) return;
        var qText = qEl.textContent.replace(/[+]\s*$/, "").trim();
        qas.push({ "@type": "Question", "name": qText, "acceptedAnswer": { "@type": "Answer", "text": aEl.textContent.trim() } });
      });
      if (qas.length) {
        appendSchema({ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qas });
      }
    });

    function appendSchema(obj) {
      var s = document.createElement("script");
      s.type = "application/ld+json";
      s.textContent = JSON.stringify(obj);
      document.head.appendChild(s);
    }
    void BASE_URL;
  }

  /* ---------------- Toast ---------------- */
  var toastTimer;
  function showToast(message) {
    var toast = document.querySelector("#toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "toast";
      toast.className = "toast";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("show"); }, 2400);
  }

  function escapeHtml(s) { return s.replace(/[&<>"']/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]; }); }

  window.AshaUI = { showToast: showToast };
})();
