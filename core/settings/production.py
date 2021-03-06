import dj_database_url
import os

# Local
DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get("DATABASE_URL"))
# Production
# DEFAULT_CONNECTION = dj_database_url.parse('')

DATABASES = {"default": DEFAULT_CONNECTION, }

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

GITHUB_AUTH = {
               "username": os.environ.get("GITHUB_USER"),
               "token": os.environ.get("GITHUB_TOKEN")
               }