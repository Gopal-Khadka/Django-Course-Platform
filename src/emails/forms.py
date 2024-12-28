from django import forms

from . import services


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
        verified = services.verify_email(email)
        if verified:
            raise forms.ValidationError("Inactive(invalid) email. Try another email. ")
        return email
