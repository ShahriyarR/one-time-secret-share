import random
import string
import tempfile
from unittest.mock import patch

import pytest
from django.test import Client, TestCase, override_settings


class SecretTestCase(TestCase):
    def setUp(self) -> None:
        settings_manager = override_settings(SECURE_SSL_REDIRECT=False)
        settings_manager.enable()
        self.addCleanup(settings_manager.disable)
        self.client = Client()

    def test_if_create_secret_index_page_is_shown(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Add your secret and click")

    def test_if_secret_url_can_be_created(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        self.assertTrue(url)
        self.assertIn("/secret", url)

    def test_if_secret_url_can_be_created_with_empty_secret(self):
        response = self.client.post("/", data={"secret": ""})
        url = response.context.get("secret_url")
        self.assertIs(url, None)

    def test_if_secret_url_can_be_opened(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, "Click below to retrieve secret value")

    def test_if_can_get_secret_using_secret_url(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        resp = self.client.post(url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.context["secret_data"], "awesome-secret")

    def test_if_can_get_secret_using_wrong_uuid(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        # Bad request if the url uuid was tempered
        resp = self.client.post(f"{url}xxx")
        self.assertEquals(resp.status_code, 400)

        # But you can still open the tempered url
        resp = self.client.get(f"{url}xxx")
        self.assertEquals(resp.status_code, 200)

    def test_if_can_get_secret_twice(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        resp = self.client.post(url)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.context["secret_data"], "awesome-secret")
        # Impossible to get secret twice; it is read once.
        resp = self.client.post(url)
        self.assertEquals(resp.status_code, 400)
        self.assertIn(
            "Secret can not be retrieved twice, it was already consumed",
            str(resp.content),
        )

    def test_if_can_get_secret_from_expired_url(self):
        with patch("onetime.use_cases.manager.is_expired", return_value=True):
            response = self.client.post("/", data={"secret": "awesome-secret"})
            url = response.context["secret_url"]
            resp = self.client.post(url)
            self.assertEquals(resp.status_code, 400)
            self.assertIn("URL with given UUID is expired", str(resp.content))

            resp = self.client.post(url)
            self.assertEquals(resp.status_code, 400)
            # Now the error message has been changed
            self.assertIn(
                "Could not find the secret with provided UUID", str(resp.content)
            )


class GenericTestCases(TestCase):
    def setUp(self) -> None:
        settings_manager = override_settings(SECURE_SSL_REDIRECT=False)
        settings_manager.enable()
        self.addCleanup(settings_manager.disable)
        self.client = Client()

    def test_if_can_send_put_request(self):
        response = self.client.put("/", data={"secret": "awesome-secret"})
        # HttpResponseNotAllowed
        self.assertEquals(response.status_code, 405)

    def test_if_can_send_put_request_for_getting_secret(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        resp = self.client.put(url)
        self.assertEquals(resp.status_code, 405)

    def test_if_can_send_file_object_as_secret(self):
        with tempfile.TemporaryFile() as file_:
            response = self.client.post("/", data={"secret": file_})
            self.assertEquals(response.status_code, 200)
            with pytest.raises(KeyError):
                _ = response.context["secret_url"]

    def test_if_large_string_is_allowed(self):
        file_size = 1 * 1024 * 1024

        # Generate random string data
        data = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(file_size)
        )
        response = self.client.post("/", data={"secret": data})
        self.assertEquals(response.status_code, 400)

    def test_form_max_length_string(self):
        file_size = 201

        # Generate random string data
        data = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(file_size)
        )
        response = self.client.post("/", data={"secret": data})
        self.assertEquals(response.status_code, 200)
        # but the secret url was not generated
        with pytest.raises(KeyError):
            _ = response.context["secret_url"]
