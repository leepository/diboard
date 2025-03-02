import io
import pytest

from datetime import datetime

from app.tests.base import TestBase
from app.utils.datetime_utils import dt2ts

class TestArticle(TestBase):

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

    def get_article_detail(self, client, article_id: int):
        url = f'/board/article/{article_id}'
        result = self.run_request(
            test_client=client,
            method='GET',
            url=url
        )
        return result

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

    def test110_create_article_with_tags(self, client):
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

        result_detail = self.get_article_detail(client=client, article_id=created_data[0]['id'])
        assert result_detail['status_code'] == 200
        assert result_detail['data'] is not None
        created_article = result_detail['data']

        assert created_article['title'] == article_data['title']
        assert created_article['content'] == article_data['content']
        created_tags = [d['tagging'] for d in created_article['tags']].sort()
        assert created_tags == article_data['tags'].sort()

    def test111_create_article_without_tags(self, client):
        article_data = {
            'title': f'Test article title without tags',
            'content': 'Test article content without tags',
            'tags': None
        }

        # Delete test articles existed
        articles = self.get_article_list(client=client)
        existed_articles = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        if len(existed_articles) > 0:
            for existed_article in existed_articles:
                self.delete_article(client=client, article_id=existed_article['id'])

        # Test create article
        url = '/board/articles'
        result = self.run_request(
            test_client=client,
            method='POST',
            url=url,
            data=article_data,
            formdata=True
        )
        assert result['status_code'] == 200

        # check created data
        articles = self.get_article_list(client=client)
        created_data = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        assert len(created_data) > 0

        result_detail = self.get_article_detail(client=client, article_id=created_data[0]['id'])
        assert result_detail['status_code'] == 200
        assert result_detail['data'] is not None
        created_article = result_detail['data']

        assert created_article['title'] == article_data['title']
        assert created_article['content'] == article_data['content']
        assert len(created_article['tags']) < 1

    def test112_create_article_with_file(self, client):
        article_data = {
            'title': f'Test article title with file',
            'content': 'Test article content',
            'tags': ['TestTag1', 'TestTag2']
        }

        # Delete article
        articles = self.get_article_list(client=client)
        existed_articles = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        if len(existed_articles) > 0:
            for existed_article in existed_articles:
                self.delete_article(client=client, article_id=existed_article['id'])

        # Test create article
        url = '/board/articles'
        file1 = io.BytesIO(b"This is file 1 content")
        file2 = io.BytesIO(b"This is file 2 content")
        file3 = io.BytesIO(b"File 3 binary data example: \x00\x01\x02\x03")
        files = [
            ("files", ("file1.txt", file1, "text/plain")),
            ("files", ("file2.txt", file2, "text/plain")),
            ("files", ("file3.bin", file3, "application/octet-stream"))
        ]

        result = self.run_request(
            test_client=client,
            method='POST',
            url=url,
            data=article_data,
            files=files,
            formdata=True
        )
        assert result['status_code'] == 200

        # Check created article
        articles = self.get_article_list(client=client)
        created_articles = list(filter(
            lambda x: x['title'] == article_data['title'],
            articles
        ))
        assert len(created_articles) > 0

        result_detail = self.get_article_detail(client=client, article_id=created_articles[0]['id'])
        assert result_detail['status_code'] == 200
        assert result_detail['data'] is not None
        created_article = result_detail['data']

        assert created_article['title'] == article_data['title']
        assert created_article['content'] == article_data['content']
        created_tags = [d['tagging'] for d in created_article['tags']].sort()
        assert created_tags == article_data['tags'].sort()

    def test200_get_article_list(self, client):
        articles = self.get_article_list(client=client)
        assert len(articles) > 0

    def test300_get_article_detail(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip("No created article test data ")
        article_id = articles[0]['id']

        result_detail = self.get_article_detail(client=client, article_id=article_id)
        assert result_detail['status_code'] == 200
        assert result_detail['data'] is not None

    def test310_get_article_detail_error_with_wrong_article_id(self, client):
        article_id = 1000000
        result_detail = self.get_article_detail(client=client, article_id=article_id)
        assert result_detail['status_code'] == 400
        assert result_detail['detail'] == 'Not exist article'

    def test400_update_article(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip("No created article test data")
        article_id = articles[0]['id']

        # Update article
        url = f'/board/article/{article_id}'
        update_data = {
            'title': 'Update article title',
            'content': 'Update article content',
            'tags': ['UpdatedTag1', 'UpdatedTag2', 'UpdatedTag3']
        }
        result = self.run_request(
            test_client=client,
            method='PATCH',
            url=url,
            data=update_data,
            formdata=True
        )
        assert result['status_code'] == 200

        # Check updated data
        result_detail = self.get_article_detail(client=client, article_id=article_id)
        assert result_detail['status_code'] == 200
        assert result_detail['data'] is not None
        article_detail = result_detail['data']

        assert article_detail['title'] == update_data['title']
        assert article_detail['content'] == update_data['content']
        assert [d['tagging'] for d in article_detail['tags']].sort() == update_data['tags'].sort()

    def test410_update_article_partially(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip("No created article test data")
        article_id = articles[0]['id']

        # Update article
        url = f'/board/article/{article_id}'
        update_data = {
            'title': 'Update twice article title'
        }
        result = self.run_request(
            test_client=client,
            method='PATCH',
            url=url,
            data=update_data,
            formdata=True
        )
        assert result['status_code'] == 200

        # Check updated data
        result_detail = self.get_article_detail(client=client, article_id=article_id)
        assert result_detail['status_code'] == 200
        assert result_detail['data'] is not None
        article_detail = result_detail['data']

        assert article_detail['title'] == update_data['title']

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
