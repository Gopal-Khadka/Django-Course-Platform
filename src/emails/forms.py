from django import forms

from .models import Email


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "placeholder": "hello@website.com",
            }
        )
    )

    # class Meta:
    #     model = Email
    #     fields = ["email"]

    def clean_email(self):
        email: str = self.cleaned_data.get("email")
        qs = Email.objects.filter(email__iexact=email, active=False)
        if qs.exists():
            raise forms.ValidationError("Inactive(invalid) email. Try another email. ")
        # if not email.endswith("gmail.com"):
        #     raise forms.ValidationError("Invalid email type. Use 'Gmail' only")
        return email
