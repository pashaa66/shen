(function () {
  const els = Array.from(document.querySelectorAll(".unfold"));
  if (!els.length) return;

  const open = (el) => el.classList.add("is-open");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) { els.forEach(open); return; }

  let started = false;
  function go() {
    if (started) return;
    started = true;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { open(en.target); io.unobserve(en.target); }
      });
    }, { threshold: 0.05 });
    els.forEach((el) => io.observe(el));
    setTimeout(() => els.forEach(open), 4000);   // страховка
  }

  const loader = document.getElementById("loader");
  if (!loader || document.documentElement.classList.contains("no-loader")) { go(); return; }

  const mo = new MutationObserver(() => {
    if (loader.classList.contains("is-hidden")) { mo.disconnect(); go(); }
  });
  mo.observe(loader, { attributes: true, attributeFilter: ["class"] });
  setTimeout(() => { mo.disconnect(); go(); }, 6000);
})();