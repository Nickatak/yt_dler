from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class YoutubeURLForm(FlaskForm):
    """Form to start a youtube download."""

    yt_url = StringField(
        label="Youtube Link:",
        validators=[
            InputRequired(),
        ],
        render_kw={
            "class_": "yt_url",
            "aria-label": "download url",
            "placeholder": "Youtube URL",
        },
    )
