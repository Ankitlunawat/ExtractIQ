import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent
SECRET_KEY=os.environ.get("SECRET_KEY","local-development-only-do-not-deploy")
DEBUG=os.environ.get("DEBUG","1")=="1"
ALLOWED_HOSTS=os.environ.get("ALLOWED_HOSTS","localhost,127.0.0.1,testserver").split(",")
INSTALLED_APPS=["django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","core"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF="urls"
DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
STATIC_URL="/static/"
STATICFILES_DIRS=[BASE_DIR/"static"]
USE_TZ=True
TIME_ZONE="Asia/Kolkata"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
LOGIN_URL="/accounts/login/"
LOGIN_REDIRECT_URL="/extractiq/"
LOGOUT_REDIRECT_URL="/accounts/login/"
if not DEBUG:
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
    SECURE_SSL_REDIRECT=True
