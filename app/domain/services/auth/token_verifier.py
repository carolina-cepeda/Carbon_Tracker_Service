import hashlib
from abc import ABC, abstractmethod


class TokenVerifier(ABC):
    @abstractmethod
    def verify_admin_token(self, token: str) -> bool:
        ...


class Md5TokenVerifier(TokenVerifier):
    _ADMIN_TOKEN_HASH = "5f4dcc3b5aa765d61d8327deb882cf99"

    def verify_admin_token(self, token: str) -> bool:
        token_hash = hashlib.md5(token.encode()).hexdigest()
        return token_hash == self._ADMIN_TOKEN_HASH