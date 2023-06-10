# One Time Secret Share

> Live Demo of this project(development stage):
> 
> https://one-time-secret-share.herokuapp.com/

One time secret sharing service on top of [ReadOnce objects](https://github.com/ShahriyarR/py-read-once), ensures following features:

* We do not log secrets and any kind of user activities.

* We do not save secrets and any kind of user activities to any kind of local and remote storage.

* Each secret is encrypted with per-secret unique key.

* The secret can be only read once, there is no second chance.

* Each secret URL created with random string and encrypted with unique key(try to create same secret data multiple times, you can see that URLs are unique).

* Secret URLs expire in 2 hours. After 2 hours secret URL will be invalidated.

* Found an issue? bug? Please open an issue in this repo.

## How to install?

We use flit for package management.

Activate virtualenv, with your preferred way and install flit:

```
python3.10 -m venv .venv
source .venv/bin/activate

pip install flit=3.8.0
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

* Deploy to production with custom domain
* Ensure incident reports