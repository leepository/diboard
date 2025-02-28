from app.utils.aws_utils import get_aws_secret_value


class TestBase:

    ACCESS_TOKEN = None

    def signin(self, client):
        test_user = get_aws_secret_value(secret_name="diboard/test-user")

        url = '/auth/signin'
        request_params = {
            'signin_id': test_user['signin_id'],
            'signin_pass': test_user['signin_password']
        }
        resp = client.post(
            url=url,
            json=request_params
        )
        result = resp.json()
        if resp.status_code not in [200, 201]:
            print("result : ", result)
        assert resp.status_code == 200
        assert result['access_token'] is not None
        assert result['refresh_token'] is not None

        TestBase.ACCESS_TOKEN = result['access_token']

    def run_request(self, test_client, method, url, headers=None, params=None, data=None, files=None, formdata=False):
        access_token = self.ACCESS_TOKEN

        # Headers
        if headers is None:
            headers = {}
        headers.update({'authorization': f'Bearer {access_token}'})

        test_client_method = {
            "GET": test_client.get,
            "POST": test_client.post,
            "PUT": test_client.put,
            "PATCH": test_client.patch,
            "DELETE": test_client.delete
        }
        if method.upper() in ["GET", "DELETE"]:
            resp = test_client_method[method.upper()](
                url=url,
                headers=headers,
                params=params
            )
        else:
            resp = test_client_method[method.upper()](
                url=url,
                headers=headers,
                params=params,
                json=data if formdata is False else None,
                data=data if formdata is True else None,
                files=files
            )

        result_dict = {}
        if resp.status_code not in [200, 201]:
            try:
                result_dict.update({
                    'status_code': resp.status_code,
                    'detail': resp.json()
                })
            except:
                result_dict.update({
                    'status_code': resp.status_code,
                    'resp_text': resp.text
                })

            print("result : ", result_dict)
        else:
            try:
                result_dict.update({
                    'status_code': resp.status_code,
                    'data': resp.json()
                })
            except:
                result_dict.update({
                    'status_code': resp.status_code,
                    'data': resp.text
                })

        return result_dict

