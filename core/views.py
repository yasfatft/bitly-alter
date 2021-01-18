import json
from flask import *
from flask_login import login_required, current_user, login_user, logout_user

from core.models import *
from core.logic import *
from core.app import app, db, redis_configure, login_manager, client


def build_template_context():
    try:
        user_email = current_user._get_current_object().email
        context = {'user_email': user_email}
    except:
        context = {'user_email': "Nobody!"}
    return context


@app.route('/')
def index():
    context = build_template_context()
    return render_template('index.html', context=context)


@app.route('/v1/urls/shorten/', methods=['POST'])
@login_required
def shorten_url():
    owner_id = current_user._get_current_object().id
    form = request.form
    long_url = form['long_url']
    url_existence, urls = find_url_with_long_url_and_owner(long_url, owner_id)
    if url_existence:
        flash(urls[0].__str__())
        context = build_template_context()
        return render_template('index.html', context=context)
    short_url = generate_unique_short_url(long_url)
    url = Url(long_url=long_url, short_url=short_url, owner_id=owner_id)
    add_to_database(url)
    redis_configure.add_to_redis(url.short_url, url.long_url)
    flash(url.__str__())
    context = build_template_context()
    return render_template('index.html', context=context)


@app.route('/<regex("([a-z]|[A-Z]|\d){8}"):short_url>/')
def redirect_to_long_url(short_url):
    long_url = get_long_url(redis_configure, short_url)
    if not long_url:
        abort(404)
    return redirect(long_url)


@login_manager.user_loader
def user_loader(user_id):
    """
    Given *user_id*, return the associated User object.
    :param unicode user_id: user_id user to retrieve
    """
    return User.query.get(user_id)



@app.route("/v1/login", methods=["POST"])
def login():
    """Login the user by processing the form."""
    form = request.form
    email: str = form['email']
    password: str = form['password']
    try:
        user = User.query.filter_by(email=email).all()[0]
    except:
        flash("There is no user registerd with this email address!")
        context = build_template_context()
        return render_template('index.html', context=context)
    else:
        if check_password(password, user.password):
            user.authenticated = True
            add_to_database(user)
            login_user(user, remember=True)
            flash("You logged in!")
            context = build_template_context()
            return render_template('index.html', context=context)
        else:
            flash("We belive you entered wrong password!")
            context = build_template_context()
            return render_template('index.html', context=context)


@app.route("/v1/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    add_to_database(user)
    logout_user()
    flash("You logged out!")
    context = build_template_context()
    return render_template('index.html', context=context)


@app.route('/v1/register/', methods=['POST'])
def register():
    """Register user by processing the form."""
    form = request.form
    email: str = form['email']
    password: str = form['password']
    try:
        user = User.query.filter_by(email=email).all()[0]
    except:
        hashed_password = hash_password(password)
        user = User(email=email,
                    password=hashed_password.decode())
        user.authenticated = True
        add_to_database(user)
        login_user(user, remember=True)
        flash("You registerd successfully!")
        context = build_template_context()
        return render_template('index.html', context=context)
    else:
        flash("There is a user registerd with this email address!")
        context = build_template_context()
        return render_template('index.html', context=context)
