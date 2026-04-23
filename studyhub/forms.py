from django import forms
from .models import Resource


class ResourceUploadForm(forms.ModelForm):
    """Form for uploading a study resource."""
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'category', 'subject', 'course', 'institution', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'e.g. Data Structures — Unit 3 Notes',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'rows': 3,
                'placeholder': 'Brief description of the resource...',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary bg-white',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'e.g. Computer Science, Physics',
            }),
            'course': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'e.g. B.Tech CSE Sem 3',
            }),
            'institution': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'e.g. GTU, Delhi University',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-[3px] border-black rounded-md font-poppins focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'algorithms, sorting, trees',
            }),
        }
