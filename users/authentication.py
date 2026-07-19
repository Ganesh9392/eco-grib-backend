from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    The frontend (src/lib/api/client.ts) sends:
        Authorization: Bearer <token>

    DRF's default TokenAuthentication expects "Token <token>" instead,
    so this tiny subclass just changes the expected keyword to "Bearer".
    """

    keyword = "Bearer"
