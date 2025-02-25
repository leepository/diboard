from app.tests.base import TestBase


class TestBoard(TestBase):

    def get_article_list(self, client):
        url = "/board/articles"
        result = self.run_request(
            test_client=client,
            method="GET",
            url=url
        )
        assert result['status_code'] == 200
        assert result['data'] is not None

        return result['data']

    def delete_article(self, client, article_id):
        url = '/board/article/{article_id}'
        result = self.run_request(
            test_client=client,
            method='DELETE',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True

    ####################################################################################################################
    # Testcase
    ####################################################################################################################
    def test000_signin(self, client):
        self.signin(client=client)

    def test100_get_board_list(self, client):
        self.get_article_list(client=client)

    def test110_create_article(self, client):
        article_data = {
            'title': 'Test article title',
            'content': 'Test article contents',
            'tags': ['tag1', 'tag2']
        }
        url = "/board/articles"
        result = self.run_request(
            test_client=client,
            method="POST",
            url=url,
            data=article_data,
            formdata=True
        )
        assert result['status_code'] == 200

        # Check inputed data
        articles = self.get_article_list(client=client)
        inputed_data = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        assert len(inputed_data) > 0

    def test111_create_article_without_tags(self, client):
        article_data = {
            'title': 'Test article title without tags',
            'content': 'Test article content without tags',
            'tags': None
        }
        url = '/board/articles'
        result = self.run_request(
            test_client=client,
            method='POST',
            url=url,
            data=article_data,
            formdata=True
        )
        assert result['status_code'] == 200

        # check input data
        articles = self.get_article_list(client=client)
        inpurted_data = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        assert len(articles) > 0

    def test500_delete_article(self, client):
        articles = self.get_article_list(client=client)
        article_id = articles[0]['id']

        # Delete article
        url = f'/board/article/{article_id}'
        result = self.run_request(
            test_client=client,
            method='DELETE',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True
