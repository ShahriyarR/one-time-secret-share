from django.test import Client, TestCase


class SecretTestCase(TestCase):
    def setUp(self) -> None:
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

    def test_if_secret_url_can_be_opened(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        resp = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(resp, "Click below to retrieve secret value")

    def test_if_can_get_secret_using_secret_url(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        resp = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp.context["secret_data"], "awesome-secret")

    def test_if_can_get_secret_using_wrong_uuid(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        # Bad request if the url uuid was tempered
        resp = self.client.post(url + "xxx")
        self.assertEquals(resp.status_code, 400)

        # But you can still open the tempered url
        resp = self.client.get(url + "xxx")
        self.assertEquals(resp.status_code, 200)

    def test_if_can_get_secret_twice(self):
        response = self.client.post("/", data={"secret": "awesome-secret"})
        url = response.context["secret_url"]
        resp = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp.context["secret_data"], "awesome-secret")
        # Impossible to get secret twice; it is read once.
        resp = self.client.post(url)
        self.assertEquals(resp.status_code, 400)
        self.assertIn(
            "Secret can not be retrieved twice, it was already consumed",
            str(resp.content),
        )
