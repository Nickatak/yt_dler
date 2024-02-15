"""At this time, we're not using flask-login.  TODO: implement auth system."""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app.forms.auth import LoginForm, NewUserForm
from app.models import User

auth = Blueprint(
    "auth",
    __file__,
    url_prefix="/auth",
)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)

            return redirect(url_for("yt_dler.upload"))
        else:
            form.password.errors.append("Invalid Username/Password.")

    return render_template("auth/login.html", form=form)


@auth.route("/new_user", methods=["GET", "POST"])
def new_user():
    form = NewUserForm()

    if form.validate_on_submit():
        User(form.username.data, form.email.data, form.password.data).save()

    return render_template("auth/new_user.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
