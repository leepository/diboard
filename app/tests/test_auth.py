from app.tests.base import TestBase

class TestAuth(TestBase):

    def test100_signin(self, client):
      self.signin(client=client)