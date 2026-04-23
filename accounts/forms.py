from django import forms
from .models import User


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'college_name', 'college_email', 'skills']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Last name',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
            }),
            'college_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Your college/university',
            }),
            'college_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'your.name@college.edu',
            }),
            'skills': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Python, React, UI Design, Video Editing...',
            }),
        }
