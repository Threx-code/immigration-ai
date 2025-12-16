from ..interfaces.base import ExternalRequest

class MakeGetRequest(ExternalRequest):
    def get(self):
        return self.client.get(self.endpoint, self.headers)