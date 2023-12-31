"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )

    @classmethod
    def get_choices(cls):
        """Returns city choices for Flask Form"""

        return [(c.code, c.name) for c in City.query.all()]

class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    url = db.Column(
        db.Text,
        nullable=False,
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey('cities.code'),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-cafe.jpg",
    )

    city = db.relationship("City", backref='cafes')

    #relationship from user to liked cafes and back
    liking_user = db.relationship(
        "User",
        secondary='likes',
        backref="liked_cafes"
    )

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'


class User(db.Model):
    """User of site"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )
    admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    email = db.Column(
        db.String(50),
        nullable=False
    )
    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    description = db.Column(
        db.Text
    )
    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-pic.png"
    )
    password = db.Column(
        db.Text(),
        nullable=False
    )

    def get_full_name(self):
        """Returns a string of  “FIRSTNAME LASTNAME” """

        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls,
                username,
                email,
                first_name,
                last_name,
                description,
                password,
                admin=False,
                image_url=None):
        """Registers a new user and handles password hashing"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            email=email,
            admin=admin,
            first_name=first_name,
            last_name=last_name,
            description=description,
            image_url=image_url,
            password=hashed)

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates user with username and password.
        Returns user instance if user found, False if not """

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Like(db.Model):
    """Maps liked cafe to user"""

    __tablename__ = "likes"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    )
    cafe_id = db.Column(
        db.Integer,
        db.ForeignKey('cafes.id'),
        primary_key=True
    )




def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
