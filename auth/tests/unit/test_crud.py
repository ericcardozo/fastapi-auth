import pytest

from auth.domain.models import Credentials
from tests.unit.mock.context import Users

def test_create():
    users = Users()
    with users:
        credentials = Credentials(username="test", password="test")
        account = users.accounts.create(credentials)
        assert account.id == 3
        assert account.username == "test"
        assert users.commited == False
        users.commit()

    assert users.commited == True

def test_read():
    users = Users()
    with users:
        account = users.accounts.read(id=1)
        assert account.id == 1
        assert account.username == "admin"
        assert users.commited == False
        users.commit()

    assert users.commited == True

def test_update():
    users = Users()
    with users:
        account = users.accounts.update(id=1, username="test")
        assert account.id == 1
        assert account.username == "test"
        assert users.commited == False
        users.commit()

    assert users.commited == True

def test_delete():
    users = Users()
    with users:
        users.accounts.delete(id=1)
        assert users.accounts.read(id=1) == None
        assert users.commited == False
        users.commit()

    assert users.commited == True


def test_verify():
    users = Users()
    with users:
        credentials = Credentials(username="admin", password="admin")
        assert users.accounts.verify(credentials) == True
        credentials = Credentials(username="admin", password="test")
        assert users.accounts.verify(credentials) == False
        assert users.commited == False
        users.commit()

    assert users.commited == True
    