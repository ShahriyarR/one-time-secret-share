from onetime.services.manager import generate_and_encrypt_uuid


def test_if_uuid_is_generated():
    assert len(generate_and_encrypt_uuid()) == 143
    assert generate_and_encrypt_uuid()


def test_if_randomized():
    first = generate_and_encrypt_uuid()
    second = generate_and_encrypt_uuid()
    assert first is not second
    assert first != second
