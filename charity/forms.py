from django import forms
from .models import Project, Club, Program, BlogPost, Article, NewsletterSubscription, School
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['category', 'image', 'title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force image to be required in the form even if model allows blank/null
        self.fields['image'].required = True

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['school', 'icon', 'image', 'title', 'description', 'location', 'meeting_schedule', 'coordinator', 'member_count']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Club description and activities'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meeting location'}),
            'meeting_schedule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Every Friday 3-5 PM'}),
            'coordinator': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Club coordinator/leader'}),
            'member_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'location', 'image', 'badge', 'description', 'partnership_date', 'contact_person', 'contact_email', 'contact_phone', 'website', 'student_population']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School location/address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief description about the school'}),
            'partnership_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person at school'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact email'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact phone number'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'School website'}),
            'student_population': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['category', 'image', 'title', 'description']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Write your article...'}),
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Email Address',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Your Name (Optional)',
                'required': False
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = False
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists and is active
            existing = NewsletterSubscription.objects.filter(email=email, is_active=True).first()
            if existing:
                raise ValidationError('This email is already subscribed to our newsletter.')
        return email
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subscription_source = 'website'
        if commit:
            instance.save()
        return instance
