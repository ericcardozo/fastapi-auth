from auth.domain.context import Context
from auth.app.models import Token

def handle_login(username : str, password : str, context : Context)->Token:
    with context:
        account = context.accounts.read(username=username)
        assert account, "Account not found"
        assert context.accounts.verify(account.id, password), "Invalid password"
        return context.tokenization.encode(account.id)