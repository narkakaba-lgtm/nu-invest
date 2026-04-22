from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Asset, Project


# ===============================
# 1. INSCRIPTION
# ===============================
class InscriptionForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Obligatoire pour recevoir les confirmations.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email


# ===============================
# 2. FORMULAIRE ASSET
# ===============================
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['title', 'category', 'description', 'price', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Chaîne YouTube 50k'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Le prix doit être supérieur à 0.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image trop lourde (max 2MB).")

            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("Fichier invalide. Upload une image.")

        return image


# ===============================
# 3. FORMULAIRE PROJET (CORRIGÉ)
# ===============================
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name',
            'description',
            'jobs_to_create',
            'amount_needed',
            'image'   # ✅ CORRECTION ICI
        ]

        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'jobs_to_create': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_needed': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_jobs_to_create(self):
        jobs = self.cleaned_data.get('jobs_to_create')
        if jobs is None or jobs <= 0:
            raise forms.ValidationError("Le nombre d’emplois doit être supérieur à 0.")
        return jobs

    def clean_amount_needed(self):
        amount = self.cleaned_data.get('amount_needed')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Le montant doit être positif.")
        return amount

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if image.size > 3 * 1024 * 1024:
                raise forms.ValidationError("Image trop lourde (max 3MB).")

            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("Fichier invalide.")

        return image