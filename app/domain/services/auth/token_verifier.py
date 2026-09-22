from abc import ABC, abstractmethod
from passlib.hash import pbkdf2_sha256


class TokenVerifier(ABC):
    @abstractmethod
    def verify_admin_token(self, token: str) -> bool:
        ...


class Pbkdf2TokenVerifier(TokenVerifier):
    _ADMIN_TOKEN_HASH = "$pbkdf2-sha256$29000$K4WwNiakVGrN.d97j9G6Nw$IGLabM9cHS.Be3DHAL3LdAKZVZvSvwoTeV1kbMmczxU"

    def verify_admin_token(self, token: str) -> bool:
        return pbkdf2_sha256.verify(token, self._ADMIN_TOKEN_HASH)