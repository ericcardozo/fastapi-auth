from tests.unit.mock.context import FakeContext
from tests.unit.mock.repository import FakeAccounts

import pytest

def test_create():
    context = FakeContext()
    with context:
        account = context.accounts.create("test", "test")
        assert account.id == 3
        assert account.username == "test"
        assert context.commited == False
        context.commit()

    assert context.commited == True

def test_read():
    context = FakeContext()
    with context:
        account = context.accounts.read(username="admin")
        assert account.id == 1
        assert account.username == "admin"

def test_update():
    context = FakeContext()
    with context:
        account = context.accounts.update(1, username="test")
        assert account.id == 1
        assert account.username == "test"
        assert context.commited == False
        context.commit()

    assert context.commited == True

def test_delete():
    context = FakeContext()
    with context:
        context.accounts.delete(username="admin")
        assert context.accounts.read(username="admin") == None
        assert context.commited == False
        context.commit()

    assert context.commited == True