from app.tests.base import TestBase

class TestApp(TestBase):

    def test100_health(self, client):
        url = "/health"
        result = self.run_request(
            test_client=client,
            method='GET',
            url=url
        )
        assert result['status_code'] == 200
