
from flask import request, url_for, render_template, session
from .app import app
from .form import SecretCreateForm
from dependency_injector.wiring import Provide, inject
from onetime.configurator.containers import Container
from onetime.use_cases.manager import SecretAndUrlManager

#exceptions
from onetime.use_cases.exceptions import (
    SecretDataWasAlreadyConsumedException,
    URLExpiredException,
    UUIDNotFoundException,
)


@app.route('/', methods=['GET', 'POST'])
@inject
def index():
    form = SecretCreateForm()
    if request.method == "POST":
        form = SecretCreateForm(request.form)
        if not form.validate_on_submit():
            container = Container()
            secret_and_url_manager = container.secret_and_url_manager()
            data = form.secret.data
            uuid = secret_and_url_manager.generate_secret_and_url(data)
            secret_url = url_for("secret", uuid=uuid, _external=True)
            return render_template("onetimesecrets/index.html", form=form, secret_url=secret_url)
    
    return render_template("onetimesecrets/index.html", form=form)


@app.route("/secret/<string:uuid>", methods=["GET", "POST"])
@inject
def secret(uuid):
    container = Container()
    secret_and_url_manager = container.secret_and_url_manager()
    if request.method == "POST":
        try:
            data = secret_and_url_manager.get_secret(uuid)
        except (UUIDNotFoundException, SecretDataWasAlreadyConsumedException, URLExpiredException) as e:
            return render_template("onetimesecrets/400.html", message=str(e)), 400

        return render_template("onetimesecrets/show_secret.html", secret_data=data)

    return render_template("onetimesecrets/show_secret.html")