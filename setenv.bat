DOSKEY init_env=python -m venv venv
DOSKEY init_dependency=pip install -r requirements.txt
DOSKEY act_env=venv\Scripts\activate
DOSKEY run_dev=flask --app app run --host=0.0.0.0 --debug
DOSKEY freeze_version=pip freeze ^> requirements.txt
DOSKEY dummy=python dummy.py

DOSKEY db_init=flask db init
DOSKEY db_migrate=flask db migrate -m $1
DOSKEY db_upgrade=flask db upgrade

venv\Scripts\activate