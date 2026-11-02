(function () {
  const root = document.getElementById("game");
  if (!root) return;

  const dogBox = document.getElementById("game-dog");
  const dog = dogBox.querySelector(".dog");
  const hint = document.getElementById("game-hint");
  const scoreEl = document.getElementById("game-score");
  const hiEl = document.getElementById("game-hi");

  const GRAVITY = 2400, JUMP_V = 760;
  const DOG_LEFT = 40, DOG_W = 96;

  let state = "idle";            // idle | running | over
  let y = 0, vy = 0, speed = 0, score = 0;
  let last = 0, sinceSpawn = 0, gap = 400, lockUntil = 0;
  let obstacles = [];
  let hi = 0;

  try { hi = parseInt(localStorage.getItem("shen_hi") || "0", 10) || 0; } catch (e) {}
  hiEl.textContent = hi;

  function spawn() {
    const w = 18 + Math.random() * 16;
    const h = 26 + Math.random() * 28;
    const el = document.createElement("div");
    el.className = "game__obs";
    el.style.width = w + "px";
    el.style.height = h + "px";
    root.appendChild(el);
    obstacles.push({ el, x: root.clientWidth + 10, w, h });
    gap = Math.max(300, speed * (0.75 + Math.random() * 0.8));
    sinceSpawn = 0;
  }

  function start() {
    obstacles.forEach((o) => o.el.remove());
    obstacles = [];
    y = 0; vy = 0; score = 0; speed = 360; sinceSpawn = 0; gap = 400;
    scoreEl.textContent = "0";
    hint.hidden = true;
    state = "running";
    last = performance.now();
    requestAnimationFrame(frame);
  }

  function gameOver() {
    state = "over";
    lockUntil = performance.now() + 400;
    dog.classList.remove("dog--run");
    const final = Math.floor(score);
    if (final > hi) {
      hi = final;
      hiEl.textContent = hi;
      try { localStorage.setItem("shen_hi", String(hi)); } catch (e) {}
    }
    hint.textContent = "Щен споткнулся. Тапни или нажми пробел, чтобы начать заново";
    hint.hidden = false;
  }

  function frame(t) {
    if (state !== "running") return;
    const dt = Math.min((t - last) / 1000, 0.05);
    last = t;

    speed = Math.min(720, speed + 10 * dt);
    score += (speed * dt) / 10;
    scoreEl.textContent = Math.floor(score);

    // прыжок
    vy -= GRAVITY * dt;
    y += vy * dt;
    if (y <= 0) { y = 0; vy = 0; }
    dog.classList.toggle("dog--run", y === 0);
    dogBox.style.transform = `translateY(${-y}px)`;

    // препятствия
    sinceSpawn += speed * dt;
    if (sinceSpawn >= gap) spawn();

    const dl = DOG_LEFT + 16, dr = DOG_LEFT + DOG_W - 12;
    for (const o of obstacles) {
      o.x -= speed * dt;
      o.el.style.transform = `translateX(${o.x}px)`;
      if (o.x < dr && o.x + o.w > dl && y < o.h - 6) return gameOver();
    }
    obstacles = obstacles.filter((o) => {
      if (o.x + o.w < -10) { o.el.remove(); return false; }
      return true;
    });

    requestAnimationFrame(frame);
  }

  function action() {
    if (state === "running") {
      if (y === 0) vy = JUMP_V;
    } else if (performance.now() >= lockUntil) {
      start();
    }
  }

  root.addEventListener("pointerdown", (e) => { e.preventDefault(); action(); });
  document.addEventListener("keydown", (e) => {
    if (e.code !== "Space" && e.code !== "ArrowUp") return;
    const tag = (e.target.tagName || "").toLowerCase();
    if (["input", "textarea", "select", "button", "a"].includes(tag)) return;
    e.preventDefault();
    action();
  });
})();