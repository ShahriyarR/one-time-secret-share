from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template, request, url_for

from onetime.entrypoints.web_flask.forms import SecretCreateForm
from onetime.use_cases.exceptions import (
    SecretDataWasAlreadyConsumedException,
    URLExpiredException,
    UUIDNotFoundException,
)
from onetime.use_cases.manager import SecretAndUrlManager

blueprint = Blueprint("secret", __name__, url_prefix="/")


@blueprint.after_request
def add_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    # response.headers['Cache-Control'] = 'public, max-age=31536000'
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Content-Type"] = "nosniff"
    return response


@blueprint.route("/", methods=["GET", "POST"])
@inject
def index(
    secret_and_url_manager: SecretAndUrlManager = Provide["secret_and_url_manager"],
):
    form = SecretCreateForm()
    if request.method == "POST":
        form = SecretCreateForm(request.form)
        if form.validate_on_submit():
            data = form.secret.data
            uuid = secret_and_url_manager.generate_secret_and_url(data)
            secret_url = url_for("secret.secret", uuid=uuid, _external=True)
            return render_template(
                "onetimesecrets/index.html", form=form, secret_url=secret_url
            )

    return render_template("onetimesecrets/index.html", form=form)


@blueprint.route("/secret/<string:uuid>", methods=["GET", "POST"])
@inject
def secret(
    uuid: str,
    secret_and_url_manager: SecretAndUrlManager = Provide["secret_and_url_manager"],
):
    if request.method == "POST":
        try:
            data = secret_and_url_manager.get_secret(uuid)
        except (
            UUIDNotFoundException,
            SecretDataWasAlreadyConsumedException,
            URLExpiredException,
        ) as e:
            return render_template("onetimesecrets/400.html", message=str(e)), 400

        return render_template("onetimesecrets/show_secret.html", secret_data=data)

    return render_template("onetimesecrets/show_secret.html")
