from tests.unit.mock.context import Users

def test_cryptography():
    context = Users()

    with context:
        hash = context.cryptography.hash("password")

    other_context = Users()
    with other_context:
        assert other_context.cryptography.verify("password", hash)

def test_tokenization():
    context = Users()
    with context:
        token = context.tokenization.encode('4')

    other_context = Users()
    with other_context:
        assert other_context.tokenization.decode(token)["subject"] == '4'


