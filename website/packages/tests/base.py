

class MockPyPIRequest(object):
    """
    Used to mock the data sent by PyPI, returned by Package.get_pypi_request.
    """

    def __init__(self, status_code=None, **json_data):
        self.status_code = status_code or 200
        self.json_data = json_data

    def json(self):
        if self.status_code != 200:
            raise Exception("Can't get JSON data from a non-200 response.")
        return {
            'info': {
                'maintainer': self.json_data.get('maintainer', ''),
                'maintainer_email': self.json_data.get('maintainer_email', ''),
                'author': self.json_data.get('author', ''),
                'author_email': self.json_data.get('author_email', ''),
                'version': self.json_data.get('version', ''),
                'summary': self.json_data.get('summary', ''),
                'docs_url': self.json_data.get('docs_url', ''),
                'home_page': self.json_data.get('home_page', ''),
                'license': self.json_data.get('license', ''),
                'description': self.json_data.get('description', ''),
            },
            'urls': [{
                'upload_time': self.json_data.get('upload_time', ''),
            }],
        }
