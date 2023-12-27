from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class SecretCreateForm(FlaskForm):
    secret = StringField(
        label=False,
        validators=[DataRequired(), Length(max=200)],
        render_kw={
            "placeholder": "Add your secret",
            "class": "input is-large is-focused",
        },
    )
