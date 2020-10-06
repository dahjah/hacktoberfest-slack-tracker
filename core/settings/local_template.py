import dj_database_url

# Local
DEFAULT_CONNECTION = dj_database_url.parse('')
# Production
# DEFAULT_CONNECTION = dj_database_url.parse('')

DATABASES = {"default": DEFAULT_CONNECTION, }

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

GITHUB_AUTH = {
               "username": "dahjah@gmail.com",
               "token": "ddbb3d388f4d95b438b6e0cac004e23e9f5b3b0f"
               }

SLACK_CLIENT_ID = ""
SLACK_CLIENT_SECRET = ""
SLACK_CLIENT_REDIRECT_URI = "https://hacktoberfest-tracker.herokuapp.com/slackbot/oauth/"