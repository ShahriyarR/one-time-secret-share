from django import forms


class SecretCreateForm(forms.Form):
    secret = forms.CharField(
        label=False,
        required=True,
        widget=forms.widgets.Input(
            attrs={
                "placeholder": "Add your secret",
                "class": "input is-large is-focused",
            }
        ),
        max_length=200,
    )
