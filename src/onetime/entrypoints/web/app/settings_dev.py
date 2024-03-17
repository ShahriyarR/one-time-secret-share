from onetime.entrypoints.web.app.settings import *  # noqa

if DEBUG:  # noqa
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

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "formatters": {
            "rich": {"datefmt": "[%X]"},
        },
        "handlers": {
            "console": {
                "class": "rich.logging.RichHandler",
                "filters": ["require_debug_true"],
                "formatter": "rich",
                "level": "DEBUG",
                "rich_tracebacks": True,
                "tracebacks_show_locals": True,
            },
        },
        "loggers": {
            "django": {
                "handlers": [],
                "level": "INFO",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
