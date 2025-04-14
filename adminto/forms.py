from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from api.models import Page
class MyProfileForm(forms.ModelForm):
    password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput,
        required=False,  # Make it optional
        help_text='Leave blank if you do not want to change your password.'
    )

    class Meta:
        model = get_user_model()
        fields = ['full_name', 'password', 'email', 'profile_file']  # Add other fields as necessary

    def __init__(self, *args, **kwargs):
        super(MyProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True  # Disable email field

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if both password fields are filled and match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super(MyProfileForm, self).save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class PageForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    type_id = forms.ChoiceField(choices=[(1, 'Terms of Service'), (2, 'Privacy Policy'), (3, 'About Us'), (4, 'FAQ')], required=True)
    description = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.page_id = kwargs.pop('page_id', None)  # get page_id if passed
        super().__init__(*args, **kwargs)

    def clean_type_id(self):
        type_id = self.cleaned_data.get('type_id')
        qs = Page.objects.filter(type_id=type_id)
        if self.page_id:
            qs = qs.exclude(id=self.page_id)
        if qs.exists():
            raise forms.ValidationError("A page with this type already exists.")
        return type_id
    
class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New password and confirmation do not match.")

        return cleaned_data
    
    