document.addEventListener("DOMContentLoaded", () => {
  const radios = document.querySelectorAll('input[name="variant"]');
  const imageBlock = document.getElementById("image-block");
  const fileInput = imageBlock ? imageBlock.querySelector('input[type="file"]') : null;
  const preview = document.getElementById("image-preview");
  if (!radios.length || !imageBlock) return;

  const update = () => {
    const checked = document.querySelector('input[name="variant"]:checked');
    imageBlock.hidden = !(checked && checked.value === "custom");
  };
  radios.forEach((r) => r.addEventListener("change", update));
  update();

  if (fileInput && preview) {
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      preview.hidden = !file;
      if (file) preview.src = URL.createObjectURL(file);
    });
  }
});