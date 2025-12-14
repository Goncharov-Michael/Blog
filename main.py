import datetime
import os
from email.message import EmailMessage
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from forms import NewBlogForm, RegisterForm, LoginForm, CommentForm
from tables import db, BlogPost, User, Comment
from dotenv import load_dotenv
from smtplib import SMTP


load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")

"""INITIALIZE FLASK(APP)"""
app = Flask(__name__)
ckeditor = CKEditor()
ckeditor.init_app(app)
app.config["SECRET_KEY"] = os.getenv("FLASK_KEY")
Bootstrap5(app)


"""INITIALIZE DB"""
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///posts.db")
db.init_app(app)


"""CREATE TABLES"""
with app.app_context():
    db.create_all()


"""INITIALIZE LOGIN MANAGER"""
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""GRAVATAR"""
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


"""DECORATOR"""
def admin_only(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)

        return func(*args, **kwargs)

    return wrapper


"""ROUTES"""
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # Get data from form
        email = register_form.email.data
        password = generate_password_hash(register_form.password.data, method="pbkdf2:sha256", salt_length=8)
        name = register_form.name.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        # Check if email is not used
        if user:
            flash("You've already signed up with that email, log in instead!", "error")
            return redirect(url_for("login"))

        new_user = User(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts", current_user=current_user))

    return render_template("register.html", form=register_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == login_form.email.data)).scalar()
        password = login_form.password.data

        if not user:
            flash("That email does not exist, please try again.", "error")
            return redirect(url_for("login"))

        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.", "error")
            return redirect(url_for("login"))

        else:
            login_user(user)
            return redirect(url_for("get_all_posts", current_user=current_user))


    return render_template("login.html", form=login_form, current_user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("get_all_posts", current_user=current_user))


@app.route("/")
def get_all_posts():
    """"""
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    """"""
    post = db.get_or_404(BlogPost, post_id)
    comments = post.comments
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You must be logged in to comment.", "error")
            return redirect(url_for("login"))

        new_comment = Comment(text=comment_form.text.data, author_id=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("show_post", post_id=post_id))

    return render_template("post.html", post=post, form=comment_form,
                           comments=comments, gravatar=gravatar)


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """"""
    form = NewBlogForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            author=current_user,
            subtitle=form.subtitle.data,
            date=datetime.datetime.now().strftime("%b %d, %Y"),
            body=form.body.data,
            img_url=form.img_url.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))

    return render_template("make-post.html", form=form, create=True)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """"""
    post = db.get_or_404(BlogPost, post_id)
    form = NewBlogForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )

    if form.validate_on_submit():
        # Update the Post
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        db.session.commit()

        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=form, create=False)


@app.route('/delete-post/<int:post_id>')
@admin_only
def delete_post(post_id):
    """"""
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    """"""
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """"""

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        send_message(name, email, phone, message)
        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html", msg_sent=False)


def send_message(name, user_email, phone, message):
        # Configure user message
        msg = EmailMessage()
        msg["Subject"] = "New Message"
        msg["From"] = user_email
        msg["To"] = EMAIL
        msg.set_content(f"Name: {name}\n"
                        f"Email: {user_email}\n"
                        f"Phone: {phone}\n"
                        f"Message: {message}")

        # Send message
        with SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)


if __name__ == "__main__":
    app.run(debug=False, port=5002)