from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.config['SECRET_KEY'] = 's3cr3t_k3y'

from .views import *
from .form import *
# talisman = Talisman(app, force_https=True)
# talisman = Talisman(app,frame_options='SAMEORIGIN')

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# SELF = "'self'"
# talisman = Talisman(
#     app,
#     content_security_policy={
#         'default-src': SELF,
#         'img-src': '*',
#         'script-src': [
#             SELF,
#             'some.cdn.com',
#         ],
#         'style-src': [
#             SELF,
#             'another.cdn.com',
#         ],
#     },
#     content_security_policy_nonce_in=['script-src'],
#     feature_policy={
#         'geolocation': '\'none\'',
#     }
# )

@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# Güvenlik ayarları
app.config['SECURE_PROXY_SSL_HEADER'] = ("HTTP_X_FORWARDED_PROTO", "https")
app.config['SECURE_SSL_REDIRECT'] = True
app.config['SECURE_CONTENT_TYPE_NOSNIFF'] = True
app.config['SECURE_BROWSER_XSS_FILTER'] = True
app.config['SECURE_REFERRER_POLICY'] = "same-origin"
app.config['SECURE_HSTS_SECONDS'] = 2592000
app.config['SECURE_HSTS_INCLUDE_SUBDOMAINS'] = True
app.config['SECURE_HSTS_PRELOAD'] = True

# security settings

app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_AGE'] = 5 * 60
app.config['SESSION_COOKIE_DOMAIN'] = "one-time-secret-share.herokuapp.com"
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = "Strict"
app.config['SESSION_COOKIE_NAME'] = "__Secure-sessionid"

# Upload settings
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 
app.config['MAX_NUMBER_FIELDS'] = 2

# Content Security Policy (CSP) settings
app.config['CSP'] = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "https://cdn.jsdelivr.net"],
    'style-src': ["'self'", "https://cdn.jsdelivr.net"],
    'img-src': ["'self'"],
    'form-action': ["'self'"],
    'frame-ancestors': ["'none'"],
    'block-all-mixed-content': True
}

# CSRF settings
app.config['WTF_CSRF_TIME_LIMIT'] = 2 * 60 * 60
app.config['WTF_CSRF_METHODS'] = ["POST"]
app.config['WTF_CSRF_COOKIE_SECURE'] = True
app.config['WTF_CSRF_COOKIE_HTTPONLY'] = True
app.config['WTF_CSRF_COOKIE_SAMESITE'] = "Strict"
app.config['WTF_CSRF_COOKIE_NAME'] = "__Secure-csrftoken"
app.config['WTF_CSRF_HEADER_NAME'] = "X-CSRFToken"


app.config['X-FRAME_HEADER_NAME'] = "SAMEORIGIN"

# CORS settings


CORS(app, origins=[
    "https://one-time-secret-share.herokuapp.com",
    "http://127.0.0.1:5000",
], methods=["GET"], supports_credentials=False, max_age=1 if app.debug else 60)

# Permissions Policy settings
app.config['Permissions-Policy'] = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

