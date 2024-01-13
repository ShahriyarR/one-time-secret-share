from flask import Flask
import unittest
from werkzeug.test import Client
from flask_testing import TestCase as FlaskTestCase
from onetime.entrypoints.web_flask.blueprints.views import blueprint
from onetime.configurator.containers import Container
from unittest.mock import patch
import tempfile
import random
import string
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class SecretTestCase(FlaskTestCase):

    def create_app(self):
        app = Flask(__name__)
        container = Container()
        app.container = container
        app.config['TESTING'] = True
        app.config['SECURE_SSL_REDIRECT'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = config.get('web_flask', 'SECRET_KEY')
        app.config['MAX_CONTENT_LENGTH'] = 100 * 1024
        app.config['MAX_CONTENT_LENGTH_FILE_UPLOAD'] = 0
        app.config['DATA_UPLOAD_MAX_NUMBER_FIELDS'] = 0
        app.register_blueprint(blueprint)
        return app

    def setUp(self):
        self.client = Client(self.app)

    def get_url(self, response):
        html_content = response.get_data(as_text=True)
        start_index = html_content.find('http://localhost/secret/')
        end_index = html_content.find('"', start_index)
        if html_content[start_index:end_index]:
            return html_content[start_index:end_index]
        return None

    def test_if_create_secret_index_page_is_shown(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add your secret and click", response.data)

    def test_if_secret_url_can_be_created(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = self.get_url(response=response)
        self.assertTrue(url)
        self.assertIn("/secret", url)

    def test_if_secret_url_can_be_created_with_empty_secret(self):
        response = self.client.post("/", data={"secret": ""})
        url = self.get_url(response=response)
        self.assertIs(url, None)

    def test_if_secret_url_can_be_opened(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = self.get_url(response=response)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Click below to retrieve secret value", resp.data)

    def test_if_can_get_secret_using_secret_url(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = self.get_url(response=response)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"awesome-secret", resp.data)

    def test_if_can_get_secret_using_wrong_uuid(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = self.get_url(response=response)
        # Bad request if the url uuid was tempered
        resp = self.client.post(f"{url}xxx")
        self.assertEqual(resp.status_code, 400)
        # But you can still open the tempered url
        resp = self.client.get(f"{url}xxx")
        self.assertEqual(resp.status_code, 200)

    def test_if_can_get_secret_twice(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = self.get_url(response=response)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"awesome-secret", resp.data)

        # Impossible to get secret twice; it is read once.
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"Secret can not be retrieved twice, it was already consumed", resp.data)

    def test_if_can_create_and_get_same_secret_multiple_times(self):
        response1 = self.client.post("/", data={"secret": "awesome-secret"})
        response2 = self.client.post("/", data={"secret": "awesome-secret"})
        response3 = self.client.post("/", data={"secret": "awesome-secret"})
        url1 = self.get_url(response=response1)
        url2 = self.get_url(response=response2)
        url3 = self.get_url(response=response3)

        resp1 = self.client.post(url1)
        resp2 = self.client.post(url2)
        resp3 = self.client.post(url3)

        self.assertEqual(resp1.status_code, 200)
        self.assertIn(b"awesome-secret", resp1.data)

        self.assertEqual(resp2.status_code, 200)
        self.assertIn(b"awesome-secret", resp2.data)

        self.assertEqual(resp3.status_code, 200)
        self.assertIn(b"awesome-secret", resp3.data)

    def test_if_can_get_secret_from_expired_url(self):
        with patch("onetime.use_cases.manager.is_expired", return_value=True):
            response = self.client.post("/", data={"secret": "awesome-secret"})
            url = self.get_url(response=response)
            resp = self.client.post(url)
            self.assertEqual(resp.status_code, 400)
            self.assertIn(b"URL with given UUID is expired", resp.data)

            resp = self.client.post(url)
            self.assertEqual(resp.status_code, 400)
            # Now the error message has been changed
            self.assertIn(b"Could not find the secret with provided UUID", resp.data)

    def test_if_can_send_put_request(self):
        response = self.client.put("/", data={"secret": "awesome-secret"})
        # HttpResponseNotAllowed
        self.assertEqual(response.status_code, 405)

    def test_if_can_send_put_request_for_getting_secret(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = self.get_url(response=response)
        resp = self.client.put(url)
        self.assertEqual(resp.status_code, 405)

    def test_if_can_send_file_object_as_secret(self):
        with tempfile.TemporaryFile() as file_:
            response = self.client.post("/", data={"secret": (file_, 'filename.txt')})
            self.assertEqual(response.status_code, 200)

    def test_if_large_string_is_allowed(self):
        file_size = 1 * 1024 * 1024

        # Generate random string data
        data = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(file_size)
        )
        response = self.client.post("/", data={"secret": data})
        self.assertEqual(response.status_code, 413)

    def test_form_max_length_string(self):
        file_size = 201

        # Generate random string data
        data = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(file_size)
        )
        response = self.client.post("/", data={"secret": data})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
