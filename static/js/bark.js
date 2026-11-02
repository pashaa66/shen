(function () {
  const dogBtn = document.getElementById("thanks-dog");
  if (!dogBtn) return;
  const dog = dogBtn.querySelector(".dog");
  const bubble = document.getElementById("bubble");
  const audio = new Audio(dogBtn.dataset.sound);
  audio.preload = "auto";

  function bark() {
    bubble.classList.add("is-visible");
    dog.classList.remove("dog--bark");
    void dog.getBoundingClientRect();
    dog.classList.add("dog--bark");

    audio.currentTime = 0;
    audio.play().catch(() => { /* браузер заблокировал автозвук, сработает по клику */ });
  }

  dogBtn.addEventListener("click", bark);
  setTimeout(bark, 300);
})();