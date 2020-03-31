"""
Utility classes to test Github Login functionality.
"""


class ProviderMockResponse(object):

    def __init__(self, response, status):
        self.response = response
        self.status_code = status

    def json(self):
        return self.response


class MockClient(object):

    def __init__(self, name, email="info@example.com", response=None,
                 response_status=200):
        self.name = name
        self.email = email
        self.url = self.get_redirect_url()
        self.response = response
        self.response_status = response_status

    def get_redirect_url(self, *args, **kwargs):
        return '/login/oauth/authorize'.format(name=self.name)

    def get_access_token(self, request, callback=None, return_value='token'):
        return return_value

    def get_profile_info(self, token, return_value=None):
        info = return_value or {
            'id': 1,
            'name': 'github user',
            'location': 'Chapel Hill', 'website_url': 'http://www.example.com',
            'github_url': 'http://www.github.com/rapidsms'
        }
        return info

    def request(self, method, email_url, headers=None):
        return ProviderMockResponse(response=self.response,
                                    status=self.response_status)
