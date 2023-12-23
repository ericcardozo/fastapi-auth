import pytest
import time
from datetime import timedelta
from src.auth.services.criptography import Cryptography
from src.auth.services.tokenization import Tokenization

@pytest.fixture
def cryptography_fixture():
    return Cryptography()

@pytest.fixture
def tokenization_fixture():
    return Tokenization()

def test_cryptography(cryptography_fixture : Cryptography):
    password = "1234"
    hashed_password = cryptography_fixture.hash(password)
    assert hashed_password != password

    assert cryptography_fixture.verify(password, hashed_password) == True
    assert cryptography_fixture.verify("12345", hashed_password) == False

def test_tokenizer_encode_decode(tokenization_fixture : Tokenization):
    tokenizer = tokenization_fixture
    subject = "user_id_123"
    token = tokenizer.encode(subject)
    assert isinstance(token, str)
    
    decoded_token = tokenizer.decode(token)
    assert isinstance(decoded_token, dict)
    
    assert decoded_token["subject"] == subject


def test_tokenizer_expired_token(tokenization_fixture : Tokenization):
    tokenizer = tokenization_fixture
    expires_delta = timedelta(seconds=1)
    token = tokenizer.encode("user_id_456", expires_delta=expires_delta)
    try:
        time.sleep(2)
        tokenizer.decode(token)
    except ValueError as error:
        assert str(error) == "Token has expired"
    else:
        raise AssertionError("Expected ValueError for expired token not raised")

def test_tokenizer_invalid_token(tokenization_fixture : Tokenization):
    tokenizer = tokenization_fixture
    invalid_token = tokenizer.encode("user_id_789")
    invalid_token = invalid_token[:-5] 
    
    try:
        tokenizer.decode(invalid_token)
    except ValueError as error:
        assert str(error) == "Invalid token"
    else:
        raise AssertionError("Expected ValueError for invalid token not raised")