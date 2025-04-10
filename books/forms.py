from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, BookstoreStock


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'password1', )

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = BookstoreStock
        fields = ['stock', 'sold']

