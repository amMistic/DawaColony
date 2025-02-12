from django import forms
from accounts.models import User
from .models import Address


class UpdateCustomerForm(forms.ModelForm):
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

    gender = forms.ChoiceField(
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
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

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "gender", "email", "phone"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["user", "create_at", "updated_at"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full Name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "pincode": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Pincode"}
            ),
            "address_line1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "House No., Building Name",
                }
            ),
            "address_line2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Road name, Area, Colony",
                }
            ),
            "landmark": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Landmark (Optional)"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "address_type": forms.Select(attrs={"class": "form-control"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-class",
            }
        ),
    )

    new_password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-class",
            }
        ),
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-class",
            }
        ),
    )

    def save(self, *args, **kwargs):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if (new_password and confirm_password) and (new_password != confirm_password):
            raise "Password didn't matched!"

        return cleaned_data

