# resume_builder/forms.py
from django import forms
from .models import Resume, Experience
from django.forms import inlineformset_factory

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'
        widgets = {
            'professional_profile': forms.Textarea(attrs={'rows': 6}),
            'skills': forms.Textarea(attrs={'rows': 5}),
            'education': forms.Textarea(attrs={'rows': 5}),
            'why_hire_me': forms.Textarea(attrs={'rows': 6}),
            'socials': forms.Textarea(attrs={'rows': 3}),
        }

ExperienceFormSet = inlineformset_factory(
    Resume, Experience,
    fields=('title', 'company', 'year', 'description'),
    extra=1, can_delete=True
)