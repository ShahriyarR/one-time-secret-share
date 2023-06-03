from django import forms


class SecretForm(forms.Form):
    secret = forms.CharField(
        label=False,
        required=True,
        widget=forms.widgets.Input(
            attrs={
                "placeholder": "Add your secret",
                "class": "input is-large is-focused",
            }
        ),
    )
