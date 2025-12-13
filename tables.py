from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class BlogPost(db.Model):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    author:Mapped["User"] = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post",
                                               cascade="all, delete", passive_deletes=True)

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True)
    name: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(250))

    # ---------Add parent relationship---------
    # "post_author" refer to the post_author property(author) in the BlogPost class.
    # "comment_author" refers to the comment_author property in the Comment class.
    posts: Mapped[list["BlogPost"]] = relationship("BlogPost", back_populates="author",
                                                cascade="all, delete", passive_deletes=True)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author",
                                                     cascade="all, delete", passive_deletes=True)

class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text)

    # ---------Add child relationship---------
    # "users.id" The users refers to the tablename of the Users class.
    # "comments" refers to the comments property in the User class.
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    author: Mapped["User"] = relationship("User", back_populates="comments")

    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_post.id", ondelete="CASCADE"))
    post: Mapped["BlogPost"] = relationship("BlogPost", back_populates="comments")