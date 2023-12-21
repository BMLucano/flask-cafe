"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, URL, Optional, Length, Email


class AddCafeForm(FlaskForm):
    """Form for adding cafes"""

    name = StringField("Cafe name", validators=[InputRequired()])
    description = TextAreaField("Description")
    url = StringField("URL", validators=[Optional(), URL()])
    address = StringField("Address", validators=[InputRequired()])
    city = SelectField("City", validators=[InputRequired()])
    image_url = StringField("Image URL", validators=[Optional(),URL()])


class SignupForm(FlaskForm):
    """Form for user sign up"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
    )
    first_name = StringField(
        "First name",
        validators=[InputRequired(), Length(max=20)]
    )
    last_name = StringField(
        "Last name",
        validators=[InputRequired(), Length(max=20)]
    )
    description = TextAreaField("Description")
    email = StringField(
        "Email",
        validators=[InputRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)]
    )
    image_url = StringField("Image URL", validators=[URL()])


class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)]
    )