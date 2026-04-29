# Project Structure

This document explains the current folder and file structure of the project.

## Root directory

```text
CITS5505-group-project/
  app/
  configs/
  docs/
  forms/
  instance/
  migrations/
  routes/
  scripts/
  static/
  templates/
  tests/
  app.py
  dummy.py
  models.py
  README.md
  requirements.txt
  run.py
  schemas.py
  structure.md
```

The project is currently organized around a new `app/` package, with a small number of legacy root-level files kept as compatibility wrappers.

## Main application package

```text
app/
  __init__.py
  config.py
  errors.py
  extensions.py
  templating.py
  features/
  forms/
  models/
  schemas/
```

- [app/__init__.py](/D:/UWA/CITS5505/git/CITS5505-group-project/app/__init__.py) contains the Flask application factory `create_app()` and creates the app instance.
- [app/config.py](/D:/UWA/CITS5505/git/CITS5505-group-project/app/config.py) loads environment-based Flask configuration.
- [app/extensions.py](/D:/UWA/CITS5505/git/CITS5505-group-project/app/extensions.py) defines shared Flask extensions such as SQLAlchemy, Marshmallow, Migrate, LoginManager, and CSRF protection.
- [app/errors.py](/D:/UWA/CITS5505/git/CITS5505-group-project/app/errors.py) contains centralized error handlers.
- [app/templating.py](/D:/UWA/CITS5505/git/CITS5505-group-project/app/templating.py) registers template filters.

### Feature modules

```text
app/features/
  api/
  pages/
  requests/
  users/
```

- `api/` builds the top-level `/api` blueprint.
- `pages/` builds the main site/page blueprint for browser-rendered pages.
- `requests/` groups request-related API routes and page routes together.
- `users/` contains user-related routes.

This is the main shift in the current structure: related backend code is now grouped more by feature than by technical layer.

### Models

```text
app/models/
  __init__.py
  enums.py
  mixins.py
  request.py
  skill.py
  user.py
```

- `enums.py` stores shared enum types such as request status and session format.
- `mixins.py` stores reusable model mixins and audit hook registration.
- `user.py`, `skill.py`, and `request.py` define the SQLAlchemy models by domain.
- `__init__.py` re-exports the models for convenient imports.

### Forms

```text
app/forms/
  __init__.py
  request.py
```

- This package contains WTForms definitions.
- `request.py` currently defines the request form used by the request feature.

### Schemas

```text
app/schemas/
  __init__.py
  request.py
```

- This package contains Marshmallow schemas used for API serialization.
- `request.py` currently holds the request-related schema tree, including nested user, skill, and offer schemas.

## Frontend assets

```text
static/
  css/
  js/

templates/
  components/
  modals/
  pages/
```

- `static/` contains frontend assets such as stylesheets and JavaScript.
- `templates/` contains Jinja templates used by Flask.
- `templates/pages/` holds full page templates.
- `templates/components/` holds reusable page fragments.
- `templates/modals/` holds modal fragments.

The frontend structure is still page/component/modal based, which matches the current template and static asset usage.

## Database and runtime folders

```text
instance/
migrations/
```

- `instance/` stores runtime-local files such as the SQLite database.
- `migrations/` contains Flask-Migrate / Alembic migration files and migration configuration.

## Scripts and docs

```text
docs/
scripts/
```

- `docs/` contains project documentation such as specifications and working notes.
- `scripts/` contains utility scripts. Right now it includes the dummy data seeding script.

## Tests

```text
tests/
```

- `tests/` is reserved for automated tests.
- There may still be very little active test coverage, but this is the intended place for unit, integration, or end-to-end tests.

## Root-level files

- [run.py](/D:/UWA/CITS5505/git/CITS5505-group-project/run.py) is the main Flask entrypoint for running the app.
- [app.py](/D:/UWA/CITS5505/git/CITS5505-group-project/app.py) is kept as a compatibility wrapper that exposes the app instance.
- [dummy.py](/D:/UWA/CITS5505/git/CITS5505-group-project/dummy.py) remains as a compatibility entrypoint for seeding data.
- [requirements.txt](/D:/UWA/CITS5505/git/CITS5505-group-project/requirements.txt) lists Python dependencies.
- [README.md](/D:/UWA/CITS5505/git/CITS5505-group-project/README.md) explains how to set up and run the project.

## Summary

The current structure is in a transitional but cleaner state:

- The real application code now lives under `app/`.
- Feature routing is moving toward feature-based organization.
- Older folders and root-level modules still exist to preserve compatibility.
- Frontend templates and assets still follow the existing page/component/modal structure.

For most future work, the best place to add backend code is inside `app/`, not the legacy wrapper folders.
