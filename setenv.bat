DOSKEY init_env=python -m venv venv
DOSKEY init_dependency=pip install -r requirements.txt
DOSKEY act_env=venv\Scripts\activate
DOSKEY run_dev=flask --app run run --host=0.0.0.0 --debug
DOSKEY freeze_version=pip freeze ^> requirements.txt
DOSKEY dummy=python -m scripts.seed_dummy_data
DOSKEY lint1=flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
DOSKEY lint2=flake8 . --count --max-complexity=10 --statistics

DOSKEY db_init=flask db init
DOSKEY db_migrate=flask db migrate -m $*
DOSKEY db_upgrade=flask db upgrade

venv\Scripts\activate