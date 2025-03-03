import pytest

from app.tests.base import TestBase

class TestArticleTag(TestBase):

    def get_article_list(self, client):
        url = '/board/articles'
        result = self.run_request(
            test_client=client,
            method='GET',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data'] is not None

        return result['data']

    def get_article_detail(self, client, article_id):
        url = f'/board/article/{article_id}'
        result = self.run_request(
            test_client=client,
            method='GET',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data'] is not None

        return result['data']

    def delete_article(self, client, article_id):
        url = f'/board/article/{article_id}'
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

    def test100_create_article_with_tag(self, client):
        article_data = {
            'title': f'Test article title',
            'content': 'Test article contents',
            'tags': ['tag1', 'tag2']
        }

        # Clear test data existed
        articles = self.get_article_list(client=client)
        existed_articles = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        if len(existed_articles) > 0:
            for existed_article in existed_articles:
                self.delete_article(client=client, article_id=existed_article['id'])

        # Test create article
        url = "/board/articles"
        result = self.run_request(
            test_client=client,
            method="POST",
            url=url,
            data=article_data,
            formdata=True
        )
        assert result['status_code'] == 200

        # Check created data
        articles = self.get_article_list(client=client)
        created_data = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        assert len(created_data) > 0

        created_article = self.get_article_detail(client=client, article_id=created_data[0]['id'])

        assert created_article['title'] == article_data['title']
        assert created_article['content'] == article_data['content']
        created_tags = [d['tagging'] for d in created_article['tags']].sort()
        assert created_tags == article_data['tags'].sort()

    def test200_delete_tag(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')
        article_id = articles[0]['id']

        article = self.get_article_detail(client=client, article_id=article_id)
        tag_id = article['tags'][0]['id']

        # Delete tag
        url = f'/board/article/{article_id}/tag/{tag_id}'
        result = self.run_request(
            test_client=client,
            method='DELETE',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True

    def test300_delete_tag_all(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')
        article_id = articles[0]['id']

        url = f'/board/article/{article_id}/tags'
        result = self.run_request(
            test_client=client,
            method='DELETE',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True
