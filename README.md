# One Time Secret Share

> Live Demo of this project(development stage):
> 
> https://one-time-secret-share.herokuapp.com/

--------

> Live demo got A+ from SecurityHeaders:
> 
> https://securityheaders.com/?q=https%3A%2F%2Fone-time-secret-share.herokuapp.com%2F&followRedirects=on

One time secret sharing service on top of [ReadOnce objects](https://github.com/ShahriyarR/py-read-once), ensures following features:

* We do not log secrets and any kind of user activities.

* We do not save secrets and any kind of user activities to any kind of local and remote storage.

* Each secret is encrypted with per-secret unique key.

* The secret can be only read once, there is no second chance.

* Each secret URL created with random string and encrypted with unique key(try to create same secret data multiple times, you can see that URLs are unique).

* Secret URLs expire in 2 hours. After 2 hours secret URL will be invalidated.

* Found an issue? bug? Please open an issue in this repo.

## Self-deployment for internal secret share

As there are increasing concerns how to share the secret between employees, 
it can be a great idea to host this application internally and use it behind some secure network as well.

The web layer is based on Django with security best practices and the secret object itself is secure by design.
As the application does not store anything, there is no need for database connection and database migrations, there is no admin panel etc.

The demo application deployed on heroku using following commands:

```
* flit install --deps=production
* python3 src/onetime/entrypoints/web/manage.py collectstatic
* cd src/onetime/entrypoints/web/; gunicorn --workers=1 app.wsgi`
```

See [Procfile](./Procfile) for Heroku steps.

> Check the demo link: https://one-time-secret-share.herokuapp.com/

## How to install for development?

We use flit for package management.

Activate virtualenv, with your preferred way and install flit:

```
python3.10 -m venv .venv
source .venv/bin/activate

pip install flit==3.8.0
```

We use Makefile for automation procedures. Please see the Makefile in the repo for further details.

But to install this project with development dependencies:

`make install-dev`

With production dependencies:

`make install`

## How to run tests?

`make test` - for non-slow and non-integration tests

`make test-slow` - for running slow marked tests

## How to run the server?

For running development server:

`make run-dev`

For running with gunicorn:

`make run`

## TODO lists

* Ensure incident reports
