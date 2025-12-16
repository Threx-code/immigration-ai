from ..interfaces.base import ExternalRequest

class MakePostRequest(ExternalRequest):

    def post(self):
        data = {}
        return self.client.post(self.endpoint, data, self.headers)