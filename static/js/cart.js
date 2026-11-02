document.addEventListener("DOMContentLoaded", () => {
  const content = document.getElementById("cart-content");
  if (!content) return;

  let timer = null;

  async function submitQty(form) {
    const itemId = form.dataset.itemId;
    try {
      const resp = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        credentials: "same-origin",
      });
      if (!resp.ok) throw new Error("bad response");

      // после POST сервер делает redirect на корзину, получаем её свежий HTML
      const doc = new DOMParser().parseFromString(await resp.text(), "text/html");
      const newContent = doc.getElementById("cart-content");
      if (!newContent) throw new Error("no cart");

      content.innerHTML = newContent.innerHTML;

      const newLink = doc.getElementById("cart-link");
      const link = document.getElementById("cart-link");
      if (newLink && link) link.textContent = newLink.textContent;

      const input = content.querySelector(`form[data-item-id="${itemId}"] input`);
      if (input) {
        input.focus();
        input.setSelectionRange?.(input.value.length, input.value.length);
      }
    } catch (e) {
      form.submit(); // запасной вариант: обычная отправка формы
    }
  }

  content.addEventListener("input", (e) => {
    const input = e.target;
    if (!input.matches(".cart-line__qty input")) return;

    const value = parseInt(input.value, 10);
    const min = parseInt(input.min, 10) || 1;
    const max = parseInt(input.max, 10) || 20;
    if (Number.isNaN(value) || value < min || value > max) return; // пока человек печатает

    clearTimeout(timer);
    timer = setTimeout(() => submitQty(input.form), 500);
  });
});