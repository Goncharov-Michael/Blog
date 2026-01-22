from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class NewBlogForm(FlaskForm):
    """Form for creating or editing a blog post. Uses CKEditor for rich text editing in the post body."""
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Blog Post SubTitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    button = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    """Form for user registration."""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("SIGN ME UP!")


class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):
    """Form to submit comments on a blog post."""
    text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")