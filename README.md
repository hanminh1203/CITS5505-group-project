# CITS5505-group-project
Group project for CITS5505 Semester 1 - 2026
## Description
This project is a Flask web application for a peer-to-peer skill sharing platform. Its purpose is to help users connect with each others to exchange knowledge, improve their own personal skills. The application is designed around the idea that learning can be collaborative, community-driven, and accessible through simple interactions between users.

From a user perspective, the application supports a workflow where people can register a profile, manage their skills, initialize or response to requests for knowledge exchange. This makes the platform useful for matching learners with peers who are willing to share practical knowledge in a more informal and flexible way than a traditional tutoring system.

### Design perspective
The application uses Flask as the core technical stack in backend server with following plugins:
- SQLAlchemy: database ORM
- Marshmallow: entity serialization
- Flask-Migrate: schema migrations
  
The frontend templates are served through Jinja templates with reusable components.
### File structure
```test
app/
  __init__.py       # Perform intialization of application
  config.py         # Environment-related config
  errors.py         # Error handling
  extensions.py     # Extensions such as database, migration, authentication, csrf,...
  templating.py     # Custom filtering used for Jinja2
  models/           # ORM models
  forms/            # WTForms used on frontend
  schemas/          # Marshmallow schemas served as DTO
  features/         # Feature-based routes
scripts/            # Additional script
  dummy.py          # Optional data seeding
static/             # Static assets such as JS, CSS, Images files
templates/          # HTML Template
  components/       # Reuseable components
  modals/           # Modals view
  pages/            # Page layout of corresponding pages
    base.page.html  # Base layout
run.py              # Flask entrypoint
```

## Members
| UWA ID | Name | Github username |
| -------| -----| ----------------|
| 25112977 | Han Minh Tran | hanminh1203|
| 24112045 | Zihan Jia | misuchii |
| 24350939 | Jianing Wang | zhazha-1004 |

## How to launch
Before launching the application, make sure your environment meets these minimum requirements:

- Python 3.13 or later
- `pip` for installing Python packages
- `venv` for creating an isolated virtual environment
- SQLite support available in Python for the default local database setup

The application is designed to run locally as a Flask server using the dependencies listed in `requirements.txt`.
### How to setup environment
1. Create a Python virtual environment.

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows (CMD):

```shell
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Optional: create a `.env` file in the project root to override configuration values. Example:

```env
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
FLASK_DEBUG=False
WTF_CSRF_SECRET_KEY=$DEFINE-YOUR-OWN-KEY$
SECRET_KEY=$DEFINE-YOUR-OWN-KEY$
```

4. Apply the database migration:

```bash
flask db upgrade
```

5. Optional: seed the database with dummy data:

```bash
python -m scripts.seed_dummy_data
```

6. Start the Flask application:

```bash
flask --app run run
```

7. Open the app in your browser:

```text
http://127.0.0.1:5000
```

Useful routes:
- `/` or `/index.html` for the main app shell
- `/api/users/` for the users API
- `/api/requests/` for the requests API

## How to run the tests
Currently, there are currently no automated tests configured in this repository.
