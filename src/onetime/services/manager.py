from onetime.domain.model import Secret


class SecretManager:
    def __init__(self):
        self.secret = None

    def generate_secret(self, secret: str) -> None:
        self.secret = Secret(secret)

    def get_secret(self) -> str:
        return self.secret.get_secret()
