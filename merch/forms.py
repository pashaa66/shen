from django import forms

from .models import Variant

MAX_UPLOAD_MB = 10
ALLOWED_FORMATS = ('JPEG', 'PNG', 'WEBP')


class AddToCartForm(forms.Form):
    variant = forms.ChoiceField(
        choices=Variant.choices,
        initial=Variant.STANDARD,
        widget=forms.RadioSelect,
    )
    text = forms.CharField(
        label='Текст на открытке',
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    image = forms.ImageField(
        label='Ваша картинка',
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'accept': 'image/jpeg,image/png,image/webp'}
        ),
    )
    quantity = forms.IntegerField(
        label='Количество', min_value=1, max_value=20, initial=1
    )

    def __init__(self, *args, product, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        if not product.allows_text:
            del self.fields['text']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > MAX_UPLOAD_MB * 1024 * 1024:
                raise forms.ValidationError(f'Файл больше {MAX_UPLOAD_MB} МБ.')
            if image.image.format not in ALLOWED_FORMATS:
                raise forms.ValidationError('Подходят только JPG, PNG и WEBP.')
        return image

    def clean(self):
        cleaned = super().clean()
        variant = cleaned.get('variant')

        if (
            self.product.allows_text
            and not (cleaned.get('text') or '').strip()
        ):
            self.add_error('text', 'Введите текст открытки.')

        if (
            variant == Variant.CUSTOM
            and not cleaned.get('image')
            and 'image' not in self.errors
        ):
            self.add_error('image', 'Загрузите картинку для этого варианта.')
        if variant == Variant.STANDARD:
            cleaned['image'] = None
        return cleaned
