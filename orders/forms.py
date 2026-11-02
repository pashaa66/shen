from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'bank', 'address', 'phone', 'nickname']
        labels = {'bank': 'Банк'}
        widgets = {
            'address': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Индекс, город, улица, дом, квартира',
                }
            ),
            'bank': forms.TextInput(attrs={'list': 'banks'}),
        }
