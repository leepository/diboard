from app.tests.base import TestBase

class TestUser(TestBase):

    def get_user_list(self, client):
        """
        User 목록 조회
        """
        url = "/membership/users"
        result = self.run_request(
            test_client=client,
            method="GET",
            url=url
        )
        assert result['status_code'] == 200
        assert len(result['data']) > 0

        return result['data']


    ####################################################################################################################
    # Testcase
    ####################################################################################################################
    def test000_signin(self, client):
        self.signin(client=client)

    def test100_get_user_list(self, client):
        """
        User 목록 조회 테스트
        """
        self.get_user_list(client=client)

    def test110_get_user_detail(self, client):
        """
        User 상세 조회 테스트
        """
        users = self.get_user_list(client=client)
        user_id = users[0]['id']


        url = f"/membership/user/{user_id}"
        result = self.run_request(
            test_client=client,
            method="GET",
            url=url
        )
        assert result['status_code'] == 200
        assert result['data']['id'] == user_id


