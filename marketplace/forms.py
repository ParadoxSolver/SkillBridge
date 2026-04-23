from django import forms
from .models import ServiceListing, Review, Order


class ServiceListingForm(forms.ModelForm):
    """Form for creating/editing a service listing."""
    class Meta:
        model = ServiceListing
        fields = ['title', 'description', 'category', 'price', 'delivery_days', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'e.g. I will design a modern logo',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 5,
                'placeholder': 'Describe your service in detail...',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary bg-white',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': '₹500',
                'min': '1',
            }),
            'delivery_days': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': '3',
                'min': '1',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'logo, branding, graphic design',
            }),
        }


class ReviewForm(forms.ModelForm):
    """Form for submitting a review."""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary bg-white',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 4,
                'placeholder': 'Share your experience...',
            }),
        }


class OrderForm(forms.ModelForm):
    """Form for placing an order."""
    class Meta:
        model = Order
        fields = ['requirements']
        widgets = {
            'requirements': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 5,
                'placeholder': 'Describe your project requirements in detail...',
            }),
        }
