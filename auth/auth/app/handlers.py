from auth.domain.models import Credentials, Token
from auth.domain.context import Users

def handle_login(credentials : Credentials, users : Users) -> Token:
    with users:
        account = users.accounts.read(username = credentials.username)
        assert account, "Account not found"
        assert users.accounts.verify(credentials), "Invalid password"
        return users.tokenization.encode(account.id)

def handle_register(credentials : Credentials, users : Users) -> Token:
    with users:
        account = users.accounts.read(username = credentials.username)
        assert account == None, "Account already exists"
        account = users.accounts.create(credentials)
        return users.tokenization.encode(account.id)