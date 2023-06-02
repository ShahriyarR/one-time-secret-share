from readonce import ReadOnce


class Secret(ReadOnce):
    def __init__(self, secret: str) -> None:
        super().__init__()
        self.add_secret(secret)
