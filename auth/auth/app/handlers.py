from auth.domain.models import Credentials, Token
from auth.domain.context import Users

def handle_login(credentials : Credentials, context : Users) -> Token:
    with context:
        account = context.accounts.read(username = credentials.username)
        assert account, "Account not found"
        assert context.accounts.verify(credentials), "Invalid password"
        return context.tokenization.encode(account.id)