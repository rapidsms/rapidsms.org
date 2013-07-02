

class MockPyPIRequest(object):

    def __init__(self, *args, **kwargs):
        self.status_code = kwargs.pop('status_code', None) or 200
        super(MockPyPIRequest, self).__init__(*args, **kwargs)

    def json(self):
        return {
            'info': {
                'maintainer': '',
                'maintainer_email': '',
                'author': '',
                'author_email': '',
                'version': '',
                'summary': '',
                'docs_url': '',
                'home_page': '',
                'license': '',
                'description': '',
            },
            'urls': [{
                'upload_time': '',
            }],
        }
