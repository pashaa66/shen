import uuid

from django.core.files.storage import default_storage

_EXT = {'JPEG': 'jpg', 'PNG': 'png', 'WEBP': 'webp'}


def save_custom_image(uploaded):
    """Сохраняет загруженную картинку под случайным именем. Расширение берём из реального формата файла."""
    name = f'custom/{uuid.uuid4().hex}.{_EXT[uploaded.image.format]}'
    return default_storage.save(name, uploaded)
