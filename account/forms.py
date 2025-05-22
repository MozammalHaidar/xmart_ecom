from django import forms
from .models import Custom_user

class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text="Leave blank if you don't want to change the password."
    )

    class Meta:
        model = Custom_user
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_password(self):
        # This ensures an empty password won't overwrite the existing one
        password = self.cleaned_data.get('password')
        return password if password else None

