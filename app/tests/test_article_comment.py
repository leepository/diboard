import pytest

from app.tests.base import TestBase

class TestArticleComment(TestBase):

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

    def get_article_comment_list(self, client, article_id):
        url = f'/board/article/{article_id}/comments'
        result = self.run_request(
            test_client=client,
            method='GET',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data'] is not None

        return result['data']

    def get_article_comment_detail(self, client, article_id, comment_id):
        url = f'/board/article/{article_id}/comment/{comment_id}'
        result = self.run_request(
            test_client=client,
            method='GET',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data'] is not None

        return result['data']

    def delete_article_comment_all(self, client, article_id):
        url = f'/board/article/{article_id}/comment'
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

    def test100_create_article_comment(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')

        article_id = articles[0]['id']

        # Delete old test data
        self.delete_article_comment_all(client=client, article_id=article_id)

        # Insert comment
        insert_data = {
            'article_id': article_id,
            'content': 'Test article comment'
        }
        url = f'/board/article/{article_id}/comment'
        result = self.run_request(
            test_client=client,
            method='POST',
            url=url,
            data=insert_data
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True

        # Check inserted
        comments = self.get_article_comment_list(client=client, article_id=article_id)
        inserted_comments = list(filter(
            lambda x: x['content'] == insert_data['content'] and x['article_id'] == insert_data['article_id'],
            comments
        ))
        assert len(inserted_comments) > 0

    def test110_create_article_subcomment(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')
        article_id = articles[0]['id']

        comments = self.get_article_comment_list(client=client, article_id=article_id)
        if len(comments) < 1:
            pytest.skip('Not exist article comment test data')
        comment_id = comments[0]['id']

        # Insert comment
        insert_data = {
            'article_id': article_id,
            'comment_id': comment_id,
            'content': 'Test sub comment'
        }
        url = f'/board/article/{article_id}/comment'
        result = self.run_request(
            test_client=client,
            method='POST',
            url=url,
            data=insert_data
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True

        # Check inserted
        comments = self.get_article_comment_list(client=client, article_id=article_id)
        inserted_comments = list(filter(
            lambda x: x['content'] == insert_data['content'] and x['article_id'] == insert_data['article_id'] and x['comment_id'] == insert_data['comment_id'],
            comments
        ))
        assert len(inserted_comments) > 0

    def test200_update_article_comment(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')
        article_id = articles[0]['id']

        comments = self.get_article_comment_list(client=client, article_id=article_id)
        if len(comments) < 1:
            pytest.skip('Not exist article comment test data')
        comment_id = comments[0]['id']

        # Update comment
        update_data = {
            'article_id': article_id,
            'content': 'Update article comment test'
        }
        url = f'/board/article/{article_id}/comment/{comment_id}'
        result = self.run_request(
            test_client=client,
            method='PATCH',
            url=url,
            data=update_data
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True

        # Check update result
        comment = self.get_article_comment_detail(client=client, article_id=article_id, comment_id=comment_id)
        assert comment['content'] == update_data['content']

    def test300_get_article_comment_list(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')
        article_id = articles[0]['id']

        url = f'/board/article/{article_id}/comments'
        result = self.run_request(
            test_client=client,
            method='GET',
            url=url
        )
        assert result['status_code'] == 200
        assert len(result['data']) > 0

    def test400_get_article_comment_detail(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')
        article_id = articles[0]['id']

        comments = self.get_article_comment_list(client=client, article_id=article_id)
        if len(comments) < 1:
            pytest.skip('Not exist article comment test data')
        comment_id = comments[0]['id']

        # Get article comment detail
        self.get_article_comment_detail(client=client, article_id=article_id, comment_id=comment_id)


    def test500_delete_article_comment(self, client):
        articles = self.get_article_list(client=client)
        if len(articles) < 1:
            pytest.skip('Not exist article test data')
        article_id = articles[0]['id']

        comments = self.get_article_comment_list(client=client, article_id=article_id)
        if len(comments) < 1:
            pytest.skip('Not exist article comment test data')
        comment_id = comments[0]['id']

        # Delete comment
        url = f'/board/article/{article_id}/comment/{comment_id}'
        result = self.run_request(
            test_client=client,
            method='DELETE',
            url=url
        )
        assert result['status_code'] == 200
        assert result['data']['result'] is True
