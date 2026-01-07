# Flask Blog Application

A full-stack personal blog platform built with Python and Flask. It provides user registration, login/logout, and an admin interface for creating, editing, and deleting blog posts.

## Features

- User Authentication: Users can register and log in using Flask-Login. Passwords are securely hashed with Werkzeug.

- Admin Role: The first registered user (ID=1) acts as admin. Only the admin can access routes for creating, editing, or deleting posts (enforced by a custom admin_only decorator).

- Blog Management: Admins can write posts with a title, subtitle, image URL, and rich text content (using CKEditor). Regular users can read posts and authors are credited on each post.

- Comments: Authenticated users can leave comments on any post. Each Comment is linked to its author and the corresponding BlogPost. Deleting a post or user cascades to delete related comments.

- Contact Form: A “Contact” page collects messages (name, email, phone, message) and sends them via Gmail SMTP. The backend handles form validation and email delivery.

- Database: Uses SQLAlchemy ORM (a “SQL toolkit and ORM”) with a SQLite (or configurable) database. Data models include User, BlogPost, and Comment with one-to-many relationships and cascade deletes for integrity.

- Responsive UI: Built with Flask-Bootstrap 5 for a modern, responsive design. Flask-Gravatar generates user avatars. The layout focuses on readability, using Bootstrap cards and grids for posts.

- Security & Config: Routes are protected with Flask-Login’s @login_required decorator. Sensitive settings (SECRET_KEY, email credentials) are loaded from a .env file via python-dotenv

### Tech Stack

- Runtime: Python 3.10+ (WSGI) — Flask application server.

- Language: Python.

- Frontend: Jinja2 templates(HTML) + Flask-Bootstrap 5 (CSS), CKEditor (rich-text editor), Flask-Gravatar (avatar rendering).

- Database & Auth: SQLAlchemy ORM, Flask-Login for session management; Werkzeug for password hashing.

- Forms & Validation: Flask-WTF (WTForms) + Flask-CKEditor for rich text fields.

- Email / SMTP: smtplib.

- Configuration: python-dotenv.

- CI/CD: GitHub Actions (Automated Testing & Deployment).

- Hosting: Render (backend).


## Quick Start
### Prerequisites

- Python 3.10+
- Git

### Installations
1. Clone the repository\
git clone https://github.com/Goncharov-Michael/Blog.git

2. Install Dependencies\
pip install -r requirements.txt

3. Environment setup
Create a .env file in the project root and with your configuration:
- FLASK_KEY
- DB_URI
- EMAIL
- EMAIL_PASSWORD

4. Run the App:\
python main.py

## Architecture Overview
### Frontend
- Built with Jinja2 templates + Flask-Bootstrap 5
- Uses CKEditor for rich-text blog content
- Gravatar integration for user avatars
- Handles forms and validation via Flask-WTF

### Backend
- Built with Python 3.10+ + Flask
- Handles user authentication (Flask-Login + Werkzeug password hashing)
- CRUD for blog posts (admin only for creating, editing, deleting posts)
- Handles comments for posts
- Handles contact form emails via SMTP

### Blog Tables
| Table           | Purpose                                                                  |
| -------------   | ------------------------------------------------------------------------ |
| `User`          | Stores user accounts and authentication info                             |
| `BlogPost`      | Stores blog posts with title, subtitle, content, author, image, and date |
| `Comment`       | Stores comments linked to users and posts                                |


### Key Routes & Functionality

- `/` – Homepage with all blog posts
- `/register` – Register a new user
- `/login` / `/logout` – User authentication
- `/post/<id>` – View a post and submit comments (login required for comments)
- `/new-post`, `/edit-post/<id>`, `/delete-post/<id>` – Admin-only blog management
- `/contact` – Contact form that sends an email


### Environment Variables
| Variable         | Description                                                                                                 
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| `FLASK_KEY`      | Secret key for sessions and CSRF protection                                                                 |
| `DB_URI`         | Database URL |
| `EMAIL`          | Gmail address used to send contact form messages                                                            |
| `EMAIL_PASSWORD` | App password for Gmail (required if sending emails)                                                         |

### License
This project is licensed under the MIT License—see the LICENSE file for details.
