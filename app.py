"""Flask App for Flask Cafe."""

import os

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, Cafe, City, User
from forms import AddCafeForm, SignupForm, LoginForm, CSRFForm, ProfileEditForm

from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_cafe')
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)


# TODO: fix defualt images upon sign up and add cafe. also populating them in edit
#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_form():
    """CSRF form for every user"""

    g.csrf_form = CSRFForm()

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=["GET", "POST"])
def handle_add_cafe():
    """Show a form for adding a cafe and add to database.
    Redirect to new cafe detail page with submission.flas
    """

    form = AddCafeForm()
    form.city.choices = City.get_choices()

    if form.validate_on_submit():

        new_cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city.data,
            image_url=form.image_url.data or Cafe.image_url.default.arg
            # form.populate_obj(obj)
        )

        db.session.add(new_cafe)
        db.session.commit()
        flash(f"{new_cafe.name} added.")

        return redirect(f"/cafes/{new_cafe.id}")

    return render_template("cafe/add-form.html", form=form)


@app.route("/cafes/<int:cafe_id>/edit", methods=["GET", "POST"])
def handle_edit_cafe(cafe_id):
    """Show form for editing a cafe and add to database.
    Redirect to cafe detail page
    """
    cafe = Cafe.query.get_or_404(cafe_id)
    form = AddCafeForm(obj=cafe)
    form.city.choices = City.get_choices()

    if form.validate_on_submit():
        cafe.name=form.name.data,
        cafe.description=form.description.data,
        cafe.url=form.url.data,
        cafe.address=form.address.data,
        cafe.city_code=form.city.data,
        cafe.image_url=form.image_url.data or Cafe.image_url.default.arg
        # form.populate_obj(cafe)

        db.session.add(cafe)
        db.session.commit()
        flash(f"{cafe.name} edited.")

        return redirect(f"/cafes/{cafe.id}")

    return render_template("cafe/edit-form.html", form=form, cafe=cafe)


#######################################
# users

@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Show registration form and process form.
    Adds user to DB and logs them in. Redirects to cafe list.
    """

    form = SignupForm()

    if form.validate_on_submit():
        try:
            new_user = User.register(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                description=form.description.data,
                email=form.email.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg)

            db.session.add(new_user)
            db.session.commit()

        except IntegrityError:
            flash(f"Username already taken.", 'warning')
            return render_template("auth/signup-form.html", form=form)

        do_login(new_user)

        flash(f"You are signed up and logged in.")
        return redirect("/cafes")

    return render_template("auth/signup-form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Show login form and handle login.
    Redirect to cafe list
    """

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!")
            return redirect("/cafes")

        flash("Invalid credentials")

    return render_template("auth/login-form.html", form=form)


@app.post("/logout")
def logout():
    """Log out user"""

    if not g.user or not g.csrf_form.validate_on_submit():
        flash("Access unauthorized.", "danger")
        return redirect("/")


    do_logout()
    flash("You have successfully logged out")
    return redirect("/cafes")


# All of these routes should check if the web user is logged in; if not, they should redirect to the login form with NOT_LOGGED_IN flashed message.

@app.get("/profile")
def show_user_profile():
    """Show user profile."""
    if not g.user:
        flash(NOT_LOGGED_IN_MSG)
        return redirect("/login")

    return render_template("profile/detail.html", user=g.user)



@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    """SHow edit profile form and process the edit.
    Redirect to to profile page upon successful edit.
    """

    if not g.user:
        flash(NOT_LOGGED_IN_MSG)
        return redirect("/login")

    user=g.user
    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        user.first_name=form.first_name.data
        user.last_name=form.last_name.data
        user.description=form.description.data
        user.email=form.email.data
        user.image_url=form.image_url.data or User.image_url.default.arg

        db.session.commit()

        flash("Profile edited.")
        return redirect("/profile")

    return render_template("profile/edit-form.html", form=form)


