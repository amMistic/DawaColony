from django import forms
from accounts.models import User


class UpdateSellerForm(forms.ModelForm):
    """
    Form for customer to join our platform - DawaBazaar!
    """

    username = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "Placeholder": "Steff Oberoi"}
        ),
    )

    first_name = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "Placeholder": "Steff "}
        ),
    )

    last_name = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "Placeholder": " Oberoi"}
        ),
    )

    email = forms.EmailField(
        max_length=64,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "oberois.chemist@gmail.com",
            }
        ),
    )

    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+916354785139"}
        ),
    )

    shopname = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "readonly": "readonly",
            }
        ),
    )
    
    address = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "shopname", "address"]



class SellerChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords don't match!")
        return cleaned_data    