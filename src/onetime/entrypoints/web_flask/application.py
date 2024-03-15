from uuid import uuid4

from cryptography.fernet import Fernet
from flask import Flask
from flask_cors import CORS

from onetime.configurator.containers import Container
from onetime.entrypoints.web_flask.blueprints.views import blueprint as secret_blueprint


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    key = Fernet.generate_key()
    container = Container()
    app.container = container
    app.secret_key = Fernet(key).encrypt(bytes(str(uuid4()), encoding="utf-8"))
    app.register_blueprint(secret_blueprint)
    # set_security_settings(app)
    return app


#
# # security settings
def set_security_settings(app: Flask) -> None:
    app.config["SECURE_PROXY_SSL_HEADER"] = ("HTTP_X_FORWARDED_PROTO", "https")
    app.config["SECURE_SSL_REDIRECT"] = True
    app.config["SECURE_CONTENT_TYPE_NOSNIFF"] = True
    app.config["SECURE_BROWSER_XSS_FILTER"] = True
    app.config["SECURE_REFERRER_POLICY"] = "same-origin"
    app.config["SECURE_HSTS_SECONDS"] = 2592000
    app.config["SECURE_HSTS_INCLUDE_SUBDOMAINS"] = True
    app.config["SECURE_HSTS_PRELOAD"] = True
    app.config["Strict-Transport-Security"] = "public, max-age=31536000"
    app.config["X-Frame-Options"] = "SAMEORIGIN"

    # cookie settings

    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_AGE"] = 5 * 60
    app.config["SESSION_SAVE_EVERY_REQUEST"] = True
    app.config["SESSION_COOKIE_DOMAIN"] = "one-time-secret-share.herokuapp.com"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
    app.config["SESSION_COOKIE_NAME"] = "__Secure-sessionid"

    # Upload settings
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024
    app.config["MAX_NUMBER_FIELDS"] = 2

    # Content Security Policy (CSP) settings
    app.config["CSP"] = {
        "default-src": ["'self'"],
        "script-src": ["'self'", "https://cdn.jsdelivr.net"],
        "style-src": ["'self'", "https://cdn.jsdelivr.net"],
        "img-src": ["'self'"],
        "form-action": ["'self'"],
        "frame-ancestors": ["'none'"],
        "block-all-mixed-content": True,
    }

    # CSRF settings
    app.config["WTF_CSRF_TIME_LIMIT"] = 2 * 60 * 60
    app.config["WTF_CSRF_METHODS"] = ["POST"]
    app.config["WTF_CSRF_COOKIE_SECURE"] = True
    app.config["WTF_CSRF_COOKIE_HTTPONLY"] = True
    app.config["WTF_CSRF_COOKIE_SAMESITE"] = "Strict"
    app.config["WTF_CSRF_COOKIE_NAME"] = "__Secure-csrftoken"
    app.config["WTF_CSRF_HEADER_NAME"] = "X-CSRFToken"

    app.config["X-FRAME_HEADER_NAME"] = "SAMEORIGIN"

    # CORS settings

    CORS(
        app,
        origins=[
            "https://one-time-secret-share.herokuapp.com",
            "http://127.0.0.1:5000",
            "*.ngrok-free.app",
        ],
        methods=["GET"],
        supports_credentials=False,
        max_age=1 if app.debug else 60,
    )

    # Permissions Policy settings
    app.config["Permissions-Policy"] = {
        "accelerometer": None,
        "ambient-light-sensor": None,
        "autoplay": None,
        "camera": None,
        "display-capture": None,
        "document-domain": None,
        "encrypted-media": None,
        "fullscreen": None,
        "geolocation": None,
        "gyroscope": None,
        "interest-cohort": None,
        "magnetometer": None,
        "microphone": None,
        "midi": None,
        "payment": None,
        "usb": None,
    }
