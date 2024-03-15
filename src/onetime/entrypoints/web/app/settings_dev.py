from .settings import *

if DEBUG:
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "corsheaders",
        "debug_toolbar",
        "django_browser_reload",
        "onetimesecrets",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django_permissions_policy.PermissionsPolicyMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "csp.middleware.CSPMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar
        "django_browser_reload.middleware.BrowserReloadMiddleware",  # browser reload
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    INTERNAL_IPS = ["127.0.0.1", "localhost"]
    RESULTS_CACHE_SIZE = 1000
