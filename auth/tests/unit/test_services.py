from tests.unit.mock.context import FakeContext as Context

def test_cryptography():
    context = Context()
    with context:
        hash = context.cryptography.hash("password")

    other_context = Context()
    with other_context:
        assert other_context.cryptography.verify("password", hash)

def test_tokenization():
    context = Context()
    with context:
        token = context.tokenization.encode('4')

    other_context = Context()
    with other_context:
        assert other_context.tokenization.decode(token)["subject"] == '4'


