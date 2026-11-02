(function () {
  const loader = document.getElementById("loader");
  if (!loader) return;

  const MIN_MS = 2000;
  const start = performance.now();

  function hide() {
    loader.classList.add("is-hidden");
    try { sessionStorage.setItem("shen_loaded", "1"); } catch (e) {}
    setTimeout(() => loader.remove(), 500);
  }
  function done() {
    setTimeout(hide, Math.max(0, MIN_MS - (performance.now() - start)));
  }

  if (document.readyState === "complete") done();
  else window.addEventListener("load", done);
  setTimeout(hide, 8000);
})();
