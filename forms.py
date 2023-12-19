"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField, SelectField, TextAreaField
from wtforms.validators import InputRequired, URL, Optional


class AddCafeForm(FlaskForm):
    """Form for adding cafes"""

    name = StringField("Cafe name", validators=[InputRequired()])
    description = TextAreaField("Description")
    url = StringField("URL", validators=[Optional(), URL()])
    address = StringField("Address", validators=[InputRequired()])
    city = SelectField("City", validators=[InputRequired()])
    image_url = StringField("Image URL", validators=[Optional(),URL()])