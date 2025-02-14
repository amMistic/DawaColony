from django import forms
from .models import Product

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["seller", "slug", "created_at", "updated_at"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product Name",
                }
            ),
            
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product Description",
                    "rows": 4,
                }
            ),
            
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product Price (INR)",
                }
            ),
            
            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control", 
                    "placeholder": "Total Stock Avaliable"
                }
            ),
            
            "image": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),
            
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }


class TableSearch(forms.Form):
    search_query = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder' : 'Search Product',
                'class' : 'form-control'
            }
        )
    )
    
    category = forms.ChoiceField(
        choices=[('','All Category')] + list(Product.CATEGORY_CHOICES),
        required=False,
        widget=forms.Select(
            attrs={
                'class' : 'form-select'
            }
        )
    )