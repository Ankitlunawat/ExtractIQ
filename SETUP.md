# Local setup

Requires Python 3.11+.

1. Create a virtual environment: `python -m venv .venv`.
2. Activate it: Windows `.venv\Scripts\activate`; macOS/Linux `source .venv/bin/activate`.
3. `pip install -r requirements.txt`
4. `python app/manage.py migrate`
5. Set LOCAL_PASSWORD to a local password of your choice. PowerShell: `$env:LOCAL_PASSWORD="your-password"`; bash: `export LOCAL_PASSWORD='your-password'`.
6. `python app/manage.py create_workspace`
7. `python app/manage.py crawl_catalogue --pages 2`

Start with `python app/manage.py runserver`. Open http://127.0.0.1:8000 and sign in as `workspace` with your chosen password. Data persists in SQLite. Run tests with `python app/manage.py test core`.

Before production hosting configure SECRET_KEY, DEBUG=0, ALLOWED_HOSTS, HTTPS and production static-file serving. No hosted live application is deployed.
