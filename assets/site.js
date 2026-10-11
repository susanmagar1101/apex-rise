// Apex Rise IT Solution: small scripts shared by every page.
document.addEventListener("DOMContentLoaded", function () {
  // Phone menu: open and close the menu under the top bar.
  var toggle = document.getElementById("menu-toggle");
  var menu = document.getElementById("mobile-menu");
  if (toggle && menu) {
    var icon = toggle.querySelector(".material-symbols-outlined");
    var setOpen = function (open) {
      menu.classList.toggle("hidden", !open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      if (icon) icon.textContent = open ? "close" : "menu";
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1024) setOpen(false);
    });
  }

  // Home page heading: the last word changes every three seconds.
  var word = document.getElementById("rotating-text");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (word && !reduce) {
    var words = ["proactive", "progressive", "professional"];
    var i = 1;
    setInterval(function () {
      word.classList.add("opacity-0", "-translate-y-2");
      word.classList.remove("opacity-100", "translate-y-0");
      setTimeout(function () {
        i = (i + 1) % words.length;
        word.textContent = words[i];
        word.classList.remove("transition-all", "duration-500", "-translate-y-2");
        word.classList.add("translate-y-2");
        void word.offsetWidth;
        word.classList.add("transition-all", "duration-500");
        word.classList.remove("translate-y-2", "opacity-0");
        word.classList.add("translate-y-0", "opacity-100");
      }, 500);
    }, 3000);
  }
});
