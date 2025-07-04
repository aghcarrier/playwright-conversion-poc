class TokenStorage:
    def __init__(self):
        self.tokens = {}

    def set_token(self, token):
        self.tokens = token

    def get_token(self):
        return self.tokens

token = TokenStorage()

class BaseURLStorage:
    def __init__(self):
        self.base_url = {}

    def set_base_url(self, baseurl):
        self.base_url = baseurl

    def get_base_url(self):
        return self.base_url

base_url = BaseURLStorage()