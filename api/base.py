import requests

class BaseAPI(object):
    def _request(self, method, endpoint, **kwargs):
        kwargs['method'] = method
        kwargs['url'] = self.get_base_url() + endpoint

        self.before_request(kwargs)

        return requests.request(**kwargs)

    def get_base_url(self):
        raise NotImplementedError

    def before_request(self, kwargs):
        pass

    def get(self, endpoint, params=None, **kwargs):
        return self._request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return self._request('POST', endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, **kwargs):
        return self._request('PUT', endpoint, data=data, **kwargs)

    def options(self, endpoint, **kwargs):
        return self._request('OPTIONS', endpoint, **kwargs)

    def head(self, endpoint, **kwargs):
        return self._request('HEAD', endpoint, **kwargs)

    def patch(self, endpoint, data=None, **kwargs):
        return self._request('PATCH', endpoint, data=data, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)

class BaseServiceAPI(BaseAPI):
    def __init__(self):
        super().__init__()

    def get_base_url(self):
        raise NotImplementedError

    def default_token(self):
        raise NotImplementedError
