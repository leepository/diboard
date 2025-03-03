import io
import pytest

from app.tests.base import TestBase

class TestAttachedFile(TestBase):

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

    def test100_delete_attached_file(self, client):
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

        # create article
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

        # Get article detail
        result_detail = self.get_article_detail(client=client, article_id=created_articles[0]['id'])
        assert result_detail['status_code'] == 200
        assert result_detail['data'] is not None
        created_article = result_detail['data']

        assert created_article['title'] == article_data['title']
        assert created_article['content'] == article_data['content']
        created_tags = [d['tagging'] for d in created_article['tags']].sort()
        assert created_tags == article_data['tags'].sort()
        assert len(created_article['attached_files']) > 0

        attached_file_id = created_article['attached_files'][0]['id']

        # Delete attached_file
        url = f"/board/article/{created_article['id']}/attached-file/{attached_file_id}"
        result = self.run_request(
            test_client=client,
            method='DELETE',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True
